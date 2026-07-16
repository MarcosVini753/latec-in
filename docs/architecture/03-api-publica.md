# API pública — Portal LABTEC.IN

A API pública permite que o frontend substitua gradualmente os dados locais de `js/data.js` por chamadas HTTP e passe a consumir conteúdos do LABTEC.IN por unidade institucional.

## Estado implementado

O backend atual já expõe `/api/v1/`, paginação, schema OpenAPI e endpoints públicos para unidades institucionais, configurações, Home, pessoas, eixos, projetos, produções científicas, posts, cursos, transparência, parceiros, métricas e contato.

Ainda não existem endpoints de pesquisas, trabalhos acadêmicos ou eventos. Os demais conteúdos atuais também não aceitam filtro por unidade nem retornam uma representação de `InstitutionalUnit`; essa adição foi adiada para preservar os payloads existentes na primeira fase.

## Política de versionamento

O prefixo permanece `/api/v1/`.

Não será aberta uma nova versão durante esta etapa de arquitetura porque a API ainda está em desenvolvimento e não há consumidores externos estáveis conhecidos. As mudanças serão evoluídas na versão inicial antes de sua estabilização pública.

## Diretrizes

- Usar Django REST Framework.
- Expor somente conteúdos ativos e publicados.
- Usar `slug` nos detalhes públicos.
- Manter endpoints administrativos fora da API pública.
- Documentar a API com OpenAPI.
- Preservar `/api/v1/` em todos os endpoints.
- Incluir unidade resumida nos conteúdos aos quais ela se aplica.
- Permitir filtro por unidade sem duplicar endpoints por instituição.

## Endpoints implementados

```txt
GET  /api/v1/site/settings/
GET  /api/v1/site/home/
GET  /api/v1/institutional-units/
GET  /api/v1/institutional-units/{slug}/
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

## Endpoints planejados

```txt
GET /api/v1/research-projects/
GET /api/v1/research-projects/{slug}/

GET /api/v1/academic-works/
GET /api/v1/academic-works/{slug}/

GET /api/v1/events/
GET /api/v1/events/{slug}/
```

Não haverá endpoint público para detalhamento interno da agenda de um evento.

## Filtros públicos planejados

Endpoints aplicáveis aceitarão `unit`:

```txt
GET /api/v1/posts/?unit=labtec-in
GET /api/v1/posts/?unit=latec
GET /api/v1/projects/?unit=latec
GET /api/v1/research-projects/?unit=labtec-in
GET /api/v1/academic-works/?work_type=tcc
GET /api/v1/scientific-outputs/?unit=labtec-in
GET /api/v1/events/?unit=labtec-in
```

Filtros existentes por eixo, categoria, ano, destaque e busca textual permanecem quando fizerem sentido. O eixo não substitui a unidade: ele classifica prioritariamente conteúdos da LATEC.

## Representação resumida da unidade

Respostas públicas de conteúdos institucionais incluirão:

```json
{
  "unit": {
    "name": "LABTEC.IN",
    "slug": "labtec-in",
    "unit_type": "laboratory"
  }
}
```

## Home do LABTEC.IN

O endpoint `/api/v1/site/home/` continuará existindo e deverá evoluir para a seguinte resposta conceitual:

```json
{
  "settings": {},
  "institution": {},
  "heroes": [],
  "sections": [],
  "featured_research": [],
  "featured_academic_works": [],
  "featured_projects": [],
  "latest_posts": [],
  "upcoming_events": [],
  "metrics": [],
  "initiatives": [],
  "social_links": []
}
```

A Home principal será composta pelo contexto `labtec-in`. Métricas e destaques poderão agregar unidades filhas quando essa regra estiver habilitada.

## Seção LATEC

A página da LATEC consumirá a unidade `/api/v1/institutional-units/latec/` e conteúdos filtrados por `?unit=latec`. Ela não terá backend ou API separados.

## Migração

1. Criar serializers e endpoints de unidades.
2. Adicionar `unit` opcional aos serializers existentes.
3. Executar o backfill.
4. Habilitar filtros por unidade.
5. Adicionar os endpoints de `research` e de eventos.
6. Atualizar a Home e a seção LATEC.

Durante a transição, respostas legadas podem permanecer temporariamente, desde que a documentação OpenAPI identifique os campos em retirada.

## Restrições

A API pública não expõe mensagens de contato, rascunhos, auditoria, escopos administrativos ou dados internos. Mensagens de contato continuam disponíveis apenas no fluxo administrativo autorizado.
