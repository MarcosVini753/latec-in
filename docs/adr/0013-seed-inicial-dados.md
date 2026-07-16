# ADR 0013: Criar seed inicial de dados

## Status

Aceita

## Contexto

O backend já possui um comando idempotente `seed_initial_data`, derivado do protótipo e da estrutura institucional anterior.

A arquitetura alvo precisa representar LABTEC.IN como raiz, LATEC como filha e classificar conteúdos por unidade, sem perder a reprodutibilidade do ambiente.

## Decisão

Manter um seed idempotente e evoluí-lo para incluir:

- LABTEC.IN e LATEC;
- memberships;
- sete eixos da LATEC e mentorias;
- configurações do portal vinculadas ao LABTEC.IN;
- perfil institucional da LATEC;
- pesquisas e tipos de trabalhos acadêmicos;
- conteúdos classificados por unidade;
- métricas separadas por unidade e modo de agregação.

Registros históricos de projetos serão revisados manualmente antes de reclassificação.

## Consequências positivas

- Desenvolvimento e homologação reproduzíveis.
- Estrutura institucional disponível desde a carga inicial.
- Backfill testável com dados conhecidos.

## Riscos e cuidados

- Preservar idempotência.
- Não sobrescrever conteúdo editorial manual fora da responsabilidade do seed.
- Validar nomes, papéis, projetos, autoria e métricas antes de produção.
