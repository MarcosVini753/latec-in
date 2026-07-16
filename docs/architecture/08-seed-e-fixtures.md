# Seed e fixtures do portal LABTEC.IN

O seed continuará sendo idempotente e servirá para desenvolvimento, homologação e migração controlada do conteúdo histórico.

## Estado implementado

O comando atual é:

```txt
python manage.py seed_initial_data
```

Ele cria ou atualiza, sem duplicação:

- 7 papéis públicos;
- 33 pessoas;
- 7 eixos;
- 9 mentorias;
- 3 projetos, 5 resultados e 7 vínculos de equipe;
- 2 posts;
- 2 cursos e 1 material;
- 7 métricas;
- configurações do site, 1 hero e 3 seções institucionais.

Esse seed ainda usa a identidade histórica da LATEC.IN como raiz, mantém pesquisa e produção científica como categorias de portfólio e não possui unidades, memberships, pesquisas formais ou trabalhos acadêmicos.

## Estratégia alvo

O comando continuará idempotente e será reorganizado conceitualmente em:

```txt
seed_institutional_units()
seed_roles()
seed_people()
seed_memberships()
seed_axes()
seed_axis_mentorships()
seed_labtec_settings()
seed_latec_profile()
seed_research_categories()
seed_academic_work_types()
seed_projects()
seed_scientific_outputs()
seed_posts()
seed_courses()
seed_events()
seed_metrics()
```

Essa lista expressa responsabilidades; a implementação pode manter um único comando e métodos internos simples.

## Dados institucionais iniciais

- LABTEC.IN como unidade raiz do tipo `laboratory`.
- LATEC como unidade filha do tipo `academic_league`.
- configurações do site vinculadas ao LABTEC.IN.
- perfil institucional da LATEC.
- memberships de coordenação, pesquisadores, professores, mentores e ligantes.
- sete eixos vinculados à LATEC.
- mentorias mantidas nos eixos.

## Classificação inicial dos dados

| Dado | Unidade inicial |
| --- | --- |
| `SiteSettings` e Home principal | LABTEC.IN |
| Sete eixos e mentorias | LATEC |
| Ligantes | LATEC |
| Pesquisadores e professores | LABTEC.IN, com memberships adicionais quando aplicável |
| Notícias explicitamente da Liga | LATEC |
| Cursos específicos da Liga | LATEC |
| Pesquisas e trabalhos acadêmicos | LABTEC.IN |
| Produção científica geral | LABTEC.IN |
| Transparência institucional | LABTEC.IN |
| Projetos existentes | Revisão manual |

## Pesquisas e trabalhos acadêmicos

O seed alvo deverá incluir:

- categorias ou escolhas iniciais de pesquisa;
- tipos de trabalho acadêmico;
- pesquisas formalmente classificadas;
- TCCs e outros trabalhos acadêmicos quando os dados forem validados;
- relações com pessoas, unidades, eixos e produções científicas.

Registros históricos classificados como “Pesquisa” ou “Produção Científica” em `portfolio` não serão movidos automaticamente sem análise do conteúdo.

## Eventos

O seed poderá criar eventos com informações gerais de divulgação. Não serão criados itens internos por horário nem dados detalhados de agenda.

## Métricas

As métricas serão separadas por unidade:

- LABTEC.IN: pesquisas, trabalhos acadêmicos, pesquisadores, produções, projetos, cursos, eventos, parcerias e iniciativas;
- LATEC: ligantes, mentores, eixos e conteúdos específicos.

Métricas da unidade raiz poderão incluir descendentes quando `aggregation_mode` permitir.

## Idempotência e ordem

- Usar chaves estáveis como `slug`, `key` ou combinação única.
- Criar unidades antes de memberships e conteúdos.
- Criar pessoas antes de vínculos de equipe e autoria.
- Criar eixos antes de mentorias.
- Não apagar registros editoriais criados manualmente.
- Atualizar somente campos sob responsabilidade declarada do seed.

## Validações manuais

- nome oficial, missão, visão, contatos e identidade visual do LABTEC.IN;
- descrição institucional da LATEC;
- papéis de cada pessoa por unidade;
- classificação dos projetos existentes;
- grafia de mentores;
- autoria e arquivos de pesquisas, trabalhos e produções;
- valores iniciais das métricas.

Nenhuma alteração no comando Python é realizada nesta tarefa documental.
