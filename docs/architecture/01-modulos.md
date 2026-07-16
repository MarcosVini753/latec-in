# Módulos do backend do portal LABTEC.IN

O backend é dividido em apps Django por domínio. A arquitetura alvo acrescenta `institutional` e `research` aos apps atuais.

## Estado implementado

Estão instalados e implementados: `accounts`, `core`, `people`, `axes`, `mediahub`, `portfolio`, `scientific`, `news`, `learning`, `transparency`, `partnerships` e `metrics`, além de utilidades em `common`.

Ainda não existem os apps `institutional` e `research`. Os módulos atuais também não possuem vínculo genérico com unidade institucional.

## Apps na arquitetura alvo

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
| `mediahub` | Imagens, documentos, PDFs e outros arquivos reutilizáveis. |
| `partnerships` | Parceiros por unidade e mensagens de contato. |
| `metrics` | Métricas por unidade e agregações para a Home. |
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

## Dependências alvo

- `institutional` fornece unidade e hierarquia para `core`, `people`, `axes`, `research`, `portfolio`, `scientific`, `news`, `learning`, `transparency`, `partnerships`, `mediahub` e `metrics`.
- `people` se relaciona com memberships, mentorias, equipes, autoria, pesquisa, trabalhos acadêmicos, posts e cursos.
- `axes` pode classificar conteúdos da LATEC e se relacionar opcionalmente com pesquisas.
- `research` pode originar produções em `scientific`.
- `mediahub` centraliza arquivos reutilizáveis.
- `metrics` pode agregar dados da unidade raiz e de unidades descendentes.
- `accounts` protege o Django Admin e aplica o escopo institucional do usuário.

O [mapa de módulos](diagrams/module-map.md) representa essas relações.

## Delimitação entre domínios

- Pesquisa formal: `research.ResearchProject`.
- TCC ou outro trabalho acadêmico: `research.AcademicWork`.
- Resultado científico publicado: `scientific.ScientificOutput`.
- Iniciativa prática, produto, serviço ou solução: `portfolio.Project`.
- Evento de divulgação, extensão ou capacitação: `learning.Event`, sem modelagem de agenda interna.

Os detalhes estão em [Pesquisas e trabalhos acadêmicos](11-pesquisas-e-trabalhos-academicos.md).

## Sequência de migração

1. Criar `institutional`.
2. Ajustar `people` e `accounts`.
3. Vincular `core` e `axes` às unidades.
4. Criar `research`.
5. Ajustar os demais módulos.
6. Executar backfill, aplicar permissões e retirar campos legados.

O plano completo está em [Migração para a arquitetura LABTEC.IN](12-migracao-labtec.md).
