# Modelagem do banco de dados — Portal LABTEC.IN

Este documento descreve a modelagem Django implementada e os legados mantidos durante a transição.

## Convenções

- Todos os modelos de domínio usam `id`, `created_at` e `updated_at`.
- Conteúdos públicos usam `slug`, status editorial, publicação e destaque quando aplicável.
- O workflow permanece `draft`, `in_review`, `published` e `archived`.
- `InstitutionalUnit` representa propriedade institucional; não serão criados booleanos como `is_latec` ou `is_labtec_content`.
- Campos `unit` dos modelos legados permanecem opcionais para permitir backfill; os novos modelos de `research` exigem unidade.
- Relações com pessoas usam entidades intermediárias quando o papel, a ordem ou outros metadados pertencem ao vínculo.

## Estado implementado

O backend possui models nos apps `institutional`, `accounts`, `core`, `people`, `axes`, `research`, `portfolio`, `scientific`, `news`, `learning`, `transparency`, `mediahub`, `partnerships` e `metrics`.

- `InstitutionalUnit` e `InstitutionMembership` possuem constraints e validações de integridade;
- `Profile` possui unidade principal, unidades autorizadas e herança opcional de descendentes;
- os sete eixos pertencem à LATEC;
- `ResearchProject` e `AcademicWork` modelam pesquisas e trabalhos acadêmicos;
- `ScientificOutput` pode apontar para ambos e possui autoria interna ordenada, mantendo `authors` para autores externos;
- conteúdos existentes possuem `unit` opcional, e `Partner` possui relação muitos-para-muitos com unidades;
- `Person.role`, categorias de portfólio e tipos científicos antigos permanecem por compatibilidade;
- `Event` continua sem endpoint público nesta entrega.

## `institutional`

App responsável pela estrutura organizacional.

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

`parent` não pode apontar para o próprio registro. `clean()` percorre os ancestrais e rejeita ciclos indiretos, e `save()` executa a validação também em gravações ORM usuais. O manager bloqueia inserções hierárquicas por `bulk_create()` e alterações de pai por `bulk_update()`. `QuerySet.update()` permanece como o único caminho ORM capaz de contornar a validação; ele deve ser reservado a migrations controladas e operações que preservem explicitamente a hierarquia.

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

Quando uma pessoa exerce mais de um papel simultâneo na mesma unidade, cada papel é registrado em um membership próprio.

A combinação `(person, unit, role)` é única. Datas nulas são aceitas; quando ambas existem, `end_date` deve ser maior ou igual a `start_date`. As duas regras existem como constraints de banco e como validação amigável no modelo. A migration que as antecede executa preflight e interrompe a aplicação com os IDs conflitantes, sem excluir ou corrigir dados automaticamente.

## `core`

### Estado implementado

- `SiteSettings` usa LABTEC.IN como padrão e possui unidade opcional.
- `HeroBanner`, `InstitutionalSection` e `SocialLink` possuem unidade opcional.
- O seed associa `SiteSettings`, o hero principal e as seções iniciais ao LABTEC.IN.

### Regras implementadas

- `SiteSettings` representa o portal LABTEC.IN e se vincula à unidade raiz.
- Nome padrão do site: `LABTEC.IN`.
- `HeroBanner`, `InstitutionalSection` e `SocialLink` possuem `unit` opcional.
- A Home principal consulta exclusivamente conteúdo da unidade `labtec-in`.
- A seção LATEC consulta conteúdo da unidade `latec`.

## `people`

### Estado implementado

`Person` representa a pessoa física e possui uma relação opcional com `Role`, tratada hoje como papel público único.

### Transição

`Person` continua independente de autenticação e unidade. O campo atual `role` é legado; papéis institucionais são expressos por `InstitutionMembership`.

O seed e o backfill criam os memberships conhecidos sem remover `Person.role`. A descontinuação e remoção do campo ocorrerão somente depois que consultas e interfaces deixarem de consumi-lo.

## `accounts`

O sistema usa `User` padrão do Django e `Profile` com os papéis `admin`, `lab_coordinator`, `unit_coordinator`, `mentor`, `editor` e `reader`.

O perfil administrativo representa:

- `primary_unit`, opcional;
- `authorized_units`, relação muitos-para-muitos opcional;
- `inherit_descendants`, desabilitado por padrão;
- vínculo opcional com `people.Person`;
- estado ativo do acesso administrativo.

Superusuários permanecem irrestritos. Perfis inativos ou sem unidade autorizada não recebem acesso institucional. A coordenação do LABTEC.IN acessa a raiz, descendentes e conteúdo sem unidade; os demais papéis são limitados às unidades ou eixos autorizados. Apenas administrador e coordenação do LABTEC.IN realizam publicação final.

