# ADR 0002: Dividir o backend em apps por domínio

## Status

Aceita

## Contexto

O sistema envolve áreas distintas: pessoas, eixos, portfólio, notícias, cursos, arquivos, transparência, repositório científico, parceiros e métricas.

Um único app Django concentrando todos os modelos aumentaria acoplamento e dificultaria manutenção.

## Decisão

Organizar o backend em apps Django por domínio.

Apps planejados: `accounts`, `core`, `people`, `axes`, `portfolio`, `scientific`, `news`, `learning`, `transparency`, `mediahub`, `partnerships` e `metrics`.

## Consequências positivas

- Redução de acoplamento.
- Melhor organização de modelos e APIs.
- Implementação incremental por domínio.

## Riscos e cuidados

- É necessário evitar dependências circulares entre apps.
- `axes` e `mediahub` serão dependências compartilhadas por vários módulos.
