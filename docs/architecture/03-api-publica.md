# API pública — LATEC.IN

A API pública deve permitir que o frontend substitua gradualmente os arrays simulados de `js/data.js` por chamadas HTTP.

## Diretrizes

- Usar Django REST Framework.
- Expor somente conteúdos publicados e ativos.
- Usar `slug` em páginas públicas.
- Manter endpoints administrativos separados da API pública.
- Documentar a API com OpenAPI.
- Preservar, quando possível, campos próximos aos objetos atuais do protótipo para reduzir retrabalho no frontend.

## Endpoints iniciais previstos

```txt
GET  /api/site/settings/
GET  /api/site/home/

GET  /api/people/
GET  /api/people/{slug}/

GET  /api/projects/
GET  /api/projects/{slug}/
GET  /api/projects/categories/

GET  /api/posts/
GET  /api/posts/{slug}/
GET  /api/posts/tags/

GET  /api/courses/
GET  /api/courses/{slug}/

GET  /api/partners/
GET  /api/metrics/impact/

POST /api/contact/
```

## Filtros públicos previstos

### Projetos

- categoria;
- status;
- ano;
- área;
- destaque;
- busca textual.

### Posts

- categoria;
- tag;
- data;
- destaque;
- busca textual.

### Cursos

- status;
- trilha;
- data;
- destaque;
- busca textual.

## Migração do protótipo

- `members` será substituído por `/api/people/`.
- `projects` será substituído por `/api/projects/`.
- `news` será substituído por `/api/posts/`.
- `courses` será substituído por `/api/courses/`.
- `materials` será substituído por vínculos entre cursos e `mediahub`.
- `impactNumbers` será substituído por `/api/metrics/impact/`.

## Contratos mínimos de resposta

### Pessoa

```json
{
  "id": 1,
  "full_name": "Nome da pessoa",
  "slug": "nome-da-pessoa",
  "role": "Ligante",
  "short_bio": "Minicurrículo",
  "photo_url": "..."
}
```

### Projeto

```json
{
  "id": 1,
  "title": "Título do projeto",
  "slug": "titulo-do-projeto",
  "category": "Pesquisa",
  "status": "Em andamento",
  "year": 2026,
  "summary": "Resumo público"
}
```

### Post

```json
{
  "id": 1,
  "title": "Título da notícia",
  "slug": "titulo-da-noticia",
  "category": "Notícia",
  "summary": "Resumo",
  "published_at": "2026-07-01"
}
```

## Restrições

A API pública não deve expor mensagens de contato, rascunhos, dados internos de auditoria ou informações administrativas.
