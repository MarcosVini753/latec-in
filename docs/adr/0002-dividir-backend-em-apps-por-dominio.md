# ADR 0002: Dividir o backend em apps por domínio

## Status

Aceita

## Estado atual

A divisão por domínio permanece aceita, mas o app `mediahub` listado na decisão original foi removido integralmente pelo [ADR 0016](0016-simplificar-conteudo-e-cortar-legados.md). Arquivos agora pertencem diretamente aos apps que os publicam. A lista e os cuidados abaixo registram a arquitetura proposta naquele momento, não os apps atualmente instalados.

## Contexto

O portal do LABTEC.IN abrange estrutura institucional, pessoas, eixos da LATEC, pesquisas, trabalhos acadêmicos, portfólio, notícias, aprendizagem, arquivos, transparência, produção científica, parceiros e métricas.

Um único app Django aumentaria acoplamento e misturaria conceitos com ciclos de vida diferentes.

## Decisão

Organizar o backend em apps por domínio.

Apps da arquitetura alvo:

- `institutional`;
- `accounts`;
- `core`;
- `people`;
- `axes`;
- `research`;
- `portfolio`;
- `scientific`;
- `news`;
- `learning`;
- `transparency`;
- `mediahub`;
- `partnerships`;
- `metrics`;
- `common`.

`institutional` será a dependência central de organização. `research` separará pesquisas formais e trabalhos acadêmicos do portfólio e da produção científica.

## Consequências positivas

- Responsabilidades mais claras.
- Evolução incremental por domínio.
- Unidades institucionais reutilizáveis em todos os conteúdos.
- Separação entre pesquisa, trabalho acadêmico, resultado científico e projeto prático.

## Riscos e cuidados

- Evitar dependências circulares.
- Manter `institutional`, `people` e `mediahub` com contratos simples.
- Não transformar a divisão por apps em duplicação de modelos ou endpoints.
