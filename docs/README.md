# Documentação técnica — Portal LABTEC.IN

Esta pasta concentra a documentação técnica e arquitetural do portal do LABTEC.IN — Laboratório de Biotecnologia, Biodiversidade e Inovação.

O LABTEC.IN é a instituição raiz e proprietária do portal, do backend e dos conteúdos institucionais. A LATEC é uma liga acadêmica ou iniciativa vinculada ao laboratório, apresentada como uma unidade e seção específica do mesmo portal.

## Escopo e leitura do estado

Os documentos distinguem três situações:

- **Implementado:** comportamento confirmado no backend atual.
- **Arquitetura alvo:** desenho aprovado para a evolução institucional LABTEC.IN/LATEC.
- **Migração:** sequência planejada para sair do estado atual e alcançar o desenho alvo.

O backend Django e a API `/api/v1/` já estão implementados. A primeira fase da migração institucional também está concluída no código: o app `institutional` modela LABTEC.IN e LATEC, `core` possui vínculos opcionais por unidade e a API expõe as unidades públicas. O restante do backend ainda reflete parcialmente a arquitetura anterior: não possui o app `research`, não classifica os demais conteúdos por unidade e ainda representa o papel público de uma pessoa por um único campo.

Esta documentação registra a arquitetura alvo e o plano de migração. A primeira fase institucional já está implementada no backend; as fases seguintes permanecem planejadas. O frontend continua inalterado.

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
- [API pública](architecture/03-api-publica.md): endpoints implementados e planejados.
- [Estrutura institucional](architecture/10-estrutura-institucional.md): LABTEC.IN, LATEC, unidades e vínculos.
- [Pesquisas e trabalhos acadêmicos](architecture/11-pesquisas-e-trabalhos-academicos.md): separação entre pesquisa, TCC, produção científica e portfólio.
- [Plano de migração](architecture/12-migracao-labtec.md): etapas, backfill, riscos e critérios de conclusão.

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

Não fazem parte desta entrega a implementação dos novos apps, migrations, backfill, alterações do seed Python, frontend, renomeação do repositório, painel administrativo próprio, autenticação pública, inscrições completas, detalhamento interno da agenda de eventos, presença, certificados, pagamentos ou reservas de laboratório e equipamentos.
