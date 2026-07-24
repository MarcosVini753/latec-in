# ADR 0001: Usar Django e Django REST Framework

## Status

Aceita

## Contexto

O portal do LABTEC.IN precisa gerenciar conteúdos do Laboratório de Biotecnologia, Biodiversidade e Inovação e de suas unidades filhas, incluindo a LATEC.

O repositório possui frontend em HTML, CSS e JavaScript puro e backend Django já implementado. A arquitetura requer persistência, administração institucional, workflow editorial e API pública `/api/v1/`.

## Decisão

Usar Django como framework backend e Django REST Framework para a API pública do portal LABTEC.IN.

A LATEC será modelada como unidade institucional dentro do mesmo backend e da mesma API.

## Alternativas consideradas

- Django e Django REST Framework.
- Node.js com Express ou NestJS.
- Laravel.
- CMS pronto ou headless CMS.

## Consequências positivas

- ORM, migrations, autenticação, permissões e Django Admin integrados.
- Evolução incremental da API.
- Administração de conteúdos do laboratório e de unidades filhas.
- Substituição gradual dos dados locais do frontend.

## Riscos e cuidados

- Manter apps, serializers, permissões e migrations organizados.
- Aplicar escopo institucional sem duplicar backends por unidade.
- Configurar o Django Admin com filtros, buscas e permissões adequadas.
