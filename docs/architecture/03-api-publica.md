# API pública — LATEC.IN

A API pública deve permitir que o frontend substitua gradualmente os arrays simulados de `js/data.js` por chamadas HTTP.

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
GET  /api/metrics/impact/
POST /api/contact/
```

## Diretriz de migração

Os primeiros serializers devem retornar campos próximos dos objetos atuais do protótipo, principalmente para membros, projetos, notícias, cursos, materiais e números de impacto. Isso reduz o esforço de adaptação do frontend.
