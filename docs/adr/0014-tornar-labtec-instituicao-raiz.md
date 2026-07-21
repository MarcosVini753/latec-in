# ADR 0014: Tornar o LABTEC.IN a instituição raiz

## Status

Aceita.

## Estado atual

A migração foi concluída: LABTEC.IN é a raiz, LATEC é sua filha, os conteúdos possuem unidade obrigatória e `Person.role` foi removido. Toda `InstitutionalUnit` cadastrada é pública por definição e não possui flags de ativação ou visibilidade. Fallbacks de nomes institucionais antigos foram retirados. As referências abaixo à LATEC.IN e a campos opcionais permanecem como contexto histórico do problema e da estratégia incremental.

## Contexto

A documentação e o backend atuais ainda refletem parcialmente a LATEC.IN como proprietária do portal. A definição institucional aprovada estabelece o LABTEC.IN — Laboratório de Biotecnologia, Biodiversidade e Inovação — como proprietário do portal, do backend e dos conteúdos institucionais.

A LATEC passa a ser uma liga acadêmica ou iniciativa vinculada ao laboratório, com sete eixos, mentorias, ligantes e conteúdos próprios.

## Decisão

Modelar LABTEC.IN como unidade institucional raiz e LATEC como unidade filha.

Será criado o app `institutional`, com:

- `InstitutionalUnit` para hierarquia e propriedade dos conteúdos;
- `InstitutionMembership` para papéis de pessoas por unidade.

Conteúdos usarão relacionamento genérico com unidade, sem booleanos específicos para LABTEC.IN ou LATEC.

## Alternativas consideradas

1. Manter LATEC como proprietária do portal.
2. Apenas renomear LATEC para LABTEC sem modelar unidades.
3. Modelar LABTEC.IN como raiz e LATEC como unidade filha.

A terceira alternativa foi escolhida porque representa a organização real e suporta futuras unidades sem nova remodelagem.

## Consequências positivas

- Propriedade institucional explícita.
- Seção LATEC no mesmo portal e backend.
- Conteúdo filtrável por unidade.
- Papéis distintos da mesma pessoa em diferentes unidades.
- Suporte a programas, grupos e iniciativas futuras.

## Consequências negativas e riscos

- Necessidade de migrations e backfill.
- Revisão manual de projetos, pessoas e conteúdos.
- Maior cuidado com permissões e agregação.
- Período transitório com nomes e campos legados.

## Impacto na modelagem

- novos models `InstitutionalUnit` e `InstitutionMembership`;
- `unit` nos conteúdos aplicáveis;
- autorrelacionamento pai/filho;
- escopo institucional em perfis administrativos;
- sete eixos vinculados à LATEC;
- `Person.role` tratado como legado.

## Impacto na API

- novos endpoints `/api/v1/institutional-units/`;
- filtro `?unit=...`;
- representação resumida da unidade nas respostas;
- Home principal no contexto `labtec-in`;
- seção LATEC no contexto `latec`;
- manutenção da versão `/api/v1/`.

## Impacto na migração

- criar unidades antes dos vínculos;
- adicionar `unit` inicialmente opcional;
- executar backfill por domínio;
- migrar papéis para memberships;
- atualizar permissões, API e interfaces;
- tornar campos obrigatórios e remover legados somente após validação.
