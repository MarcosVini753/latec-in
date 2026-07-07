# Modelagem inicial do banco de dados — LATEC.IN

Este documento registra a modelagem inicial do backend Django. A modelagem ainda é conceitual e deve evoluir junto com as migrations.

## Convenções gerais

Todos os modelos devem possuir `id`, `created_at` e `updated_at`.

Conteúdos públicos devem possuir `is_published`. Conteúdos com página própria devem possuir `slug`. Entidades editoriais devem possuir status, data de publicação e possibilidade de destaque na Home quando fizer sentido.

## Apps considerados

- `accounts`: usuários administrativos, perfis e auditoria.
- `core`: configurações institucionais, hero, seções da Home e links sociais.
- `people`: membros, professores, ligantes, pesquisadores e linhas de atuação.
- `portfolio`: projetos, categorias, resultados, links, equipe e anexos.
- `news`: notícias, blog, editais, jornal e tags.
- `learning`: cursos, trilhas, workshops, materiais e instrutores.
- `mediahub`: imagens, documentos, PDFs e arquivos reutilizáveis.
- `partnerships`: parceiros e mensagens de contato.
- `metrics`: números de impacto da Home.

## Entidades por módulo

### `accounts`

- `Profile`: complementa o usuário do Django e pode se vincular opcionalmente a uma pessoa pública.
- `AuditLog`: registra ações administrativas relevantes em fase posterior.

### `core`

- `SiteSettings`: nome do site, descrição, instituição, e-mail de contato, logo e configurações globais.
- `HeroBanner`: título, subtítulo, CTA, imagem e ordem de exibição do hero.
- `InstitutionalSection`: missão, visão, valores, histórico e propósito.
- `SocialLink`: links sociais e canais oficiais.

### `people`

- `Person`: pessoa exibida publicamente no site.
- `Role`: função pública da pessoa, como coordenadora, professor, ligante ou pesquisador.
- `ResearchLine`: linha de atuação ou pesquisa.

Campos mínimos de `Person`: nome completo, slug, função, minicurrículo, foto, links opcionais, ativo, destaque e ordem de exibição.

### `portfolio`

- `Project`: entidade central do portfólio.
- `ProjectCategory`: Ensino, Pesquisa, Extensão, Produção Científica, Startup e Premiação.
- `ProjectStatus`: Planejado, Em andamento, Concluído e Arquivado.
- `ProjectTeamMember`: relacionamento entre projeto e pessoa, com papel no projeto.
- `ProjectResult`: entregas, produtos e resultados.
- `ProjectLink`: links externos, repositórios, publicações ou aplicações.

Campos mínimos de `Project`: título, slug, categoria, área, status, ano, resumo, problema, solução, imagem de capa, publicado, destaque e ordem.

### `news`

- `Post`: notícia, edital, blog, jornal, evento, premiação ou artigo técnico.
- `PostCategory`: categoria editorial.
- `Tag`: classificação adicional para busca e filtros.

Campos mínimos de `Post`: título, slug, categoria, resumo, conteúdo, imagem de capa, status, data de publicação, publicado e destaque.

### `learning`

- `Course`: curso, workshop, bootcamp ou capacitação.
- `LearningTrack`: trilha de aprendizagem.
- `CourseMaterial`: material vinculado a curso.

Campos mínimos de `Course`: título, slug, descrição, datas, carga horária, status, link de inscrição, imagem de capa, publicado e destaque.

### `mediahub`

- `MediaAsset`: ativo reutilizável, como imagem, PDF, e-book, livro, documento técnico ou certificado.

Campos mínimos: título, descrição, arquivo, tipo, texto alternativo, crédito, visibilidade e responsável pelo upload.

### `partnerships`

- `Partner`: parceiro institucional.
- `ContactMessage`: mensagem recebida pelo formulário público.

Campos mínimos de `Partner`: nome, slug, tipo, descrição, logotipo, site, ativo e ordem.

Campos mínimos de `ContactMessage`: assunto, nome, e-mail, organização opcional, mensagem, status e datas de criação/resposta.

### `metrics`

- `ImpactMetric`: métrica exibida na Home.
- `MetricSnapshot`: histórico opcional de métricas.

Métricas iniciais: membros, projetos, artigos/publicações, parcerias, cursos e premiações.

## Relacionamentos principais

- `Person` participa de vários `Project` por meio de `ProjectTeamMember`.
- `Person` pode ser autor de vários `Post`.
- `Person` pode ser instrutor de vários `Course`.
- `Project` possui vários resultados, links e anexos.
- `Post` possui categoria e tags.
- `Course` pode possuir materiais e instrutores.
- `MediaAsset` pode ser reutilizado por projetos, posts, cursos e seções institucionais.
- `Partner` pode aparecer publicamente e futuramente se vincular a projetos.

## Ordem sugerida de implementação

1. `core`, `people` e `mediahub`.
2. `portfolio`.
3. `news`.
4. `learning`.
5. `partnerships`.
6. `metrics`.
7. ajustes finais de `accounts` e permissões.
