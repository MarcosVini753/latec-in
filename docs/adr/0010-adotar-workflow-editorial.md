# ADR 0010: Adotar workflow editorial simples

## Status

Aceita

## Contexto

O portal LABTEC.IN terá publicações criadas por coordenação, pesquisadores, professores e mentores da LATEC. Conteúdos não devem ficar públicos antes de revisão.

A hierarquia institucional também exige que cada usuário atue somente nas unidades autorizadas.

## Decisão

Manter os status `draft`, `in_review`, `published` e `archived`.

- autores criam e enviam conteúdo para revisão;
- a coordenação competente realiza a publicação final;
- a coordenação do LABTEC.IN pode atuar na raiz e em unidades descendentes;
- coordenadores de unidade atuam somente em seu escopo;
- mentores da LATEC atuam nos próprios eixos;
- a API pública mostra somente conteúdos publicados.

## Consequências positivas

- Separa criação de publicação.
- Mantém revisão final pela coordenação.
- Acrescenta escopo institucional sem criar outro workflow.

## Riscos e cuidados

- Aplicar filtros por unidade no Django Admin e na API.
- Não conceder herança de acesso a todos os papéis.
- Uniformizar gradualmente o uso de `status` e `editorial_status`.
