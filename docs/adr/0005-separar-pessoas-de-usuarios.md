# ADR 0005: Separar pessoas de usuários administrativos

## Status

Aceita

## Contexto

O site exibirá membros, professores, coordenadores, ligantes, pesquisadores, colaboradores e egressos. Nem todos precisam acessar o sistema administrativo.

Misturar pessoa pública com usuário administrativo criaria dependência desnecessária entre exposição institucional e autenticação.

## Decisão

Criar um modelo público de pessoas em `people.Person`, separado do usuário administrativo do Django.

Um usuário administrativo poderá opcionalmente estar vinculado a uma pessoa por meio de `Profile`.

## Consequências positivas

- Membros podem aparecer publicamente sem possuir acesso administrativo.
- Usuários administrativos são criados apenas quando necessário.
- Reduz exposição indevida de dados de login.

## Riscos e cuidados

- Será necessário tratar corretamente o vínculo opcional entre `Profile` e `Person`.
