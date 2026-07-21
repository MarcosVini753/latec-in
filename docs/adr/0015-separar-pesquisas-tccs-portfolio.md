# ADR 0015: Separar pesquisas, trabalhos acadêmicos, produção científica e portfólio

## Status

Aceita.

## Estado atual

A separação está implementada. A pesquisa de Bioativos foi publicada em `research`, sua origem no portfólio foi arquivada e as categorias históricas de pesquisa e produção científica foram removidas. A sequência de migração abaixo registra o processo já concluído.

## Contexto

O modelo atual permite que pesquisas e produção científica sejam tratadas como categorias de `portfolio.Project`, enquanto TCCs não possuem entidade própria.

Esses conteúdos têm dados, participantes, ciclo editorial e apresentação pública diferentes.

## Decisão

- pesquisas formais serão `research.ResearchProject`;
- TCCs e outros trabalhos acadêmicos serão `research.AcademicWork`;
- resultados publicados serão `scientific.ScientificOutput`;
- soluções, produtos, extensão e iniciativas práticas serão `portfolio.Project`.

As entidades poderão se relacionar para representar o encadeamento entre pesquisa, trabalho, publicação e solução.

## Alternativas consideradas

- manter tudo em `portfolio.Project`;
- criar apenas categorias adicionais no portfólio;
- separar os quatro conceitos por responsabilidade.

A terceira alternativa foi escolhida.

## Consequências positivas

- Filtros e páginas públicas coerentes.
- Equipes, autoria e orientação estruturadas.
- Menos ambiguidade no portfólio.
- Relações explícitas entre processo, trabalho, publicação e resultado prático.

## Consequências negativas e riscos

- Necessidade de novo app e migrations.
- Classificação manual dos registros históricos.
- Possibilidade de duplicação se as responsabilidades não forem respeitadas.

## Migração

1. Inventariar categorias históricas.
2. Classificar cada registro.
3. Criar os registros no domínio correto.
4. Relacionar entidades derivadas.
5. Manter no portfólio apenas iniciativas práticas.
6. Desativar categorias incompatíveis depois do backfill.
