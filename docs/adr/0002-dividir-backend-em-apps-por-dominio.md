# ADR 0002: Dividir o backend em apps por domínio

## Status
Aceita

## Contexto
O sistema envolve áreas distintas: pessoas, portfólio, notícias, cursos, arquivos, parceiros e métricas.

## Decisão
Organizar o backend em apps Django por domínio: accounts, core, people, portfolio, news, learning, mediahub, partnerships e metrics.

## Consequências
A separação reduz acoplamento, facilita testes e permite evolução incremental dos módulos.
