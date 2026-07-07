# ADR 0003: Usar PostgreSQL em produção

## Status
Aceita

## Contexto
O backend armazenará conteúdo institucional, relacionamentos muitos-para-muitos, arquivos, mensagens e dados editoriais.

## Decisão
Usar PostgreSQL como banco de homologação e produção. SQLite pode ser usado apenas no início do desenvolvimento local.

## Consequências
O projeto terá um banco robusto para produção e compatível com recursos avançados do Django.
