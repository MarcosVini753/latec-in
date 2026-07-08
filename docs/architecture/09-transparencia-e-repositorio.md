# Transparência, repositório científico e vitrine biotecnológica

As imagens institucionais definem a plataforma web da LATEC.IN como mais do que um site institucional. A plataforma deve cumprir funções públicas específicas.

## Funções da plataforma

### Transparência

Área destinada a editais, atas, homologações, julgamentos de recursos, resultados e comunicados.

Essa área será modelada pelo app `transparency`.

### Repositório científico

Área destinada a artigos, resumos, patentes e produções vinculadas aos eixos de atuação.

Essa área será modelada pelo app `scientific`.

### Vitrine biotecnológica

Área destinada a patentes, bioprodutos, soluções e entregas de projetos ou startups parceiras.

Essa função será contemplada principalmente por `portfolio` e `scientific`.

### Difusão e extensão

Área destinada a inscrições e divulgação de simpósios, cursos, palestras e ações abertas.

Essa função será contemplada principalmente por `learning`.

## Papel da LATEC.IN

A atuação da liga será organizada em três frentes:

- Ensino: inovação regional.
- Pesquisa: propriedade intelectual.
- Extensão: impacto social.

## Entidades novas

### `ScientificOutput`

Representa produção científica vinculada a eixo, autores e arquivo ou link externo.

Campos mínimos:

- `title`;
- `slug`;
- `output_type`;
- `axis`;
- `authors`;
- `abstract`;
- `publication_date`;
- `file`;
- `external_url`;
- `status`;
- `is_published`;
- `is_featured`.

### `TransparencyDocument`

Representa documento público de transparência.

Campos mínimos:

- `title`;
- `slug`;
- `document_type`;
- `description`;
- `file`;
- `publication_date`;
- `related_process`;
- `status`;
- `is_published`.

### `Event`

Representa simpósio, curso, palestra ou ação de difusão/extensão.

Campos mínimos:

- `title`;
- `slug`;
- `event_type`;
- `description`;
- `axis`;
- `start_date`;
- `end_date`;
- `location`;
- `registration_url`;
- `status`;
- `is_published`.
