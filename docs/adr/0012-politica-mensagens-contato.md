# ADR 0012: Política inicial para mensagens de contato

## Status

Aceita

## Contexto

O formulário público de contato coletará nome, e-mail, assunto e mensagem. Esses dados não devem ser públicos.

## Decisão

Na primeira versão, mensagens de contato serão mantidas por tempo indeterminado e acessadas funcionalmente apenas pela coordenadora.

## Consequências positivas

- Simplifica a gestão inicial das mensagens.
- Reduz exposição de dados pessoais.
- Mantém rastreabilidade de contatos recebidos.

## Riscos e cuidados

- A política de retenção deve ser revisada no futuro.
- Superusuários técnicos podem ter acesso operacional ao admin ou banco, mas a regra funcional deve restringir o uso à coordenação.
