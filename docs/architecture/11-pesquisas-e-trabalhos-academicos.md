# Pesquisas e trabalhos acadêmicos do LABTEC.IN

O LABTEC.IN é responsável institucional por pesquisas, TCCs e outros trabalhos acadêmicos publicados no portal. A LATEC pode possuir conteúdos próprios ou se relacionar com pesquisas por unidade e eixo, mas não substitui o laboratório como raiz.

## Estado implementado

O app `research` concentra o processo de pesquisa e os trabalhos acadêmicos. `scientific` mantém resultados publicados e `portfolio` mantém soluções e iniciativas práticas.

Os registros novos usam unidade obrigatória. A compatibilidade histórica permanece: projetos de portfólio originários não são removidos automaticamente e `ScientificOutput.authors` continua disponível para autoria externa.

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

`unit` é obrigatório e usa `PROTECT`. A relação com eixo é opcional. `project_status` aceita `planned`, `in_progress`, `completed`, `suspended` e `canceled`. Datas nulas são aceitas; quando ambas existem, `end_date >= start_date` é garantido por constraint.

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

Cada pessoa aparece no máximo uma vez por pesquisa.

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

`unit` é obrigatório e usa `PROTECT`. A unicidade de contribuidores é `(academic_work, person, role)`, permitindo que a mesma pessoa acumule papéis diferentes no trabalho.

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
- uma pessoa e uma ordem de autoria são únicas por produção;
- `ScientificOutput.authors` permanece disponível e pode coexistir com autores internos estruturados;
- pesquisas, trabalhos e produções usam seus campos próprios de arquivo; a integração estrutural com `mediahub` permanece futura.

## Páginas públicas

- lista e detalhe de pesquisas;
- lista e detalhe de trabalhos acadêmicos;
- filtros por unidade, status, ano, tipo e destaque;
- relações navegáveis entre pesquisa, trabalho acadêmico e produção científica;
- recorte LATEC quando houver vínculo com a unidade.

A inclusão de destaques de pesquisa na Home permanece fora desta entrega.

O portfólio legado não é exposto como relação de domínio. O identificador técnico da origem existe somente para permitir a reversão segura da conversão histórica.

## API implementada

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

Pesquisas aceitam `unit`, `axis`, `project_status`, `year`, `featured` e `search`. Trabalhos aceitam `unit`, `work_type`, `year`, `featured` e `search`. Lista e detalhe exibem somente registros simultaneamente publicados no workflow e marcados com `is_published=True`.

Pesquisa inclui eixo e equipe ordenada. Trabalho inclui pesquisa resumida e contribuidores. Produção científica inclui pesquisa, trabalho e `ScientificAuthorship`, sem serialização circular.

## Conversão de registros históricos

A migration de dados reversível aplica regras conservadoras:

- categoria `pesquisa` cria `ResearchProject`;
- categoria `producao-cientifica` cria `ScientificOutput`;
- registros sem unidade fazem a migration falhar antes da conversão;
- unidade, eixo, título, slug, resumo e status de execução são preservados quando semanticamente compatíveis;
- o líder da equipe vira coordenador e os demais integrantes viram colaboradores;
- autoria científica, metodologia, datas e instituição não são inferidas;
- o novo registro fica em rascunho;
- a origem de portfólio permanece inalterada e pública;
- um identificador interno `legacy_portfolio_project_id`, não exposto pela API ou pelo Admin, registra a proveniência;
- a reversão remove somente os registros marcados como derivados, mesmo que seus slugs tenham sido editados depois.

No conjunto inicial, `pesquisa-de-bioativos-da-amazonia` gera uma pesquisa em rascunho. Não existe produção científica histórica para converter. O projeto legado só será arquivado manualmente depois da revisão institucional e da publicação do novo registro.

## Validações institucionais necessárias

- lista oficial de pesquisas;
- catálogo de TCCs e outros trabalhos;
- autoria, orientação e ordem de autores;
- unidade responsável por cada registro;
- relação com os eixos da LATEC;
- direitos e disponibilidade pública dos arquivos;
- categorias e status oficiais de pesquisa.
