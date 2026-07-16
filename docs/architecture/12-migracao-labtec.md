# Migração para a arquitetura institucional LABTEC.IN

Este plano documenta a transição do backend atual para LABTEC.IN como instituição raiz e LATEC como unidade filha. Nenhuma migration ou alteração de código é executada nesta tarefa.

## Estado atual

- O backend Django e a API `/api/v1/` estão implementados.
- Nomes históricos ainda tratam a LATEC.IN como instituição principal.
- `SiteSettings` não se relaciona com uma unidade.
- `Person` possui um único papel público.
- `Profile` possui papel administrativo global, sem escopo institucional.
- Eixos, conteúdos, parceiros e métricas não possuem `unit`.
- Os sete eixos são implicitamente ligados à Liga, mas isso não está modelado.
- Não existem os apps `institutional` e `research`.
- Pesquisa e produção científica podem estar misturadas ao portfólio.
- Autoria científica ainda é textual.
- O seed atual reproduz essa estrutura.

## Arquitetura alvo

- LABTEC.IN como `InstitutionalUnit` raiz.
- LATEC como unidade filha.
- `InstitutionMembership` para papéis por unidade.
- escopo institucional nos usuários administrativos.
- vínculo `unit` nos conteúdos aplicáveis.
- sete eixos vinculados à LATEC.
- pesquisas e trabalhos acadêmicos em `research`.
- produções publicadas em `scientific`.
- projetos práticos e soluções em `portfolio`.
- API `/api/v1/` com filtros e representação de unidade.

## Incompatibilidades a resolver

| Área | Estado atual | Alvo |
| --- | --- | --- |
| Identidade | Nome histórico como raiz | LABTEC.IN raiz; LATEC filha |
| Pessoas | Um `Person.role` | Vários memberships por unidade |
| Administração | Papel global | Papel e unidades autorizadas |
| Eixos | Sem unidade | Sete eixos da LATEC |
| Conteúdos | Sem propriedade institucional | Relação com `InstitutionalUnit` |
| Pesquisa | Misturada ao portfólio | App `research` |
| TCCs | Sem model próprio | `AcademicWork` |
| Autoria científica | Texto livre | `ScientificAuthorship` e texto externo |
| API | Sem filtro por unidade | `?unit=...` em `/api/v1/` |
| Seed | Estrutura histórica | LABTEC.IN, LATEC e backfill classificado |

## Etapa 1 — estrutura institucional

1. Criar o app `institutional`.
2. Criar `InstitutionalUnit`.
3. Criar LABTEC.IN como unidade raiz.
4. Criar LATEC como unidade filha.
5. Criar `InstitutionMembership`.
6. Validar slugs estáveis `labtec-in` e `latec`.

Essa migration deve adicionar estrutura sem alterar os dados existentes.

## Etapa 2 — campos de unidade opcionais

Adicionar `unit` com `null=True` durante a transição em:

- configurações e seções de `core`;
- eixos;
- pesquisas e trabalhos acadêmicos novos;
- projetos;
- produções científicas;
- posts;
- cursos, trilhas, materiais e eventos quando aplicável;
- transparência;
- mídia, como vínculo opcional;
- parceiros, por relação de múltiplas unidades;
- métricas.

Nenhum campo deve se tornar obrigatório antes do inventário e backfill.

## Etapa 3 — backfill institucional

Classificação inicial:

| Registro | Unidade |
| --- | --- |
| `SiteSettings`, heroes, seções e links da Home principal | LABTEC.IN |
| Sete eixos | LATEC |
| Mentorias dos eixos | LATEC por meio do eixo |
| Ligantes | LATEC |
| Pesquisadores e professores | LABTEC.IN |
| Notícias explicitamente da Liga | LATEC |
| Cursos específicos da Liga | LATEC |
| Pesquisas e trabalhos acadêmicos | LABTEC.IN |
| Produção científica geral | LABTEC.IN |
| Transparência institucional | LABTEC.IN |
| Projetos existentes | Revisão manual |

Pessoas podem receber mais de um membership. Professores que também são mentores terão vínculo no LABTEC.IN e na LATEC quando confirmado.

## Etapa 4 — memberships e permissões

1. Converter `Person.role` em memberships equivalentes.
2. Preservar o campo legado temporariamente.
3. Definir unidade principal e unidades autorizadas em `Profile`.
4. Separar coordenador do laboratório de coordenador de unidade.
5. Configurar herança de acesso para a coordenação do LABTEC.IN.
6. Limitar mentores aos próprios eixos da LATEC.
7. Reclassificar ou desativar contas com os papéis legados `editor` e `reader`.
8. Atualizar Django Admin e serviços administrativos.

