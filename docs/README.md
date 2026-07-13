# Documentação técnica — LATEC.IN

Esta pasta concentra a documentação técnica e arquitetural do projeto LATEC.IN.

O objetivo é manter as decisões de arquitetura, modelagem de dados, módulos do backend, API pública, permissões e estratégias de implantação versionadas no próprio repositório. Assim, as decisões deixam de ficar espalhadas entre conversas, protótipos e documentos externos.

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
```

## Como usar esta documentação

1. Decisões estruturais devem ser registradas em `docs/adr/`.
2. A arquitetura corrente do sistema deve ser mantida em `docs/architecture/`.
3. A modelagem do banco deve evoluir em `docs/architecture/02-modelagem-banco.md` e no diagrama `docs/architecture/diagrams/erd.md`.
4. Novos módulos devem ser descritos em `docs/architecture/01-modulos.md` antes ou durante sua implementação.
5. Alterações relevantes na arquitetura devem atualizar os ADRs existentes ou gerar novos ADRs.

## Estado atual

O projeto possui um protótipo frontend em HTML, CSS e JavaScript puro. A próxima fase planejada é construir um backend em Django para atuar como CMS institucional e API pública para o site da LATEC.IN.

## Direção técnica consolidada

- Backend em Django.
- API pública com Django REST Framework.
- API pública versionada por `/api/v1/`.
- Django Admin como CMS inicial.
- Usuário padrão do Django, com autenticação básica por usuário e senha.
- PostgreSQL como banco-alvo para homologação e produção.
- SQLite aceitável apenas para desenvolvimento local inicial.
- Armazenamento local em desenvolvimento e volumes no servidor em homologação e produção.
- Documentação técnica versionada em Markdown.
- Diagramas em Mermaid para facilitar versionamento e revisão via Git.
