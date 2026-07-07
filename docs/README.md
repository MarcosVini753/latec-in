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
```

## Como usar esta documentação

1. As decisões estruturais devem ser registradas em `docs/adr/`.
2. A arquitetura corrente do sistema deve ser mantida em `docs/architecture/`.
3. A modelagem do banco deve evoluir em `docs/architecture/02-modelagem-banco.md` e no diagrama `docs/architecture/diagrams/erd.md`.
4. Novos módulos devem ser descritos em `docs/architecture/01-modulos.md` antes ou durante sua implementação.
5. Alterações relevantes na arquitetura devem atualizar os ADRs existentes ou gerar novos ADRs.

## Estado atual

O projeto possui um protótipo frontend em HTML, CSS e JavaScript puro. A próxima fase planejada é construir um backend em Django para atuar como CMS institucional e API pública para o site da LATEC.IN.

## Direção técnica consolidada

- Backend em Django.
- API pública com Django REST Framework.
- Django Admin como CMS inicial.
- PostgreSQL como banco-alvo para homologação e produção.
- SQLite aceitável apenas para desenvolvimento local inicial.
- Documentação técnica versionada em Markdown.
- Diagramas em Mermaid para facilitar versionamento e revisão via Git.
