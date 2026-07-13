# ADR 0007: Versionar API pública com /api/v1

## Status

Aceita

## Contexto

O frontend atual será migrado gradualmente de dados simulados em `js/data.js` para chamadas HTTP. A API deve poder evoluir sem quebrar o frontend público.

## Decisão

A API pública será versionada desde o início com o prefixo `/api/v1/`.

## Consequências positivas

- Facilita evolução futura da API.
- Reduz risco de quebra para consumidores existentes.
- Torna documentação e testes mais explícitos.

## Riscos e cuidados

- A equipe deve evitar criar endpoints públicos fora do prefixo versionado.
- Mudanças incompatíveis devem ser planejadas para versões futuras.