## Etapa 5 — pesquisa, trabalhos e produção científica

1. Criar o app `research`.
2. Criar pesquisas e trabalhos acadêmicos validados.
3. Inventariar categorias históricas de portfólio.
4. Migrar pesquisas formais para `ResearchProject`.
5. Migrar TCCs e outros trabalhos para `AcademicWork`.
6. Manter resultados publicados em `ScientificOutput`.
7. Criar autoria estruturada.
8. Relacionar produções a pesquisas e trabalhos.
9. Manter projetos práticos em `portfolio.Project`.
10. Revisar tipos históricos genéricos de `ScientificOutput`.

Projetos históricos exigem classificação manual antes de qualquer movimentação.

## Etapa 6 — API, consultas e interfaces

1. Expor unidades em `/api/v1/institutional-units/`.
2. Expor pesquisas em `/api/v1/research-projects/`.
3. Expor trabalhos em `/api/v1/academic-works/`.
4. Adicionar `unit` resumida às respostas aplicáveis.
5. Adicionar filtro `?unit=labtec-in` e `?unit=latec`.
6. Atualizar a Home para o contexto LABTEC.IN.
7. Atualizar a seção LATEC para consumir o recorte `latec`.
8. Atualizar OpenAPI, testes e frontend em entregas próprias.

Não será criada uma nova versão da API durante essa transição.

## Etapa 7 — obrigatoriedade e retirada de legados

Depois de validar o backfill:

1. tornar `unit` obrigatório onde fizer sentido;
2. manter `MediaAsset.unit` opcional para casos técnicos;
3. remover consultas dependentes de `Person.role`;
4. marcar categorias incompatíveis do portfólio como inativas;
5. substituir textos institucionais históricos;
6. remover `Person.role` em migration posterior;
7. retirar campos ou opções legadas somente após ausência de uso.

## Reversibilidade

- separar criação de tabelas, adição de campos, backfill e remoção;
- manter campos novos opcionais até a validação;
- usar migrations de dados com operação reversa quando possível;
- não remover dados históricos durante reclassificação;
- registrar mapeamentos antigos e novos;
- gerar backup antes de cada etapa de produção;
- validar rollback em homologação.

## Riscos

- classificação incorreta entre pesquisa, produção e portfólio;
- perda de contexto ao converter papel único em memberships;
- conteúdo sem unidade após backfill;
- permissões excessivas por herança indevida;
- métricas duplicadas ao agregar descendentes;
- links públicos alterados por mudança de slug;
- arquivos sem autorização clara para publicação;
- divergência entre nomes institucionais no frontend, seed e banco.

## Mitigações

- relatórios de registros sem unidade;
- validação manual de projetos e pessoas;
- constraints adicionadas somente após limpeza;
- testes de permissão por unidade;
- comparação de contagens antes e depois;
- manutenção dos slugs públicos sempre que possível;
- migrations pequenas e revisáveis;
- homologação com cópia controlada dos dados.

## Critérios de conclusão

- LABTEC.IN existe como única unidade raiz.
- LATEC existe como filha do LABTEC.IN.
- Todo conteúdo aplicável possui unidade.
- Os sete eixos pertencem à LATEC.
- Pessoas possuem memberships coerentes.
- Pesquisas e trabalhos acadêmicos estão em domínio próprio.
- Produções e projetos foram classificados corretamente.
- API e Home retornam o contexto institucional esperado.
- Permissões respeitam unidade e descendência.
- Seed e documentação usam a nova estrutura.
- Campos legados não possuem consumidores antes da remoção.
- Backfill e rollback foram validados em homologação.

## Itens que exigem validação manual

- nome, missão, visão, contatos e identidade visual oficiais do LABTEC.IN;
- descrição e enquadramento oficial da LATEC;
- coordenação e papéis de cada pessoa por unidade;
- lista oficial de pesquisadores e ligantes;
- classificação de todos os projetos existentes;
- catálogo de pesquisas, TCCs e produções;
- autoria, orientação, arquivos e direitos de publicação;
- quais conteúdos da Home agregam unidades filhas;
- valores e regras de agregação das métricas;
- permissões de publicação para coordenadores de unidade.

## Fora do escopo desta entrega

- implementação de models e migrations;
- execução real do backfill;
- alteração do seed Python;
- mudança do frontend;
- renomeação do repositório;
- painel administrativo próprio;
- autenticação pública;
- pagamentos, certificados ou reservas.
