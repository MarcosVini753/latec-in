# Modelagem do banco de dados — Portal LABTEC.IN

Este documento descreve o estado implementado, a arquitetura alvo e a sequência de migração da modelagem Django.

## Convenções

- Todos os modelos de domínio usam `id`, `created_at` e `updated_at`.
- Conteúdos públicos usam `slug`, status editorial, publicação e destaque quando aplicável.
- O workflow permanece `draft`, `in_review`, `published` e `archived`.
- `InstitutionalUnit` representa propriedade institucional; não serão criados booleanos como `is_latec` ou `is_labtec_content`.
- Campos `unit` serão inicialmente opcionais para permitir backfill e se tornarão obrigatórios onde fizer sentido.
- Relações com pessoas usam entidades intermediárias quando o papel, a ordem ou outros metadados pertencem ao vínculo.

## Estado implementado

O backend atual possui models nos apps `institutional`, `accounts`, `core`, `people`, `axes`, `portfolio`, `scientific`, `news`, `learning`, `transparency`, `mediahub`, `partnerships` e `metrics`.

Situação após a primeira fase:

- `InstitutionalUnit` e `InstitutionMembership` estão implementados;
- `SiteSettings.site_name` usa `LABTEC.IN` como padrão;
- `SiteSettings`, `HeroBanner`, `InstitutionalSection` e `SocialLink` possuem `unit` opcional;
- o seed cria LABTEC.IN e LATEC e associa os conteúdos centrais conhecidos ao laboratório;
- memberships ainda não foram preenchidos;

As incompatibilidades restantes são:

- `Person` possui um único `role`;
- `Profile` não possui escopo por unidade;
- os sete eixos não possuem unidade proprietária;
- não existem models próprios para pesquisas e trabalhos acadêmicos;
- projetos, posts, cursos, eventos, produções científicas, transparência, parceiros, mídia e métricas não possuem vínculo institucional;
- autoria científica é apenas textual;
- pesquisas e produção científica ainda aparecem como categorias de portfólio;
- o model `Event` existe, mas ainda não é exposto na API pública.

## `institutional`

Novo app responsável pela estrutura organizacional.

### `InstitutionalUnit`

Representa LABTEC.IN, LATEC e futuras unidades.

Campos conceituais:

- `id`;
- `name`;
- `acronym`;
- `slug`;
- `unit_type`;
- `parent`, autorrelacionamento opcional;
- `description`;
- `mission`;
- `vision`;
- `logo`;
- `cover_image`;
- `contact_email`;
- `website_url`;
- `is_active`;
- `is_public`;
- `display_order`;
- `created_at`;
- `updated_at`.

Tipos iniciais:

- `laboratory`;
- `academic_league`;
- `program`;
- `research_group`;
- `initiative`.

Unidades iniciais:

- LABTEC.IN: `laboratory`, sem unidade pai e raiz do portal;
- LATEC: `academic_league`, filha do LABTEC.IN.

### `InstitutionMembership`

Representa a participação de uma pessoa em uma unidade.

Campos conceituais:

- `person`;
- `unit`;
- `role`;
- `start_date`;
- `end_date`;
- `is_active`;
- `is_public`;
- `display_order`;
- `created_at`;
- `updated_at`.

Uma mesma pessoa pode possuir vários vínculos. Exemplo:

- Marta Adelino no LABTEC.IN: coordenadora e pesquisadora;
- Marta Adelino na LATEC: coordenadora e mentora de eixo.

Quando uma pessoa exercer mais de um papel simultâneo na mesma unidade, cada papel será registrado em um membership próprio.

## `core`

### Estado implementado

- `SiteSettings` usa LABTEC.IN como padrão e possui unidade opcional.
- `HeroBanner`, `InstitutionalSection` e `SocialLink` possuem unidade opcional.
- O seed associa `SiteSettings`, o hero principal e as seções iniciais ao LABTEC.IN.

### Arquitetura alvo

- `SiteSettings` representa o portal LABTEC.IN e se vincula à unidade raiz.
- Nome padrão do site: `LABTEC.IN`.
- `HeroBanner`, `InstitutionalSection` e `SocialLink` recebem `unit`.
- A Home principal consulta conteúdo da unidade `labtec-in`.
- A seção LATEC consulta conteúdo da unidade `latec`.

## `people`

### Estado implementado

`Person` representa a pessoa física e possui uma relação opcional com `Role`, tratada hoje como papel público único.

### Arquitetura alvo