## `axes`

`ResearchAxis` e `AxisMentorship` estão implementados. `ResearchAxis.unit` permanece opcional durante a transição, e os sete registros iniciais pertencem explicitamente à LATEC.

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

App responsável por pesquisas formais e trabalhos acadêmicos subsidiados ou mantidos pelo LABTEC.IN.

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

Uma pesquisa exige unidade com proteção contra exclusão da unidade referenciada. O eixo é opcional. Datas nulas são aceitas; quando ambas existem, `end_date` deve ser maior ou igual a `start_date`.

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

Uma pessoa aparece no máximo uma vez em cada pesquisa.

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

Um mesmo papel de uma pessoa aparece no máximo uma vez em cada trabalho. `AcademicWork.unit` também é obrigatório e protegido.

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

`Project` possui `unit` opcional. Projetos podem pertencer ao LABTEC.IN ou à LATEC.

Pesquisa e produção científica deixam de ser responsabilidades centrais do portfólio. As categorias históricas “Pesquisa” e “Produção Científica” podem permanecer temporariamente por compatibilidade, mas seus registros devem ser revisados e migrados para os domínios corretos.

### `scientific`

`ScientificOutput` possui:

- `unit`;
- `axis`, que permanece opcional;
- relação opcional com `ResearchProject`;
- relação opcional com `AcademicWork`;
- autoria estruturada;
- campo textual para autores externos não cadastrados.

Os tipos principais representam artigo, resumo, patente, e-book, livro e relatório. As opções históricas `project` e `scientific_production` permanecem temporariamente para compatibilidade.

#### `ScientificAuthorship`

Campos:

- `scientific_output`;
- `person`;
- `author_order`;
- `author_role`;
- timestamps.

Cada pessoa e cada posição de autoria são únicas por produção. O campo textual `authors` continua disponível para nomes externos não cadastrados.

### `news`

`Post` possui `unit` opcional.

- notícias gerais: LABTEC.IN;
- notícias específicas da Liga: LATEC;
- `axis` permanece opcional;
- autores continuam vinculáveis.

### `learning`

`Course`, `LearningTrack` e `Event` possuem `unit` opcional. Materiais herdam o escopo do curso.

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

`TransparencyDocument` possui `unit` opcional.

O padrão é LABTEC.IN, com suporte a documentos específicos da LATEC e de futuras unidades.

### `mediahub`

`MediaAsset` possui unidade proprietária opcional.

Um arquivo pode pertencer ao LABTEC.IN, à LATEC ou permanecer sem unidade em casos técnicos. Nesta etapa, os demais domínios ainda não possuem relação estrutural com `MediaAsset`.

### `partnerships`

`Partner` se relaciona com uma ou mais unidades. Uma parceria pode ser institucional do LABTEC.IN, específica da LATEC ou compartilhada.

`ContactMessage` permanece sem exposição pública e sob acesso funcional da coordenação do LABTEC.IN.

### `metrics`

`ImpactMetric` possui `unit` opcional e os campos atuais de chave, rótulo, valor, sufixo, descrição, ativação e ordem. `MetricSnapshot` herda o escopo da métrica.

Métricas do LABTEC.IN podem incluir pesquisas, trabalhos acadêmicos, pesquisadores, produções, projetos, cursos, eventos, parcerias e iniciativas apoiadas.

Métricas da LATEC podem incluir ligantes, mentores, eixos, projetos, cursos e publicações específicos.

`MetricSnapshot` continua registrando valores históricos da métrica.

## Relacionamentos principais

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
- `Project`, `Post`, `Course`, `LearningTrack`, `Event`, `TransparencyDocument`, `MediaAsset` e `ImpactMetric` podem pertencer a uma unidade durante a transição.
- `Partner` pode se relacionar com várias unidades.
- `MediaAsset` pode ter unidade opcional; sua reutilização por outros domínios ainda não é representada por relações no banco.

## Compatibilidade e próximos cortes

- `Person.role`, projetos de categorias históricas, `ScientificOutput.authors` e tipos científicos legados não foram removidos.
- A conversão histórica cria registros novos em rascunho e mantém a origem de portfólio inalterada.
- Pesquisas e produções derivadas guardam `legacy_portfolio_project_id` apenas como proveniência técnica para rollback seguro; o campo não integra a API nem o Admin.
- Campos institucionais legados só serão tornados obrigatórios depois do inventário e backfill completos.

As migrations são incrementais e reversíveis quando envolvem conversão de dados. O plano operacional está em [Migração para a arquitetura LABTEC.IN](12-migracao-labtec.md).
