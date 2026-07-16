# ADR 0005: Separar pessoas de usuários administrativos

## Status

Aceita

## Contexto

O portal exibirá coordenadores, pesquisadores, professores, mentores, ligantes, colaboradores e egressos. Uma pessoa pode atuar em mais de uma unidade e exercer papéis diferentes sem precisar de acesso administrativo.

Misturar identidade pública, vínculo institucional e autenticação criaria dependência desnecessária.

## Decisão

Manter `people.Person` separado do `User` padrão do Django.

- `accounts.Profile` vincula opcionalmente usuário e pessoa.
- `institutional.InstitutionMembership` representa papéis da pessoa por unidade e período.
- o campo único atual `Person.role` será tratado como legado e retirado gradualmente.

## Consequências positivas

- Pessoas podem aparecer publicamente sem usuário.
- Uma pessoa pode ter papéis distintos no LABTEC.IN e na LATEC.
- Autenticação permanece simples.
- Histórico institucional pode ser preservado.

## Riscos e cuidados

- Evitar duplicação de memberships equivalentes.
- Migrar `Person.role` antes de removê-lo.
- Diferenciar papel institucional de papel administrativo.
