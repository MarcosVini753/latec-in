# API pública — LATEC.IN

A API pública deve permitir que o frontend substitua gradualmente os arrays simulados de `js/data.js` por chamadas HTTP.

## Política de versionamento

A API pública será versionada desde a primeira versão usando o prefixo `/api/v1/`.

A versão deve aparecer no caminho da URL para simplificar roteamento, documentação, testes e compatibilidade com o frontend. Versões futuras poderão usar `/api/v2/`, mantendo `/api/v1/` estável pelo tempo necessário.

## Diretrizes

- Usar Django REST Framework.
- Expor somente conteúdos publicados e ativos.
- Usar `slug` em páginas públicas.
- Manter endpoints administrativos separados da API pública.
- Documentar a API com OpenAPI.
- Preservar, quando possível, campos próximos aos objetos atuais do protótipo para reduzir retrabalho no frontend.

## Endpoints iniciais previstos

```txt
GET  /api/v1/site/settings/
GET  /api/v1/site/home/

GET  /api/v1/people/
GET  /api/v1/people/{slug}/

GET  /api/v1/axes/
GET  /api/v1/axes/{slug}/

GET  /api/v1/projects/
GET  /api/v1/projects/{slug}/
GET  /api/v1/projects/categories/

GET  /api/v1/scientific-outputs/
GET  /api/v1/scientific-outputs/{slug}/

GET  /api/v1/posts/
GET  /api/v1/posts/{slug}/
GET  /api/v1/posts/tags/

GET  /api/v1/courses/
GET  /api/v1/courses/{slug}/

GET  /api/v1/transparency-documents/
GET  /api/v1/partners/
GET  /api/v1/metrics/impact/

POST /api/v1/contact/
```

## Filtros públicos previstos

Projetos, posts, cursos e produções científicas devem aceitar filtros por eixo, categoria, status, ano/data, destaque e busca textual quando aplicável.

Exemplos:

```txt
GET /api/v1/projects/?axis=producao-vegetal-e-biotecnologia
GET /api/v1/posts/?axis=redacao-cientifica
GET /api/v1/scientific-outputs/?axis=praticas-em-laboratorio-e-nanotecnologia
GET /api/v1/courses/?axis=agroindustrializacao
```

## Migração do protótipo

- `members` será substituído por `/api/v1/people/`.
- `projects` será substituído por `/api/v1/projects/`.
- `news` será substituído por `/api/v1/posts/`.
- `courses` será substituído por `/api/v1/courses/`.
- `materials` será substituído por vínculos entre cursos e `mediahub`.
- `impactNumbers` será substituído por `/api/v1/metrics/impact/`.

## Restrições

A API pública não deve expor mensagens de contato, rascunhos, dados internos de auditoria ou informações administrativas.
