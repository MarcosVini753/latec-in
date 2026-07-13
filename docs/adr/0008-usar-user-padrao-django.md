# ADR 0008: Usar User padrão do Django

## Status

Aceita

## Contexto

Não haverá necessidade de login por e-mail, múltiplos tipos de autenticação ou fluxos avançados de autenticação na primeira versão.

A administração será feita pelo Django Admin.

## Decisão

Usar o `User` padrão do Django, com autenticação básica por usuário e senha.

O vínculo com uma pessoa pública será opcional por meio de `accounts.Profile`.

## Consequências positivas

- Reduz complexidade inicial.
- Aproveita recursos nativos do Django Admin.
- Evita modelagem prematura de autenticação.

## Riscos e cuidados

- Caso surja necessidade futura de autenticação customizada, a migração deve ser planejada com cautela.
