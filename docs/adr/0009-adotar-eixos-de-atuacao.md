# ADR 0009: Adotar os eixos de atuação da LATEC

## Status

Aceita

## Contexto

A LATEC possui sete eixos de atuação e mentorias associadas. A nova hierarquia estabelece que a Liga é unidade filha do LABTEC.IN.

Os eixos organizam prioritariamente atividades e conteúdos da LATEC; eles não representam a estrutura global do laboratório.

## Decisão

Manter o app `axes` e os models `ResearchAxis` e `AxisMentorship`.

- `ResearchAxis` terá vínculo obrigatório com `InstitutionalUnit`.
- Os sete eixos existentes pertencerão à unidade LATEC.
- Projetos, publicações, cursos, eventos e pesquisas poderão se relacionar com eixo quando aplicável.
- Pesquisas do LABTEC.IN terão eixo opcional.

## Consequências positivas

- Preserva a organização real da LATEC.
- Permite mentorias e filtros por eixo.
- Evita impor os eixos a todos os conteúdos do LABTEC.IN.

## Riscos e cuidados

- Validar compatibilidade entre unidade e eixo.
- Aplicar permissões de mentores somente aos próprios eixos.
- Confirmar nomes de mentores antes do seed definitivo.
