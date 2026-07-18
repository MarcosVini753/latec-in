import importlib

from django.contrib import admin
from django.apps import apps as django_apps
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.test import RequestFactory, TestCase

from apps.accounts.admin import ProfileAdmin
from apps.accounts.models import Profile
from apps.axes.admin import ResearchAxisAdmin
from apps.axes.models import AxisMentorship, ResearchAxis
from apps.common.admin_actions import mark_as_in_review, mark_as_published
from apps.common.models import EditorialStatus
from apps.institutional.admin import InstitutionMembershipAdmin, InstitutionalUnitAdmin
from apps.institutional.models import InstitutionMembership, InstitutionalUnit
from apps.partnerships.admin import ContactMessageAdmin, PartnerAdmin
from apps.partnerships.models import ContactMessage, Partner
from apps.people.models import Person
from apps.portfolio.admin import ProjectAdmin, ProjectTeamMemberAdmin, ProjectTeamMemberInline
from apps.portfolio.models import Project, ProjectCategory, ProjectTeamMember


class InstitutionalAdminPermissionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.labtec = InstitutionalUnit.objects.create(
            name="LABTEC.IN",
            acronym="LABTEC.IN",
            slug="labtec-in",
            unit_type=InstitutionalUnit.UnitType.LABORATORY,
        )
        cls.latec = InstitutionalUnit.objects.create(
            name="Liga Acadêmica de Tecnologia e Inovação",
            acronym="LATEC",
            slug="latec",
            unit_type=InstitutionalUnit.UnitType.ACADEMIC_LEAGUE,
            parent=cls.labtec,
        )
        cls.descendant = InstitutionalUnit.objects.create(
            name="Núcleo LATEC",
            acronym="NL",
            slug="nucleo-latec",
            unit_type=InstitutionalUnit.UnitType.INITIATIVE,
            parent=cls.latec,
        )
        cls.other = InstitutionalUnit.objects.create(
            name="Outro laboratório",
            acronym="OUTRO",
            slug="outro",
            unit_type=InstitutionalUnit.UnitType.LABORATORY,
        )

        cls.mentor_person = Person.objects.create(full_name="Mentora", slug="mentora")
        cls.member = Person.objects.create(full_name="Integrante", slug="integrante")
        InstitutionMembership.objects.create(person=cls.mentor_person, unit=cls.latec, role="Mentor")
        InstitutionMembership.objects.create(person=cls.member, unit=cls.latec, role="Integrante")

        cls.mentor_axis = ResearchAxis.objects.create(
            unit=cls.latec,
            number=1,
            title="Eixo mentorado",
            slug="eixo-mentorado",
        )
        cls.other_latec_axis = ResearchAxis.objects.create(
            unit=cls.latec,
            number=2,
            title="Outro eixo LATEC",
            slug="outro-eixo-latec",
        )
        cls.descendant_axis = ResearchAxis.objects.create(
            unit=cls.descendant,
            number=3,
            title="Eixo descendente",
            slug="eixo-descendente",
        )
        cls.other_axis = ResearchAxis.objects.create(
            unit=cls.other,
            number=4,
            title="Eixo externo",
            slug="eixo-externo",
        )
        AxisMentorship.objects.create(axis=cls.mentor_axis, person=cls.mentor_person)
        cls.category = ProjectCategory.objects.create(name="Ensino", slug="ensino")

        cls.projects = {
            "labtec": Project.objects.create(unit=cls.labtec, title="Projeto LABTEC", slug="projeto-labtec"),
            "latec": Project.objects.create(
                unit=cls.latec,
                axis=cls.mentor_axis,
                title="Projeto LATEC",
                slug="projeto-latec",
            ),
            "latec_other_axis": Project.objects.create(
                unit=cls.latec,
                axis=cls.other_latec_axis,
                title="Projeto em outro eixo",
                slug="projeto-outro-eixo",
            ),
            "descendant": Project.objects.create(
                unit=cls.descendant,
                axis=cls.descendant_axis,
                title="Projeto descendente",
                slug="projeto-descendente",
            ),
            "other": Project.objects.create(
                unit=cls.other,
                axis=cls.other_axis,
                title="Projeto externo",
                slug="projeto-externo",
            ),
            "null": Project.objects.create(title="Projeto sem unidade", slug="projeto-sem-unidade"),
        }

        cls.users = {}
        cls.profiles = {}
        cls._make_profile("admin", Profile.AdminRole.ADMIN)
        cls._make_profile(
            "lab_coordinator",
            Profile.AdminRole.LAB_COORDINATOR,
            primary_unit=cls.labtec,
            inherit_descendants=True,
        )
        cls._make_profile("unit_coordinator", Profile.AdminRole.UNIT_COORDINATOR, primary_unit=cls.latec)
        cls._make_profile("mentor", Profile.AdminRole.MENTOR, primary_unit=cls.latec, person=cls.mentor_person)
        cls._make_profile("editor", Profile.AdminRole.EDITOR, authorized_units=(cls.latec,))
        cls._make_profile("reader", Profile.AdminRole.READER, authorized_units=(cls.latec,))
        cls._make_profile("inactive_profile", Profile.AdminRole.EDITOR, is_active_admin=False)
        cls._make_profile("wrong_lab_coordinator", Profile.AdminRole.LAB_COORDINATOR, primary_unit=cls.latec)
        cls.users["no_profile"] = get_user_model().objects.create_user("no_profile", is_staff=True)
        cls.users["superuser"] = get_user_model().objects.create_superuser(
            "superuser",
            "super@example.com",
            "password",
        )

    @classmethod
    def _make_profile(
        cls,
        username,
        role,
        *,
        primary_unit=None,
        authorized_units=(),
        inherit_descendants=False,
        person=None,
        is_active_admin=True,
    ):
        user = get_user_model().objects.create_user(username, is_staff=True)
        profile = Profile.objects.create(
            user=user,
            person=person,
            role=role,
            primary_unit=primary_unit,
            inherit_descendants=inherit_descendants,
            is_active_admin=is_active_admin,
        )
        profile.authorized_units.add(*authorized_units)
        cls.users[username] = user
        cls.profiles[username] = profile

    def setUp(self):
        self.factory = RequestFactory()
        self.project_admin = ProjectAdmin(Project, admin.site)

    def request_for(self, username, method="get", data=None):
        request = getattr(self.factory, method)("/admin/", data=data or {})
        request.user = self.users[username]
        return request

    def project_slugs_for(self, username):
        return set(self.project_admin.get_queryset(self.request_for(username)).values_list("slug", flat=True))

    def test_queryset_matrix_covers_global_root_unit_descendant_null_and_inactive_scopes(self):
        all_slugs = {project.slug for project in self.projects.values()}
        self.assertEqual(self.project_slugs_for("superuser"), all_slugs)
        self.assertEqual(self.project_slugs_for("admin"), all_slugs)
        self.assertEqual(
            self.project_slugs_for("lab_coordinator"),
            {
                "projeto-labtec",
                "projeto-latec",
                "projeto-outro-eixo",
                "projeto-descendente",
                "projeto-sem-unidade",
            },
        )
        self.assertEqual(
            self.project_slugs_for("unit_coordinator"),
            {"projeto-latec", "projeto-outro-eixo"},
        )
        self.profiles["unit_coordinator"].inherit_descendants = True
        self.profiles["unit_coordinator"].save(update_fields=("inherit_descendants",))
        self.assertIn("projeto-descendente", self.project_slugs_for("unit_coordinator"))
        self.assertEqual(self.project_slugs_for("editor"), {"projeto-latec", "projeto-outro-eixo"})
        self.assertEqual(self.project_slugs_for("reader"), {"projeto-latec", "projeto-outro-eixo"})
        self.assertFalse(self.project_slugs_for("inactive_profile"))
        self.assertFalse(self.project_slugs_for("no_profile"))
        self.assertFalse(self.project_slugs_for("wrong_lab_coordinator"))

        self.profiles["lab_coordinator"].authorized_units.add(self.other)
        self.assertNotIn("projeto-externo", self.project_slugs_for("lab_coordinator"))

    def test_mentor_is_limited_to_axis_mentorship(self):
        self.assertEqual(self.project_slugs_for("mentor"), {"projeto-latec"})

        AxisMentorship.objects.create(axis=self.other_axis, person=self.mentor_person)
        self.profiles["mentor"].authorized_units.add(self.other)
        self.profiles["mentor"].inherit_descendants = True
        self.profiles["mentor"].save(update_fields=("inherit_descendants",))
        self.assertEqual(self.project_slugs_for("mentor"), {"projeto-latec"})

        unit_field = Project._meta.get_field("unit")
        axis_field = Project._meta.get_field("axis")
        unit_choices = self.project_admin.formfield_for_foreignkey(
            unit_field,
            self.request_for("mentor"),
        ).queryset
        axis_choices = self.project_admin.formfield_for_foreignkey(
            axis_field,
            self.request_for("mentor"),
        ).queryset
        self.assertEqual(set(unit_choices.values_list("slug", flat=True)), {"latec"})
        self.assertEqual(set(axis_choices.values_list("slug", flat=True)), {"eixo-mentorado"})

    def test_only_admin_and_root_lab_coordinator_can_publish_archive_or_edit_published(self):
        published = self.projects["latec"]
        published.editorial_status = EditorialStatus.PUBLISHED
        published.is_published = True
        published.save(update_fields=("editorial_status", "is_published"))

        for username in ("unit_coordinator", "mentor", "editor", "reader", "wrong_lab_coordinator"):
            with self.subTest(username=username):
                request = self.request_for(username)
                self.assertFalse(self.project_admin.has_change_permission(request, published))
                self.assertNotIn("mark_as_published", self.project_admin.get_actions(request))
                self.assertNotIn("mark_as_archived", self.project_admin.get_actions(request))

        for username in ("superuser", "admin", "lab_coordinator"):
            with self.subTest(username=username):
                request = self.request_for(username)
                self.assertTrue(self.project_admin.has_change_permission(request, published))
                self.assertIn("mark_as_published", self.project_admin.get_actions(request))
                self.assertIn("mark_as_archived", self.project_admin.get_actions(request))

        self.assertFalse(self.profiles["wrong_lab_coordinator"].can_publish)

    def test_archived_content_is_final_for_non_publishers(self):
        archived = self.projects["latec_other_axis"]
        archived.editorial_status = EditorialStatus.ARCHIVED
        archived.is_published = False
        archived.save(update_fields=("editorial_status", "is_published"))
        editor_request = self.request_for("editor", method="post")

        self.assertFalse(self.project_admin.has_change_permission(editor_request, archived))
        mark_as_in_review(self.project_admin, editor_request, Project.objects.filter(pk=archived.pk))

        archived.refresh_from_db()
        self.assertEqual(archived.editorial_status, EditorialStatus.ARCHIVED)

    def test_server_side_save_rejects_tampered_scope_and_final_status(self):
        editor_request = self.request_for("editor", method="post")
        allowed = Project(
            unit=self.latec,
            axis=self.mentor_axis,
            title="Rascunho permitido",
            slug="rascunho-permitido",
        )
        self.project_admin.save_model(editor_request, allowed, form=None, change=False)
        self.assertTrue(Project.objects.filter(slug="rascunho-permitido").exists())

        outside = Project(unit=self.other, axis=self.other_axis, title="Adulterado", slug="adulterado")
        with self.assertRaises(PermissionDenied):
            self.project_admin.save_model(editor_request, outside, form=None, change=False)
        self.assertFalse(Project.objects.filter(slug="adulterado").exists())

        final = Project(
            unit=self.latec,
            axis=self.mentor_axis,
            title="Publicação adulterada",
            slug="publicacao-adulterada",
            editorial_status=EditorialStatus.PUBLISHED,
            is_published=True,
        )
        with self.assertRaises(PermissionDenied):
            self.project_admin.save_model(editor_request, final, form=None, change=False)
        self.assertFalse(Project.objects.filter(slug="publicacao-adulterada").exists())

    def test_actions_intersect_the_scoped_queryset_and_cannot_unpublish_as_editor(self):
        latec_draft = self.projects["latec"]
        other_draft = self.projects["other"]
        mark_as_published(self.project_admin, self.request_for("editor", method="post"), Project.objects.all())
        latec_draft.refresh_from_db()
        other_draft.refresh_from_db()
        self.assertFalse(latec_draft.is_published)
        self.assertFalse(other_draft.is_published)

        mark_as_published(
            self.project_admin,
            self.request_for("lab_coordinator", method="post"),
            Project.objects.all(),
        )
        latec_draft.refresh_from_db()
        other_draft.refresh_from_db()
        self.assertTrue(latec_draft.is_published)
        self.assertFalse(other_draft.is_published)

        mark_as_in_review(
            self.project_admin,
            self.request_for("editor", method="post"),
            Project.objects.filter(pk=latec_draft.pk),
        )
        latec_draft.refresh_from_db()
        self.assertTrue(latec_draft.is_published)
        self.assertEqual(latec_draft.editorial_status, EditorialStatus.PUBLISHED)

    def test_reader_is_view_only_and_editor_can_edit_drafts(self):
        draft = self.projects["latec"]
        reader_request = self.request_for("reader")
        self.assertTrue(self.project_admin.has_view_permission(reader_request, draft))
        self.assertFalse(self.project_admin.has_add_permission(reader_request))
        self.assertFalse(self.project_admin.has_change_permission(reader_request, draft))
        self.assertFalse(self.project_admin.has_delete_permission(reader_request, draft))
        self.assertTrue(self.project_admin.has_change_permission(self.request_for("editor"), draft))
        self.assertFalse(self.project_admin.has_delete_permission(self.request_for("editor"), draft))

    def test_public_flags_without_workflow_stay_under_final_publication_control(self):
        axis_admin = ResearchAxisAdmin(ResearchAxis, admin.site)
        editor_request = self.request_for("editor", method="post")

        self.assertFalse(axis_admin.has_change_permission(editor_request, self.mentor_axis))
        draft_axis = ResearchAxis(
            unit=self.latec,
            number=50,
            title="Novo eixo em rascunho",
            slug="novo-eixo-em-rascunho",
        )
        axis_admin.save_model(editor_request, draft_axis, form=None, change=False)

        self.assertFalse(draft_axis.is_active)
        self.assertIn("is_active", axis_admin.get_readonly_fields(editor_request))
        self.assertTrue(axis_admin.has_change_permission(editor_request, draft_axis))
        self.assertTrue(
            axis_admin.has_change_permission(self.request_for("lab_coordinator"), self.mentor_axis)
        )

    def test_unit_autocomplete_is_queryable_but_scoped_for_non_managers(self):
        editor = self.users["editor"]
        self.client.force_login(editor)
        response = self.client.get(
            "/admin/autocomplete/",
            {
                "app_label": "portfolio",
                "model_name": "project",
                "field_name": "unit",
                "term": "",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual({item["text"] for item in response.json()["results"]}, {"LATEC"})

        category_response = self.client.get(
            "/admin/autocomplete/",
            {
                "app_label": "portfolio",
                "model_name": "project",
                "field_name": "category",
                "term": "Ensino",
            },
        )
        self.assertEqual(category_response.status_code, 200)
        self.assertEqual([item["text"] for item in category_response.json()["results"]], ["Ensino"])

        unit_admin = InstitutionalUnitAdmin(InstitutionalUnit, admin.site)
        self.assertFalse(unit_admin.has_module_permission(self.request_for("lab_coordinator")))
        self.assertTrue(unit_admin.has_view_permission(self.request_for("editor")))
        self.assertFalse(unit_admin.has_change_permission(self.request_for("editor"), self.latec))

    def test_child_autocomplete_hides_published_parents_from_non_publishers(self):
        published = self.projects["latec"]
        published.editorial_status = EditorialStatus.PUBLISHED
        published.is_published = True
        published.save(update_fields=("editorial_status", "is_published"))
        self.client.force_login(self.users["editor"])

        response = self.client.get(
            "/admin/autocomplete/",
            {
                "app_label": "portfolio",
                "model_name": "projectteammember",
                "field_name": "project",
                "term": "Projeto",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn(str(published), {item["text"] for item in response.json()["results"]})

    def test_editor_cannot_delete_reference_records(self):
        person_admin = admin.site._registry[Person]
        editor_request = self.request_for("editor")
        inactive_person = Person.objects.create(
            full_name="Pessoa inativa",
            slug="pessoa-inativa",
            is_active=False,
        )
        InstitutionMembership.objects.create(person=inactive_person, unit=self.latec, role="Integrante")

        self.assertTrue(person_admin.has_change_permission(editor_request, inactive_person))
        self.assertFalse(person_admin.has_delete_permission(editor_request, inactive_person))
        self.assertNotIn("delete_selected", person_admin.get_actions(editor_request))

    def test_editor_cannot_gain_descendants_by_tampering_inheritance_flag(self):
        self.profiles["editor"].inherit_descendants = True
        self.profiles["editor"].save(update_fields=("inherit_descendants",))
        self.assertEqual(self.project_slugs_for("editor"), {"projeto-latec", "projeto-outro-eixo"})

    def test_inline_permissions_follow_parent_and_block_published_children(self):
        inline = ProjectTeamMemberInline(Project, admin.site)
        member_admin = ProjectTeamMemberAdmin(ProjectTeamMember, admin.site)
        draft = self.projects["latec"]
        self.assertTrue(inline.has_add_permission(self.request_for("editor"), draft))

        draft.editorial_status = EditorialStatus.PUBLISHED
        draft.is_published = True
        draft.save(update_fields=("editorial_status", "is_published"))
        self.assertFalse(inline.has_add_permission(self.request_for("editor"), draft))
        self.assertTrue(inline.has_add_permission(self.request_for("lab_coordinator"), draft))

        editor_request = self.request_for("editor", method="post")
        project_field = ProjectTeamMember._meta.get_field("project")
        project_choices = member_admin.formfield_for_foreignkey(project_field, editor_request).queryset
        self.assertNotIn(draft.pk, project_choices.values_list("pk", flat=True))
        with self.assertRaises(PermissionDenied):
            member_admin.save_model(
                editor_request,
                ProjectTeamMember(project=draft, person=self.member),
                form=None,
                change=False,
            )

    def test_shared_partner_is_visible_but_only_root_roles_can_edit(self):
        single = Partner.objects.create(name="Parceiro LATEC", slug="parceiro-latec", is_active=False)
        single.units.add(self.latec)
        shared = Partner.objects.create(name="Parceiro compartilhado", slug="parceiro-compartilhado")
        shared.units.add(self.labtec, self.latec)
        partner_admin = PartnerAdmin(Partner, admin.site)
        editor_request = self.request_for("editor")

        self.assertEqual(
            set(partner_admin.get_queryset(editor_request).values_list("slug", flat=True)),
            {"parceiro-latec", "parceiro-compartilhado"},
        )
        self.assertTrue(partner_admin.has_change_permission(editor_request, single))
        self.assertFalse(partner_admin.has_change_permission(editor_request, shared))
        self.assertTrue(partner_admin.has_change_permission(self.request_for("lab_coordinator"), shared))

    def test_lab_coordinator_can_create_unassigned_partner(self):
        self.client.force_login(self.users["lab_coordinator"])

        response = self.client.post(
            "/admin/partnerships/partner/add/",
            {
                "name": "Parceiro sem unidade",
                "slug": "parceiro-sem-unidade",
                "partner_type": Partner.PartnerType.INSTITUTIONAL,
                "description": "",
                "website": "",
                "is_active": "on",
                "display_order": 0,
                "_save": "Salvar",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Partner.objects.get(slug="parceiro-sem-unidade").units.exists())

    def test_tampered_shared_partner_post_rolls_back(self):
        self.profiles["editor"].authorized_units.add(self.descendant)
        self.client.force_login(self.users["editor"])
        response = self.client.post(
            "/admin/partnerships/partner/add/",
            {
                "units": [self.latec.pk, self.descendant.pk],
                "name": "Parceiro adulterado",
                "slug": "parceiro-adulterado",
                "partner_type": Partner.PartnerType.INSTITUTIONAL,
                "description": "",
                "website": "",
                "is_active": "on",
                "display_order": 0,
                "_save": "Salvar",
            },
        )
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Partner.objects.filter(slug="parceiro-adulterado").exists())

    def test_contact_membership_profile_and_unit_management_are_restricted(self):
        contact = ContactMessage.objects.create(
            subject="Contato",
            name="Pessoa",
            email="pessoa@example.com",
            message="Mensagem",
        )
        contact_admin = ContactMessageAdmin(ContactMessage, admin.site)
        membership_admin = InstitutionMembershipAdmin(InstitutionMembership, admin.site)
        profile_admin = ProfileAdmin(Profile, admin.site)
        unit_admin = InstitutionalUnitAdmin(InstitutionalUnit, admin.site)

        self.assertFalse(contact_admin.has_view_permission(self.request_for("editor"), contact))
        self.assertTrue(contact_admin.has_change_permission(self.request_for("lab_coordinator"), contact))
        self.assertFalse(membership_admin.has_module_permission(self.request_for("editor")))
        self.assertTrue(membership_admin.has_module_permission(self.request_for("lab_coordinator")))
        self.assertFalse(profile_admin.has_module_permission(self.request_for("lab_coordinator")))
        self.assertTrue(profile_admin.has_module_permission(self.request_for("admin")))
        self.assertFalse(unit_admin.has_change_permission(self.request_for("lab_coordinator"), self.latec))
        self.assertTrue(unit_admin.has_change_permission(self.request_for("admin"), self.latec))

        unassigned_person = Person.objects.create(full_name="Pessoa ainda sem vínculo", slug="sem-vinculo")
        person_field = InstitutionMembership._meta.get_field("person")
        person_choices = membership_admin.formfield_for_foreignkey(
            person_field,
            self.request_for("lab_coordinator"),
        ).queryset
        self.assertIn(unassigned_person.pk, person_choices.values_list("pk", flat=True))

    def test_profile_data_migration_maps_only_active_legacy_scopes(self):
        active_user = get_user_model().objects.create_user("legacy_coordinator", is_staff=True)
        inactive_user = get_user_model().objects.create_user("legacy_inactive", is_staff=True)
        disabled_user = get_user_model().objects.create_user(
            "legacy_disabled_user",
            is_staff=True,
            is_active=False,
        )
        mentor_user = get_user_model().objects.create_user("legacy_mentor", is_staff=True)
        outside_mentor_user = get_user_model().objects.create_user("legacy_outside_mentor", is_staff=True)
        mentor_person = Person.objects.create(full_name="Mentor legado", slug="mentor-legado")
        outside_mentor_person = Person.objects.create(
            full_name="Mentor legado externo",
            slug="mentor-legado-externo",
        )
        AxisMentorship.objects.create(axis=self.mentor_axis, person=mentor_person)
        AxisMentorship.objects.create(axis=self.other_axis, person=outside_mentor_person)
        active = Profile.objects.create(user=active_user, role="coordinator")
        inactive = Profile.objects.create(
            user=inactive_user,
            role="coordinator",
            is_active_admin=False,
        )
        disabled = Profile.objects.create(user=disabled_user, role="coordinator")
        mentor = Profile.objects.create(user=mentor_user, person=mentor_person, role=Profile.AdminRole.MENTOR)
        outside_mentor = Profile.objects.create(
            user=outside_mentor_user,
            person=outside_mentor_person,
            role=Profile.AdminRole.MENTOR,
        )

        migration = importlib.import_module("apps.accounts.migrations.0002_add_institutional_admin_scope")
        migration.migrate_legacy_profile_scopes(django_apps, None)

        active.refresh_from_db()
        inactive.refresh_from_db()
        disabled.refresh_from_db()
        mentor.refresh_from_db()
        outside_mentor.refresh_from_db()
        self.assertEqual(active.role, Profile.AdminRole.LAB_COORDINATOR)
        self.assertEqual(active.primary_unit, self.labtec)
        self.assertTrue(active.inherit_descendants)
        self.assertEqual(inactive.role, Profile.AdminRole.LAB_COORDINATOR)
        self.assertIsNone(inactive.primary_unit)
        self.assertFalse(inactive.inherit_descendants)
        self.assertIsNone(disabled.primary_unit)
        self.assertFalse(disabled.inherit_descendants)
        self.assertEqual(mentor.primary_unit, self.latec)
        self.assertIsNone(outside_mentor.primary_unit)
