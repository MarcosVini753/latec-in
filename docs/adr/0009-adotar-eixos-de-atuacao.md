# ADR 0009: Adotar eixos de atuação como entidade central

## Status

Aceita

## Contexto

As imagens institucionais da LATEC.IN definem sete eixos de atuação e associam cada eixo a mentorias. Os eixos organizam ensino, pesquisa, extensão, produção científica e publicações.

## Decisão

Criar o app `axes` e modelar os eixos por meio de `ResearchAxis` e `AxisMentorship`.

Projetos, publicações científicas, posts, cursos e eventos poderão ser vinculados a um eixo.

## Consequências positivas

- A modelagem passa a refletir a organização real da LATEC.IN.
- Mentores podem publicar conteúdos vinculados aos próprios eixos.
- O frontend poderá filtrar conteúdos por eixo.

## Riscos e cuidados

- É necessário evitar inconsistência entre eixo, mentor e permissão editorial.
- A grafia de nomes de mentores deve ser validada antes do seed definitivo.
