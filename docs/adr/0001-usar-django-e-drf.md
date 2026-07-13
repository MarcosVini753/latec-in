# ADR 0001: Usar Django e Django REST Framework

## Status

Aceita

## Contexto

A LATEC.IN precisa de um backend para gerenciar conteúdo institucional, projetos, notícias, cursos, membros, materiais, parceiros, mensagens de contato, produções científicas e números de impacto.

O projeto já possui um protótipo frontend em HTML, CSS e JavaScript puro. Os dados ainda são simulados em `js/data.js`. A próxima fase exige persistência, administração de conteúdo e API pública.

## Decisão

Usar Django como framework backend e Django REST Framework para construção da API pública.

## Alternativas consideradas

- Django + Django REST Framework.
- Node.js com Express ou NestJS.
- Laravel.
- CMS pronto ou headless CMS.

## Consequências positivas

- O projeto ganha ORM, migrations, autenticação, permissões e Django Admin.
- A equipe pode evoluir a API gradualmente.
- Os dados simulados do protótipo podem ser substituídos por endpoints.

## Riscos e cuidados

- A equipe deve manter organização clara de apps, serializers, permissões e migrations.
- O Django Admin deve ser configurado com filtros, buscas e permissões adequadas.
