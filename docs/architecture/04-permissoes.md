# Permissões e acesso administrativo

## Princípios

- Visitantes acessam somente conteúdo público e publicado.
- Pessoas públicas continuam separadas de usuários administrativos.
- O sistema mantém o `User` padrão do Django.
- O Django Admin continua sendo o CMS inicial.
- Toda autorização administrativa deve combinar papel e escopo institucional.
- A unidade raiz pode conceder acesso às unidades descendentes quando configurado.

## Estado implementado

`accounts.Profile` possui hoje um papel global entre administrador, coordenadora, mentor/professor, editor e leitor administrativo. Ainda não existem unidade principal, unidades autorizadas ou herança para descendentes.

Mentorias são vinculadas aos eixos, mas o backend ainda não aplica um escopo institucional genérico.

## Papéis na arquitetura alvo

| Papel | Escopo |
| --- | --- |
| Administrador | Acesso completo ao sistema. |
| Coordenador do laboratório | LABTEC.IN e unidades descendentes; gestão institucional e publicação final. |
| Coordenador de unidade | Conteúdos da unidade atribuída e, quando autorizado, de suas descendentes. |
| Mentor/professor | Conteúdos dos próprios eixos da LATEC e das unidades autorizadas. |

## Escopo institucional

O perfil administrativo deverá informar:

- unidade principal;
- conjunto de unidades autorizadas;
- possibilidade de herdar acesso para unidades descendentes;
- papel administrativo;
- vínculo opcional com `people.Person`.

Exemplo:

- a coordenação do LABTEC.IN acessa o laboratório e a LATEC;
- a coordenação da LATEC acessa somente a LATEC, salvo autorização adicional;
- um mentor da LATEC atua apenas nos eixos aos quais está vinculado.

## Regras por eixo

- Cada professor, orientador ou mentor pode ser vinculado a um ou mais eixos da LATEC.
- O mentor pode criar e editar conteúdo relacionado aos próprios eixos e à unidade autorizada.
- O mentor pode enviar conteúdo para revisão.
- O mentor não realiza publicação final, salvo permissão adicional explícita.
- Um eixo não amplia acesso para outros conteúdos do LABTEC.IN.

## Publicação

- A coordenação do laboratório pode realizar publicação final no LABTEC.IN e nas unidades descendentes.
- A coordenação de unidade pode realizar publicação final em sua unidade quando essa permissão for concedida.
- Mentores seguem o workflow e não publicam por padrão.
- A API pública filtra conteúdos não publicados independentemente do papel administrativo.

## Mensagens de contato

A decisão existente permanece:

- mensagens não são públicas;
- são armazenadas por tempo indeterminado na fase inicial;
- o acesso funcional é restrito à coordenação do LABTEC.IN;
- superusuários técnicos podem ter acesso operacional ao admin ou ao banco.

Coordenadores de unidades filhas não recebem acesso automático às mensagens.

## Migração

1. Manter os papéis atuais durante a transição.
2. Criar unidade principal e unidades autorizadas.
3. Mapear coordenadores e mentores para seus escopos.
4. Aplicar filtros no Django Admin, serviços e serializers administrativos.
5. Habilitar herança apenas para papéis explicitamente autorizados.
6. Reclassificar ou desativar contas legadas de editor e leitor.
7. Retirar regras que dependam exclusivamente do papel global legado.

## Decisões futuras

- Definir o nível necessário de auditoria editorial.
- Formalizar revisão periódica da retenção das mensagens.
- Validar institucionalmente quais coordenadores de unidade terão publicação final.
