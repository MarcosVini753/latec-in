# API pública — Portal LABTEC.IN

A API pública permite que o frontend substitua gradualmente os dados locais de `js/data.js` por chamadas HTTP e passe a consumir conteúdos do LABTEC.IN por unidade institucional.

## Estado implementado

O backend expõe `/api/v1/`, paginação, schema OpenAPI e endpoints públicos para unidades, pesquisas, trabalhos acadêmicos e os domínios de conteúdo existentes. Conteúdos com propriedade institucional retornam unidade resumida e aceitam filtro por seu slug. O endpoint público de eventos permanece fora desta entrega.

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
GET  /api/v1/research-projects/
GET  /api/v1/research-projects/{slug}/
GET  /api/v1/academic-works/
GET  /api/v1/academic-works/{slug}/
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

## Endpoint fora desta entrega

```txt
GET /api/v1/events/
GET /api/v1/events/{slug}/
```

Não haverá endpoint público para detalhamento interno da agenda de um evento.

## Filtros públicos

O `PublicReadOnlyModelViewSet` aplica `?unit=<slug>` aos models que possuem `unit`; parceiros usam a relação muitos-para-muitos equivalente. Registros sem unidade continuam serializáveis quando o filtro não é informado, mas não aparecem em uma consulta por unidade.

```txt
GET /api/v1/posts/?unit=labtec-in
GET /api/v1/posts/?unit=latec
GET /api/v1/projects/?unit=latec
GET /api/v1/research-projects/?unit=labtec-in
GET /api/v1/academic-works/?work_type=tcc
GET /api/v1/scientific-outputs/?unit=labtec-in
```

Filtros específicos documentados no OpenAPI:

| Endpoint | Filtros |
| --- | --- |
| `research-projects` | `unit`, `axis`, `project_status`, `year`, `featured`, `search` |
| `academic-works` | `unit`, `work_type`, `year`, `featured`, `search` |
| `scientific-outputs` | `unit`, `axis`, `year`, `featured`, `search` |

O eixo não substitui a unidade: ele classifica prioritariamente conteúdos da LATEC. Todos esses endpoints expõem somente registros publicados no campo editorial do model (`editorial_status` ou o legado `status`) e com `is_published=True`.

## Contratos de pesquisa e produção

- pesquisa inclui unidade resumida, eixo e equipe ordenada;
- trabalho acadêmico inclui unidade, pesquisa resumida e contribuidores ordenados;
- produção científica inclui pesquisa, trabalho acadêmico e autorias internas resumidas;
- `ScientificOutput.authors` continua coexistindo com a autoria estruturada para autores externos;
- representações resumidas evitam ciclos entre pesquisa, trabalho e produção.
- querysets carregam unidade, eixo e relações aninhadas com `select_related`/`prefetch_related` para evitar N+1.

## Representação resumida da unidade

Respostas públicas de conteúdos institucionais incluirão:

```json
{
  "unit": {
    "name": "LABTEC.IN",
    "acronym": "LABTEC.IN",
    "slug": "labtec-in",
    "unit_type": "laboratory"
  }
}
```

## Home do LABTEC.IN

O endpoint `/api/v1/site/home/` retorna somente configurações, heroes, seções e links sociais vinculados diretamente a `labtec-in`. Ele não mistura conteúdo da LATEC nem conteúdo sem unidade. A ampliação da Home com pesquisas, trabalhos, projetos ou eventos permanece fora desta entrega.

## Seção LATEC

A API oferece a unidade `/api/v1/institutional-units/latec/` e conteúdos filtrados por `?unit=latec`, sem backend separado para a Liga. A adoção desses endpoints pelo frontend permanece em outra entrega.

## Compatibilidade

Os slugs e o prefixo `/api/v1/` foram preservados. A unidade é obrigatória nos novos registros de pesquisa e trabalho acadêmico, mas permanece opcional nos modelos legados até a conclusão do backfill. A API pública continua anônima e somente leitura, sem expor o escopo administrativo do usuário.

## Restrições

A API pública não expõe mensagens de contato, rascunhos, auditoria, escopos administrativos ou dados internos. Mensagens de contato continuam disponíveis apenas no fluxo administrativo autorizado.