`Person` continua independente de autenticação e unidade. O campo atual `role` será legado; papéis institucionais serão expressos por `InstitutionMembership`.

Migração:

1. manter `Person.role` temporariamente;
2. criar memberships equivalentes;
3. atualizar consultas, serializers e interfaces;
4. descontinuar o campo;
5. removê-lo em migration posterior.

## `accounts`

### Estado implementado

O sistema usa `User` padrão do Django e `Profile` com os papéis `admin`, `coordinator`, `mentor`, `editor` e `reader`.

### Arquitetura alvo

Papéis conceituais:

- administrador;
- coordenador do laboratório;
- coordenador de unidade;
- mentor/professor.

O perfil administrativo deverá representar:

- unidade principal;
- unidades autorizadas;
- possibilidade de acesso a unidades descendentes;
- vínculo opcional com `people.Person`;
- estado ativo do acesso administrativo.

A coordenação do LABTEC.IN poderá acessar a unidade raiz e suas descendentes. Coordenadores de unidade e mentores/professores serão limitados às unidades e aos eixos autorizados.

Os papéis implementados `editor` e `reader` são legados da modelagem anterior. Na migração, cada conta deverá ser reclassificada em um dos papéis alvo ou desativada quando não houver necessidade administrativa.

## `axes`

### Estado implementado

`ResearchAxis` e `AxisMentorship` já existem. Os sete eixos não possuem vínculo institucional.

### Arquitetura alvo

`ResearchAxis` recebe vínculo obrigatório com `InstitutionalUnit` após o backfill. Os sete registros existentes pertencem à LATEC.

Campos de `ResearchAxis`:

- `unit`;
- `number`;
- `title`;
- `slug`;
- `description`;
- `keywords`;
- `is_active`;
- `display_order`;
- timestamps.

`AxisMentorship` continua relacionando eixo e pessoa, com papel, indicação de mentor principal e ordem. A unidade é inferida pelo eixo.

## `research`

Novo app responsável por pesquisas formais e trabalhos acadêmicos subsidiados ou mantidos pelo LABTEC.IN.

### `ResearchProject`

Representa uma pesquisa científica formal.

Campos conceituais:

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

Uma pesquisa normalmente pertence ao LABTEC.IN. O eixo é opcional e só indica relação com um eixo da LATEC.

### `ResearchProjectMember`

Representa participantes da pesquisa.

Campos:

- `research_project`;
- `person`;
- `role`;
- `is_coordinator`;
- `display_order`;
- timestamps.

Papéis iniciais:

- coordenador;
- pesquisador;
- orientador;
- bolsista;
- voluntário;
- colaborador.

### `AcademicWork`

Representa TCCs e outros trabalhos acadêmicos.

Campos conceituais:

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

Tipos iniciais:

- `tcc`;
- `monograph`;
- `scientific_initiation`;
- `dissertation`;
- `thesis`;
- `other`.

### `AcademicWorkContributor`

Representa autores, orientadores e outros participantes.

Campos:

- `academic_work`;
- `person`;
- `role`;
- `display_order`;
- timestamps.

Papéis iniciais:

- autor;
- orientador;
- coorientador;
- avaliador;
- colaborador.

## Delimitação entre pesquisa, trabalho, produção e portfólio

| Entidade | Uso |
| --- | --- |
| `research.ResearchProject` | Pesquisa científica formal, com objetivos, metodologia, equipe e período. |
| `research.AcademicWork` | TCC, monografia, iniciação científica, dissertação, tese ou outro trabalho acadêmico. |
| `scientific.ScientificOutput` | Resultado científico publicado, como artigo, resumo, patente, livro, e-book ou relatório. |
| `portfolio.Project` | Iniciativa prática, extensão, produto, serviço, startup, solução tecnológica ou projeto de inovação. |

Exemplo integrado:

- Pesquisa: “Desenvolvimento de bioativo amazônico”.
- Trabalho acadêmico: “Avaliação fitoquímica da espécie X”.
- Produção científica: “Artigo com os resultados da avaliação fitoquímica”.
- Portfólio: “Protótipo de bioproduto desenvolvido a partir do bioativo”.

## Ajustes nos módulos existentes

### `portfolio`

`Project` recebe `unit`. Projetos podem pertencer ao LABTEC.IN ou à LATEC.

Pesquisa e produção científica deixam de ser responsabilidades centrais do portfólio. As categorias históricas “Pesquisa” e “Produção Científica” podem permanecer temporariamente por compatibilidade, mas seus registros devem ser revisados e migrados para os domínios corretos.

