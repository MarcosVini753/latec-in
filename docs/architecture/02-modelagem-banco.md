# Modelagem inicial do banco de dados — LATEC.IN

Este documento registra a modelagem inicial do backend Django. A modelagem ainda é conceitual e deve evoluir junto com as migrations.

## Convenções gerais

Todos os modelos devem possuir `id`, `created_at` e `updated_at`.

Conteúdos públicos devem possuir `is_published`. Conteúdos com página própria devem possuir `slug`. Entidades editoriais devem possuir status, data de publicação e possibilidade de destaque na Home quando fizer sentido.

O workflow editorial inicial será: `draft`, `in_review`, `published` e `archived`.

## Apps considerados

- `accounts`: usuários administrativos, perfis e auditoria.
- `core`: configurações institucionais, hero, seções da Home e links sociais.
- `people`: membros, professores, ligantes, pesquisadores e linhas de atuação.
- `axes`: eixos de atuação e mentorias.
- `portfolio`: projetos, categorias, resultados, links, equipe e anexos.
- `scientific`: repositório científico, artigos, resumos, patentes e produções vinculadas aos eixos.
- `news`: notícias, blog, editais editoriais, jornal e tags.
- `learning`: cursos, trilhas, workshops, materiais, eventos e instrutores.
- `transparency`: editais, atas, homologações, julgamentos de recursos e comunicados.
- `mediahub`: imagens, documentos, PDFs e arquivos reutilizáveis.
- `partnerships`: parceiros e mensagens de contato.
- `metrics`: números de impacto da Home.

## Entidades por módulo

### `accounts`

- `Profile`: complementa o usuário padrão do Django e pode se vincular opcionalmente a uma pessoa pública.
- `AuditLog`: registra ações administrativas relevantes em fase posterior.

Campos mínimos de `Profile`: `user`, `person`, `role`, `is_active_admin`.

### `core`

- `SiteSettings`: nome do site, descrição, instituição, e-mail de contato, logo e configurações globais.
- `HeroBanner`: título, subtítulo, CTA, imagem e ordem de exibição do hero.
- `InstitutionalSection`: missão, visão, valores, histórico e propósito.
- `SocialLink`: links sociais e canais oficiais.

### `people`

- `Person`: pessoa exibida publicamente no site.
- `Role`: função pública da pessoa, como coordenadora, professor, ligante, pesquisador, estagiário, colaborador ou egresso.

Campos mínimos de `Person`: nome completo, slug, função, minicurrículo, foto, links opcionais, ativo, destaque e ordem de exibição.

### `axes`

- `ResearchAxis`: eixo formal de atuação da LATEC.IN.
- `AxisMentorship`: vínculo entre eixo e professor, orientador ou mentor.

Campos mínimos de `ResearchAxis`: número, título, slug, descrição, palavras-chave, ativo e ordem de exibição.

Campos mínimos de `AxisMentorship`: eixo, pessoa, papel no eixo, mentor principal e ordem de exibição.

Eixos iniciais:

1. Etnobotânica e Pós-Colheita.
2. Práticas em Laboratório e Nanotecnologia.
3. Nutrição e Ciências dos Alimentos.
4. Saúde e bem-estar.
5. Produção Vegetal e Biotecnologia.
6. Agroindustrialização.
7. Redação Científica.

### `portfolio`

- `Project`: entidade central do portfólio.
- `ProjectCategory`: Ensino, Pesquisa, Extensão, Produção Científica, Startup e Premiação.
- `ProjectStatus`: Planejado, Em andamento, Concluído e Arquivado.
- `ProjectTeamMember`: relacionamento entre projeto e pessoa, com papel no projeto.
- `ProjectResult`: entregas, produtos e resultados.
- `ProjectLink`: links externos, repositórios, publicações ou aplicações.

Campos mínimos de `Project`: título, slug, eixo, categoria, área, status, ano, resumo, problema, solução, imagem de capa, publicado, destaque e ordem.

### `scientific`

- `ScientificOutput`: artigo, resumo, patente, e-book, livro, relatório técnico, projeto ou produção científica.

Campos mínimos de `ScientificOutput`: título, slug, tipo, eixo, autores, resumo, data de publicação, arquivo, URL externa, status, publicado e destaque.

### `news`

- `Post`: notícia, blog, jornal, evento, premiação, artigo técnico ou comunicado editorial.
- `PostCategory`: categoria editorial.
- `Tag`: classificação adicional para busca e filtros.

Campos mínimos de `Post`: título, slug, eixo opcional, categoria, resumo, conteúdo, imagem de capa, status, data de publicação, publicado e destaque.

### `learning`

- `Course`: curso, workshop, bootcamp ou capacitação.
- `LearningTrack`: trilha de aprendizagem.
- `CourseMaterial`: material vinculado a curso.
- `Event`: simpósio, palestra ou ação de difusão/extensão.

Campos mínimos de `Course`: título, slug, eixo opcional, descrição, datas, carga horária, status, link de inscrição, imagem de capa, publicado e destaque.

Campos mínimos de `Event`: título, slug, tipo, eixo opcional, descrição, datas, local, link de inscrição, status e publicado.

### `transparency`

- `TransparencyDocument`: edital, ata, homologação, julgamento de recurso, resultado ou comunicado.

Campos mínimos: título, slug, tipo, descrição, arquivo, data de publicação, processo relacionado, status e publicado.

### `mediahub`

- `MediaAsset`: ativo reutilizável, como imagem, PDF, e-book, livro, documento técnico ou certificado.

Campos mínimos: título, descrição, arquivo, tipo, texto alternativo, crédito, visibilidade e responsável pelo upload.

### `partnerships`

- `Partner`: parceiro institucional.
- `ContactMessage`: mensagem recebida pelo formulário público.

Campos mínimos de `Partner`: nome, slug, tipo, descrição, logotipo, site, ativo e ordem.

Campos mínimos de `ContactMessage`: assunto, nome, e-mail, organização opcional, mensagem, status e datas de criação/resposta.

As mensagens de contato serão retidas por tempo indeterminado na fase inicial e acessadas apenas pela coordenação.

### `metrics`

- `ImpactMetric`: métrica exibida na Home.
- `MetricSnapshot`: histórico opcional de métricas.

Métricas iniciais: membros, projetos, artigos/publicações, parcerias, cursos, eventos e premiações.

## Relacionamentos principais

- `Person` pode ser mentor de vários `ResearchAxis` por meio de `AxisMentorship`.
- `ResearchAxis` se relaciona com projetos, posts, cursos, eventos e produções científicas.
- `Person` participa de vários `Project` por meio de `ProjectTeamMember`.
- `Person` pode ser autor de vários `Post` e `ScientificOutput`.
- `Person` pode ser instrutor de vários `Course`.
- `Project` possui vários resultados, links e anexos.
- `Course` pode possuir materiais e instrutores.
- `MediaAsset` pode ser reutilizado por projetos, posts, produções científicas, cursos e transparência.
- `Partner` pode aparecer publicamente e futuramente se vincular a projetos.

## Ordem sugerida de implementação

1. `core`, `people`, `axes` e `mediahub`.
2. `portfolio`.
3. `scientific`.
4. `news`.
5. `learning`.
6. `transparency`.
7. `partnerships`.
8. `metrics`.
9. ajustes finais de `accounts` e permissões.
