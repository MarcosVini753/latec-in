# ADR 0001: Usar Django e Django REST Framework

## Status
Aceita

## Contexto
A LATEC.IN precisa de um backend para gerenciar conteúdo institucional, projetos, notícias, cursos, membros, materiais e contatos.

## Decisão
Usar Django como framework backend e Django REST Framework para a API pública.

## Consequências
O projeto ganha ORM, migrations, autenticação, permissões e Django Admin. A API poderá substituir gradualmente os dados simulados do protótipo.
