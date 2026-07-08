# ADR 0003: Usar PostgreSQL em produção

## Status

Aceita

## Contexto

O backend armazenará conteúdo institucional, relacionamentos muitos-para-muitos, arquivos, mensagens, dados editoriais, produções científicas e métricas.

SQLite é suficiente para desenvolvimento local inicial, mas não é a escolha adequada para homologação e produção.

## Decisão

Usar PostgreSQL como banco de dados para homologação e produção. SQLite pode ser usado apenas no desenvolvimento local inicial.

## Consequências positivas

- Banco adequado para uso institucional.
- Melhor suporte a integridade relacional e crescimento futuro.
- Boa compatibilidade com recursos avançados do Django.

## Riscos e cuidados

- Configuração por variáveis de ambiente.
- Necessidade de backups.
- Necessidade de testar migrations antes de produção.
