# ADR 0004: Usar Django Admin como CMS inicial

## Status

Aceita

## Contexto

A LATEC.IN precisa gerenciar membros, eixos, projetos, notícias, cursos, materiais, documentos de transparência, produções científicas, parceiros e mensagens de contato.

Construir um painel administrativo customizado logo no início aumentaria prazo e complexidade.

## Decisão

Usar Django Admin como CMS inicial da plataforma.

## Consequências positivas

- Redução do tempo de desenvolvimento inicial.
- Foco na modelagem, API e organização do conteúdo.
- Facilidade para cadastrar e revisar dados durante homologação.

## Riscos e cuidados

- O Django Admin deve ser ajustado para boa usabilidade.
- Um painel customizado poderá ser avaliado depois, caso o admin se torne insuficiente.
