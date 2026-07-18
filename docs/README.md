# Documentação técnica — Portal LABTEC.IN

Esta pasta concentra a documentação técnica e arquitetural do portal do LABTEC.IN — Laboratório de Biotecnologia, Biodiversidade e Inovação.

O LABTEC.IN é a instituição raiz e proprietária do portal, do backend e dos conteúdos institucionais. A LATEC é uma liga acadêmica ou iniciativa vinculada ao laboratório, apresentada como uma unidade e seção específica do mesmo portal.

## Escopo e leitura do estado

Os documentos distinguem três situações:

- **Implementado:** comportamento confirmado no backend atual.
- **Compatibilidade:** campos e dados antigos preservados durante a transição.
- **Próximos cortes:** mudanças que dependem de validação manual ou de outra entrega.

O backend Django implementa a estrutura LABTEC.IN/LATEC, memberships validados, classificação institucional dos conteúdos, escopo do Admin por unidade e eixo, o app `research`, autoria científica estruturada e endpoints públicos de pesquisas e trabalhos em `/api/v1/`. O seed idempotente cria 43 memberships e preserva dados e slugs legados durante a transição.

Os models anteriores a `research` ainda aceitam `unit` nula, `Person.role` e categorias históricas não foram removidos, e o projeto de portfólio que originou a pesquisa permanece disponível até revisão e corte manual. O frontend, a expansão da Home, o endpoint público de eventos e a obrigatoriedade desses campos continuam fora desta entrega.

## Estrutura

```txt
docs/
  README.md
  architecture/
    00-visao-geral.md
    01-modulos.md
    02-modelagem-banco.md
    03-api-publica.md
    04-permissoes.md
    05-deploy.md
    06-eixos-de-atuacao.md
    07-workflow-editorial.md
    08-seed-e-fixtures.md
    09-transparencia-e-repositorio.md
    10-estrutura-institucional.md
    11-pesquisas-e-trabalhos-academicos.md
    12-migracao-labtec.md
    diagrams/
      c4-context.md
      c4-container.md
      erd.md
      module-map.md
  adr/
    0001-usar-django-e-drf.md
    0002-dividir-backend-em-apps-por-dominio.md
    0003-usar-postgresql-em-producao.md
    0004-usar-django-admin-como-cms-inicial.md
    0005-separar-pessoas-de-usuarios.md
    0006-usar-mediahub-para-arquivos-e-anexos.md
    0007-versionar-api-com-api-v1.md
    0008-usar-user-padrao-django.md
    0009-adotar-eixos-de-atuacao.md
    0010-adotar-workflow-editorial.md
    0011-usar-storage-local-e-volumes.md
    0012-politica-mensagens-contato.md
    0013-seed-inicial-dados.md
    0014-tornar-labtec-instituicao-raiz.md
    0015-separar-pesquisas-tccs-portfolio.md
```

## Mapa de leitura

- [Visão geral](architecture/00-visao-geral.md): contexto institucional e direção técnica.
- [Módulos](architecture/01-modulos.md): responsabilidades e dependências dos apps.
- [Modelagem](architecture/02-modelagem-banco.md): entidades atuais e alvo.
- [API pública](architecture/03-api-publica.md): endpoints, filtros e limites da entrega atual.
- [Estrutura institucional](architecture/10-estrutura-institucional.md): LABTEC.IN, LATEC, unidades e vínculos.
- [Pesquisas e trabalhos acadêmicos](architecture/11-pesquisas-e-trabalhos-academicos.md): separação entre pesquisa, TCC, produção científica e portfólio.
- [Plano de migração](architecture/12-migracao-labtec.md): backfill, conversão reversível e corte manual dos legados.

## Direção técnica consolidada

- Django e Django REST Framework.
- API pública mantida em `/api/v1/`.
- Django Admin como CMS inicial.
- `User` padrão do Django para autenticação administrativa.
- PostgreSQL em homologação e produção; SQLite apenas no desenvolvimento local inicial.
- Mídia local em desenvolvimento e volumes persistentes em homologação e produção.
- `institutional.InstitutionalUnit` como raiz genérica de propriedade dos conteúdos.
- `institutional.InstitutionMembership` para papéis de pessoas por unidade.
- `research` para pesquisas formais e trabalhos acadêmicos.
- Sete eixos e mentorias pertencentes à unidade LATEC.
- Workflow editorial `draft`, `in_review`, `published` e `archived`.

## Fora do escopo desta atualização

Não fazem parte desta entrega o frontend, a expansão da Home, o endpoint público de eventos, a obrigatoriedade dos campos institucionais legados, o corte automático do projeto convertido, painel administrativo próprio, autenticação pública, inscrições completas, detalhamento interno da agenda de eventos, presença, certificados, pagamentos ou reservas de laboratório e equipamentos.
