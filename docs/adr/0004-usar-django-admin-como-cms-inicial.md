# ADR 0004: Usar Django Admin como CMS inicial

## Status

Aceita

## Contexto

O LABTEC.IN precisa administrar conteúdos do laboratório e de unidades filhas, incluindo a LATEC, com revisão editorial e permissões por escopo institucional.

Construir um painel próprio nesta fase aumentaria prazo e complexidade sem necessidade comprovada.

## Decisão

Usar Django Admin como CMS inicial do portal LABTEC.IN.

O Admin gerenciará unidades, memberships, pesquisas, trabalhos acadêmicos e os demais conteúdos. Listas, formulários e ações deverão respeitar as unidades autorizadas do usuário.

## Consequências positivas

- Menor tempo de implementação.
- Foco em modelagem, migração, API e qualidade dos dados.
- Administração do laboratório e de unidades filhas no mesmo sistema.

## Riscos e cuidados

- Filtrar registros e opções de relacionamento por unidade.
- Evitar que coordenadores ou mentores acessem unidades não autorizadas.
- Avaliar painel próprio somente quando limitações concretas do Admin justificarem.
