# Eixos de atuação — LATEC.IN

As imagens institucionais da LATEC.IN definem os eixos de atuação como parte central da identidade da liga. Portanto, os eixos não devem ser tratados apenas como texto estático: eles serão modelados como entidades do backend.

## Decisão de modelagem

Será criado o app `axes`, responsável por `ResearchAxis` e `AxisMentorship`.

`ResearchAxis` representa um eixo formal de atuação. `AxisMentorship` representa a relação entre um eixo e seus professores, orientadores ou mentores.

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

Observação: a grafia `Dayam` ou `Dayan` deve ser validada antes da carga definitiva dos dados.

## Campos mínimos de `ResearchAxis`

- `number`;
- `title`;
- `slug`;
- `description`;
- `keywords`;
- `is_active`;
- `display_order`;
- `created_at`;
- `updated_at`.

## Campos mínimos de `AxisMentorship`

- `axis`;
- `person`;
- `role`;
- `is_main_mentor`;
- `display_order`;
- `created_at`;
- `updated_at`.

## Regras de negócio

- Um eixo pode ter um ou mais mentores.
- Uma pessoa pode atuar em mais de um eixo.
- Projetos, cursos, posts e produções científicas podem ser vinculados a um eixo.
- Professores, orientadores e mentores poderão criar publicações associadas aos seus próprios eixos.