### `scientific`

`ScientificOutput` recebe:

- `unit`;
- `axis`, que permanece opcional;
- relação opcional com `ResearchProject`;
- relação opcional com `AcademicWork`;
- autoria estruturada;
- campo textual para autores externos não cadastrados.

Os tipos alvo representam resultados publicados, como artigo, resumo, patente, e-book, livro e relatório. As opções históricas genéricas `project` e `scientific_production` deverão ser revisadas durante a migração.

#### `ScientificAuthorship`

Campos:

- `scientific_output`;
- `person`;
- `author_order`;
- `author_role`;
- timestamps.

### `news`

`Post` recebe `unit`.

- notícias gerais: LABTEC.IN;
- notícias específicas da Liga: LATEC;
- `axis` permanece opcional;
- autores continuam vinculáveis.

### `learning`

`Course`, `LearningTrack`, `Event` e, quando aplicável, `CourseMaterial` recebem `unit`.

`Event` representa simpósios, palestras, cursos abertos, inaugurações, visitas institucionais, divulgação e extensão.

Campos conceituais de `Event`:

- `title`;
- `slug`;
- `unit`;
- `event_type`;
- `description`;
- `start_date`;
- `end_date`;
- `location`;
- `cover_image`;
- `registration_url`;
- `event_status`;
- `editorial_status`;
- `is_published`;
- `published_at`;
- `is_featured`;
- timestamps.

O evento possui somente informações gerais. Não haverá entidade, CRUD, endpoint ou seed para detalhamento interno por horário.

### `transparency`

`TransparencyDocument` recebe `unit`.

O padrão é LABTEC.IN, com suporte a documentos específicos da LATEC e de futuras unidades.

### `mediahub`

`MediaAsset` recebe unidade proprietária opcional.

Um arquivo pode pertencer ao LABTEC.IN, à LATEC, ser reutilizado por vários conteúdos ou permanecer sem unidade em casos técnicos.

### `partnerships`

`Partner` passa a se relacionar com uma ou mais unidades. Uma parceria pode ser institucional do LABTEC.IN, específica da LATEC ou compartilhada.

`ContactMessage` permanece sem exposição pública e sob acesso funcional da coordenação do LABTEC.IN.

### `metrics`

`ImpactMetric` recebe:

- `unit`;
- `aggregation_mode`;
- demais campos atuais de chave, rótulo, valor, sufixo, descrição, ativação e ordem.

O modo de agregação distinguirá, no mínimo, valor direto da unidade e valor que inclui descendentes.

Métricas do LABTEC.IN podem incluir pesquisas, trabalhos acadêmicos, pesquisadores, produções, projetos, cursos, eventos, parcerias e iniciativas apoiadas.

Métricas da LATEC podem incluir ligantes, mentores, eixos, projetos, cursos e publicações específicos.

`MetricSnapshot` continua registrando valores históricos da métrica.

## Relacionamentos principais da arquitetura alvo

- `InstitutionalUnit` possui autorrelacionamento pai/filho.
- `Person` participa de unidades por `InstitutionMembership`.
- `InstitutionalUnit` possui conteúdos em todos os domínios aplicáveis.
- LATEC possui os sete `ResearchAxis`.
- `ResearchProject` pertence a uma unidade e pode se relacionar com um eixo.
- `ResearchProjectMember` relaciona pesquisa e pessoa.
- `AcademicWork` pertence a uma unidade e pode se relacionar com uma pesquisa.
- `AcademicWorkContributor` relaciona trabalho e pessoa.
- `ScientificOutput` pode derivar de pesquisa ou trabalho acadêmico.
- `ScientificAuthorship` ordena autores cadastrados.
- `Project`, `Post`, `Course`, `Event`, `TransparencyDocument` e `ImpactMetric` pertencem a uma unidade.
- `Partner` pode se relacionar com várias unidades.
- `MediaAsset` pode ter unidade opcional e ser reutilizado.

## Ordem sugerida de implementação

1. `institutional`.
2. ajustes em `people` e `accounts`.
3. `core`.
4. `axes`.
5. `research`.
6. ajustes em `portfolio` e `scientific`.
7. ajustes em `news`, `learning` e `transparency`.
8. `partnerships`, `mediahub` e `metrics`.
9. permissões, backfill final e retirada de campos legados.

As migrations deverão ser pequenas, separadas e reversíveis sempre que possível. O plano operacional está em [Migração para a arquitetura LABTEC.IN](12-migracao-labtec.md).
