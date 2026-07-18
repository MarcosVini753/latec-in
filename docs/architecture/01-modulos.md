# Módulos do backend do portal LABTEC.IN

O backend é dividido em apps Django por domínio. `institutional` centraliza a organização e `research` separa pesquisas e trabalhos acadêmicos do portfólio.

## Estado implementado

Estão instalados e implementados: `institutional`, `accounts`, `core`, `people`, `axes`, `research`, `mediahub`, `portfolio`, `scientific`, `news`, `learning`, `transparency`, `partnerships` e `metrics`, além de utilidades em `common`.

`institutional` fornece unidades, hierarquia validada e memberships. `accounts.Profile` define papel e escopo administrativo. Os modelos de conteúdo possuem propriedade institucional, e o Admin aplica o escopo também a filhos, inlines, autocomplete e parceiros compartilhados. Os campos `unit` herdados continuam opcionais; em `research` a unidade é obrigatória.

## Apps

| App | Responsabilidade |
| --- | --- |
| `institutional` | Estrutura organizacional, unidades, hierarquia e memberships. |
| `accounts` | Usuários administrativos, perfil, papel administrativo e escopo autorizado por unidade. |
| `core` | Configurações do portal, heroes, seções institucionais e links sociais por unidade. |
| `people` | Cadastro da pessoa física, independente de autenticação e de seus vínculos institucionais. |
| `axes` | Sete eixos da LATEC e suas mentorias. |
| `research` | Pesquisas formais, TCCs e outros trabalhos acadêmicos. |
| `portfolio` | Projetos práticos, extensão, produtos, serviços, startups e soluções de inovação. |
| `scientific` | Resultados científicos publicados, autoria e relações com pesquisas e trabalhos acadêmicos. |
| `news` | Notícias, posts, categorias, tags e autores. |
| `learning` | Cursos, trilhas, materiais e eventos com informações gerais. |
| `transparency` | Documentos de transparência do laboratório e de suas unidades. |
| `mediahub` | Catálogo de imagens, documentos, PDFs e outros arquivos, com unidade proprietária opcional. |
| `partnerships` | Parceiros por unidade e mensagens de contato. |
| `metrics` | Métricas e históricos de valores por unidade. |
| `common` | Modelos-base, status editoriais e utilidades compartilhadas. |

## Módulos centrais

### `institutional`

É a dependência central de organização. Define LABTEC.IN como unidade raiz, LATEC como unidade filha e permite futuras unidades sem criar campos booleanos específicos.

### `people`

Mantém a identidade da pessoa. Os papéis institucionais passam a ser expressos por `InstitutionMembership`, e não por um único papel global.

### `axes`

Continua responsável por `ResearchAxis` e `AxisMentorship`, mas deixa de organizar todo o laboratório. Seus sete eixos pertencem à LATEC.

### `research`

Separa pesquisas formais e trabalhos acadêmicos de `portfolio.Project` e de `scientific.ScientificOutput`.

## Dependências

- `institutional` fornece unidade e hierarquia para os conteúdos; a participação de pessoas é representada por `InstitutionMembership`.
- `people` se relaciona com memberships, mentorias, equipes, autoria, pesquisa, trabalhos acadêmicos, posts e cursos.
- `axes` pode classificar conteúdos da LATEC e se relacionar opcionalmente com pesquisas.
- `research` pode originar produções em `scientific`.
- `mediahub` mantém um catálogo próprio, ainda sem relações estruturais com os modelos dos demais domínios.
- `metrics` registra valores informados por unidade; não calcula agregações nem alimenta a Home automaticamente nesta etapa.
- `accounts` protege o Django Admin e aplica o escopo institucional do usuário.

O [mapa de módulos](diagrams/module-map.md) representa essas relações.

## Delimitação entre domínios

- Pesquisa formal: `research.ResearchProject`.
- TCC ou outro trabalho acadêmico: `research.AcademicWork`.
- Resultado científico publicado: `scientific.ScientificOutput`.
- Iniciativa prática, produto, serviço ou solução: `portfolio.Project`.
- Evento de divulgação, extensão ou capacitação: `learning.Event`, sem modelagem de agenda interna.

Os detalhes estão em [Pesquisas e trabalhos acadêmicos](11-pesquisas-e-trabalhos-academicos.md).

## Limites atuais

- `Person.role` e categorias históricas continuam preservados até o corte dos consumidores legados.
- Campos `unit` dos conteúdos anteriores a `research` continuam opcionais durante o backfill.
- O endpoint público de eventos, a expansão da Home e o frontend não integram esta etapa.
- A retirada dos legados e a obrigatoriedade institucional ocorrerão somente após validação dos dados.

O histórico e o corte manual estão em [Migração para a arquitetura LABTEC.IN](12-migracao-labtec.md).
