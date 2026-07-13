# ADR 0010: Adotar workflow editorial simples

## Status

Aceita

## Contexto

A LATEC.IN terá publicações feitas por coordenadora, editores e mentores. Conteúdos não devem ficar públicos automaticamente antes de revisão.

## Decisão

Adotar os status editoriais `draft`, `in_review`, `published` e `archived`.

Mentores podem criar e enviar conteúdos para revisão. A publicação final fica sob responsabilidade da coordenação.

## Consequências positivas

- Separa cadastro de conteúdo de publicação pública.
- Permite revisão pela coordenação.
- Mantém API pública restrita a conteúdos publicados.

## Riscos e cuidados

- O Django Admin deve facilitar mudança de status.
- A API pública deve filtrar corretamente conteúdos não publicados.
