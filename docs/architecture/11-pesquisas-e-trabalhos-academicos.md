# Pesquisas e trabalhos acadêmicos do LABTEC.IN

O LABTEC.IN é responsável institucional por pesquisas, TCCs e outros trabalhos acadêmicos publicados no portal. A LATEC pode possuir conteúdos próprios ou se relacionar com pesquisas por unidade e eixo, mas não substitui o laboratório como raiz.

## Estado implementado

Hoje não existe app `research`.

- pesquisas podem aparecer como `portfolio.Project` na categoria “Pesquisa”;
- produção científica pode aparecer como categoria de portfólio;
- `scientific.ScientificOutput` registra resultados publicados, com autoria textual;
- não há entidade própria para TCCs;
- não há equipe estruturada de pesquisa;
- não há vínculo institucional.

Essa sobreposição dificulta filtros, autoria, histórico e apresentação pública.

## Arquitetura alvo

O novo app `research` concentra o processo de pesquisa e os trabalhos acadêmicos. `scientific` mantém resultados publicados e `portfolio` mantém soluções e iniciativas práticas.

## `ResearchProject`

Representa pesquisa científica formal com período, objetivos, metodologia e equipe.

Campos:

- `title`;
- `slug`;
- `unit`;
- `axis`, opcional;
- `summary`;
- `objectives`;
- `methodology`;
- `expected_results`;
- `start_date`;
- `end_date`;
- `project_status`;
- `editorial_status`;
- `cover_image`;
- `is_published`;
- `published_at`;
- `is_featured`;
- timestamps.

Regra inicial: a pesquisa normalmente pertence ao LABTEC.IN. A relação com eixo é opcional e indica conexão com um eixo da LATEC.

## `ResearchProjectMember`

Relaciona pesquisa e pessoa.

Campos:

- `research_project`;
- `person`;
- `role`;
- `is_coordinator`;
- `display_order`;
- timestamps.

Papéis:

- coordenador;
- pesquisador;
- orientador;
- bolsista;
- voluntário;
- colaborador.

## `AcademicWork`

Representa TCC e outros trabalhos acadêmicos.

Campos:

- `title`;
- `slug`;
- `unit`;
- `research_project`, opcional;
- `work_type`;
- `course`;
- `institution`;
- `year`;
- `abstract`;
- `keywords`;
- `file`;
- `external_url`;
- `editorial_status`;
- `is_published`;
- `published_at`;
- `is_featured`;
- timestamps.

Tipos:

- `tcc`;
- `monograph`;
- `scientific_initiation`;
- `dissertation`;
- `thesis`;
- `other`.

## `AcademicWorkContributor`

Relaciona trabalho acadêmico e pessoa.

Campos:

- `academic_work`;
- `person`;
- `role`;
- `display_order`;
- timestamps.

Papéis:

- autor;
- orientador;
- coorientador;
- avaliador;
- colaborador.

## Delimitação dos domínios

| Domínio | Pergunta respondida |
| --- | --- |
| `ResearchProject` | Qual pesquisa formal está sendo ou foi executada? |
| `AcademicWork` | Qual trabalho acadêmico foi apresentado e por quem? |
| `ScientificOutput` | Qual resultado científico foi publicado? |
| `portfolio.Project` | Qual solução, produto, serviço ou iniciativa prática foi desenvolvida? |

Exemplo:

- Pesquisa: “Desenvolvimento de bioativo amazônico”.
- Trabalho acadêmico: “Avaliação fitoquímica da espécie X”.
- Produção científica: “Artigo com os resultados da avaliação fitoquímica”.
- Portfólio: “Protótipo de bioproduto desenvolvido a partir do bioativo”.

Um mesmo esforço pode gerar registros nos quatro domínios, ligados entre si sem duplicar sua função.

## Relações

- `ResearchProject.unit` define a responsabilidade institucional.
- `ResearchProject.axis` é opcional.
- `ResearchProjectMember.person` identifica a equipe.
- `AcademicWork.unit` define a responsabilidade institucional.
- `AcademicWork.research_project` relaciona o trabalho a uma pesquisa, quando aplicável.
- `AcademicWorkContributor.person` estrutura autoria e orientação.
- `ScientificOutput` pode se relacionar a uma pesquisa, a um trabalho ou a ambos.
- `ScientificAuthorship` ordena autores cadastrados.
- campos textuais permanecem disponíveis para autores externos.
- arquivos podem usar campos próprios ou ativos reutilizáveis do `mediahub`.

## Páginas públicas previstas

- lista e detalhe de pesquisas;
- lista e detalhe de trabalhos acadêmicos;
- filtros por unidade, status, ano, tipo e destaque;
- relações navegáveis entre pesquisa, trabalho, produção e portfólio;
- destaques na Home do LABTEC.IN;
- recorte LATEC quando houver vínculo com a unidade.

## API planejada

```txt
GET /api/v1/research-projects/
GET /api/v1/research-projects/{slug}/
GET /api/v1/academic-works/
GET /api/v1/academic-works/{slug}/
```

Exemplos:

```txt
GET /api/v1/research-projects/?unit=labtec-in
GET /api/v1/research-projects/?axis=praticas-em-laboratorio-e-nanotecnologia
GET /api/v1/academic-works/?work_type=tcc
GET /api/v1/academic-works/?year=2026
```

## Migração de registros históricos

1. Inventariar projetos nas categorias “Pesquisa” e “Produção Científica”.
2. Classificar cada registro por natureza real.
3. Criar `ResearchProject`, `AcademicWork` ou `ScientificOutput` conforme o caso.
4. Manter `portfolio.Project` somente quando houver iniciativa prática.
5. Relacionar registros derivados.
6. Validar unidade, pessoas, autoria, arquivos e datas.
7. Desativar categorias incompatíveis após o backfill.

Nenhum registro de projeto será convertido automaticamente sem validação manual.

## Validações institucionais necessárias

- lista oficial de pesquisas;
- catálogo de TCCs e outros trabalhos;
- autoria, orientação e ordem de autores;
- unidade responsável por cada registro;
- relação com os eixos da LATEC;
- direitos e disponibilidade pública dos arquivos;
- categorias e status oficiais de pesquisa.
