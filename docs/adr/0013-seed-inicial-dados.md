# ADR 0013: Criar seed inicial de dados

## Status

Aceita

## Contexto

O protótipo já possui dados simulados em `js/data.js`, e as imagens institucionais definem eixos, frentes de atuação e funções da plataforma.

O backend precisa nascer com dados mínimos para desenvolvimento e homologação.

## Decisão

Criar fixtures e/ou comando idempotente `seed_initial_data` para popular dados básicos.

## Consequências positivas

- Facilita desenvolvimento local.
- Facilita homologação com dados próximos do conteúdo real.
- Reduz trabalho manual no Django Admin.

## Riscos e cuidados

- O seed deve ser idempotente para evitar duplicações.
- Dados de nomes, mentores e eixos devem ser revisados antes de produção.
