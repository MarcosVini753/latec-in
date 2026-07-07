# ADR 0005: Separar pessoas de usuários administrativos

## Status
Proposta

## Contexto
O site exibirá membros, professores, ligantes e pesquisadores. Nem todos precisam acessar o sistema.

## Decisão
Criar um modelo de pessoas separado do usuário administrativo do Django.

## Consequências
A exposição pública da equipe fica desacoplada de login, senha e permissões.
