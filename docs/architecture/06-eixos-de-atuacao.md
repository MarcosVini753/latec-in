# Eixos de atuação da LATEC

A LATEC é uma unidade filha apoiada pelo LABTEC.IN. Seus sete eixos organizam prioritariamente mentorias e atividades próprias da Liga; eles não representam a estrutura global do laboratório.

## Estado implementado

O app `axes` já possui `ResearchAxis` e `AxisMentorship`, com sete eixos e nove vínculos de mentoria carregados pelo seed atual.

Os eixos ainda não possuem `unit`. A associação institucional à LATEC existe apenas de forma implícita no conteúdo histórico.

## Arquitetura alvo

`ResearchAxis` terá vínculo obrigatório com `institutional.InstitutionalUnit`. Os sete registros existentes receberão a unidade `latec`.

`AxisMentorship` continuará representando a relação entre eixo e pessoa. O papel institucional geral da pessoa será representado separadamente por `InstitutionMembership`.

## Eixos iniciais

### Eixo 1 — Etnobotânica e Pós-Colheita

Cultivo, manejo e óleos essenciais.

Mentoria inicial: Profa. Almecina.

### Eixo 2 — Práticas em Laboratório e Nanotecnologia

Farmácia Viva, farmacologia aplicada a plantas medicinais e fitoquímica.

Mentoria inicial: Profa. Marta.

### Eixo 3 — Nutrição e Ciências dos Alimentos

Educação alimentar, desenvolvimento e avaliação de alimentos, interface clínica e eventos científicos.

Mentoria inicial: Profa. Bruna.

### Eixo 4 — Saúde e bem-estar

Produção de ativos para aplicação em saúde integrativa.

Mentoria inicial: Prof. Kleyton.

### Eixo 5 — Produção Vegetal e Biotecnologia

Produção vegetal, biotecnologia de plantas, fitotecnia, genética vegetal, horticultura, manejo de culturas e PANCs.

Mentoria inicial: Profa. Marilene e Prof. Bruno.

### Eixo 6 — Agroindustrialização

Desenvolvimento de produtos, processamento de matérias-primas amazônicas e inovação tecnológica.

Mentoria inicial: Profa. Luciana.

### Eixo 7 — Redação Científica

Produção acadêmica, escrita de artigos, resumos, projetos e revisão de literatura.

Mentoria inicial: Prof. Dayam/Dayan e Profa. Anne.

A grafia `Dayam` ou `Dayan` ainda exige validação institucional antes da carga definitiva.

## Campos de `ResearchAxis`

- `unit`;
- `number`;
- `title`;
- `slug`;
- `description`;
- `keywords`;
- `is_active`;
- `display_order`;
- `created_at`;
- `updated_at`.

## Campos de `AxisMentorship`

- `axis`;
- `person`;
- `role`;
- `is_main_mentor`;
- `display_order`;
- `created_at`;
- `updated_at`.

## Regras de negócio

- Cada eixo pertence à LATEC.
- Um eixo pode ter um ou mais mentores.
- Uma pessoa pode atuar em mais de um eixo.
- Projetos, cursos, posts, eventos e produções específicas da LATEC podem usar eixo.
- Uma pesquisa do LABTEC.IN pode se relacionar opcionalmente com um eixo.
- Conteúdo geral do laboratório não precisa de eixo.
- O acesso editorial de mentores combina unidade autorizada e vínculo com eixo.

## Migração

1. Criar a unidade LATEC como filha do LABTEC.IN.
2. Adicionar `unit` opcional a `ResearchAxis`.
3. Associar os sete eixos existentes à LATEC.
4. Atualizar consultas, serializers, filtros e permissões.
5. Tornar `unit` obrigatório.

Nenhum eixo deve ser reclassificado para o LABTEC.IN sem validação institucional.
