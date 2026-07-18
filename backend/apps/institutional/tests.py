from datetime import date

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models import F
from django.test import TestCase

from apps.institutional.models import InstitutionMembership, InstitutionalUnit
from apps.people.models import Person, Role


class InstitutionalIntegrityTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.role = Role.objects.create(name="Pesquisador", slug="pesquisador-integridade")
        cls.person = Person.objects.create(full_name="Pessoa Teste", slug="pessoa-teste-integridade")
        cls.root = InstitutionalUnit.objects.create(
            name="Unidade raiz",
            acronym="RAIZ",
            slug="unidade-raiz-integridade",
            unit_type=InstitutionalUnit.UnitType.LABORATORY,
        )

    def test_membership_rejects_duplicate_person_unit_and_role(self):
        InstitutionMembership.objects.create(person=self.person, unit=self.root, role="Pesquisador")
        duplicate = InstitutionMembership(person=self.person, unit=self.root, role="Pesquisador")

        with self.assertRaises(ValidationError):
            duplicate.full_clean()
        with self.assertRaises(IntegrityError), transaction.atomic():
            duplicate.save()

    def test_membership_rejects_end_date_before_start_date(self):
        membership = InstitutionMembership(
            person=self.person,
            unit=self.root,
            role="Pesquisador",
            start_date=date(2026, 2, 1),
            end_date=date(2026, 1, 31),
        )

        with self.assertRaisesMessage(ValidationError, "igual ou posterior"):
            membership.full_clean()
        with self.assertRaises(IntegrityError), transaction.atomic():
            membership.save()

    def test_membership_accepts_open_date_ranges(self):
        InstitutionMembership.objects.create(
            person=self.person,
            unit=self.root,
            role="Início aberto",
            end_date=date(2026, 1, 31),
        )
        InstitutionMembership.objects.create(
            person=self.person,
            unit=self.root,
            role="Término aberto",
            start_date=date(2026, 2, 1),
        )

        self.assertEqual(InstitutionMembership.objects.count(), 2)

    def test_unit_save_rejects_direct_self_parent(self):
        self.root.parent = self.root

        with self.assertRaisesMessage(ValidationError, "ciclo"):
            self.root.save()

    def test_database_constraint_rejects_direct_self_parent_through_update(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            InstitutionalUnit.objects.filter(pk=self.root.pk).update(parent_id=F("id"))

    def test_unit_save_rejects_indirect_cycle(self):
        child = InstitutionalUnit.objects.create(
            name="Unidade filha",
            acronym="FILHA",
            slug="unidade-filha-integridade",
            unit_type=InstitutionalUnit.UnitType.INITIATIVE,
            parent=self.root,
        )
        grandchild = InstitutionalUnit.objects.create(
            name="Unidade neta",
            acronym="NETA",
            slug="unidade-neta-integridade",
            unit_type=InstitutionalUnit.UnitType.INITIATIVE,
            parent=child,
        )
        self.root.parent = grandchild

        with self.assertRaisesMessage(ValidationError, "ciclo"):
            self.root.save()

    def test_bulk_create_rejects_units_with_parent(self):
        child = InstitutionalUnit(
            name="Unidade em lote",
            acronym="LOTE",
            slug="unidade-em-lote-integridade",
            unit_type=InstitutionalUnit.UnitType.INITIATIVE,
            parent=self.root,
        )

        with self.assertRaisesMessage(ValidationError, "salvas individualmente"):
            InstitutionalUnit.objects.bulk_create([child])

    def test_bulk_create_accepts_root_units(self):
        InstitutionalUnit.objects.bulk_create(
            [
                InstitutionalUnit(
                    name="Outra raiz",
                    acronym="OUTRA",
                    slug="outra-raiz-integridade",
                    unit_type=InstitutionalUnit.UnitType.LABORATORY,
                )
            ]
        )

        self.assertTrue(
            InstitutionalUnit.objects.filter(slug="outra-raiz-integridade").exists()
        )

    def test_bulk_update_rejects_parent_changes(self):
        child = InstitutionalUnit.objects.create(
            name="Filha para lote",
            acronym="FILHA LOTE",
            slug="filha-para-lote-integridade",
            unit_type=InstitutionalUnit.UnitType.INITIATIVE,
        )
        child.parent = self.root

        with self.assertRaisesMessage(ValidationError, "bulk_update"):
            InstitutionalUnit.objects.bulk_update([child], ["parent"])
