# Seed e fixtures do portal LABTEC.IN

O seed continuará sendo idempotente e servirá para desenvolvimento, homologação e migração controlada do conteúdo histórico.

## Estado implementado

O comando atual é:

```txt
python manage.py seed_initial_data
```

Ele cria ou atualiza, sem duplicação:

- 2 unidades institucionais;
- 7 papéis públicos;
- 33 pessoas;
- 43 memberships institucionais;
- 7 eixos;
- 9 mentorias;
- projetos de portfólio, resultados e equipes iniciais;
- 1 pesquisa formal em rascunho;
- 2 posts;
- 2 cursos e 1 material;
- 7 métricas;
- configurações do site, 1 hero e 3 seções institucionais.

O seed cria LABTEC.IN como raiz, LATEC como filha e associa as configurações, o hero, as seções e as métricas iniciais ao laboratório. Os sete eixos, ligantes e conteúdos explicitamente ligados à Liga pertencem à LATEC. Em banco novo, a pesquisa de bioativos é criada somente como `ResearchProject` em rascunho; em banco atualizado, o projeto de portfólio legado é preservado até o corte manual.

## Organização do comando

O comando idempotente está organizado em métodos simples:

```txt
seed_institutional_units()
seed_roles()
seed_people()
seed_institution_memberships()
seed_axes()
seed_axis_mentorships()
seed_mentor_memberships()
seed_project_categories()
seed_project_statuses()
seed_projects()
seed_research_projects()
seed_post_categories()
seed_posts()
seed_learning_tracks()
seed_courses()
seed_metrics()
seed_site_settings()
```

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
| Pesquisas e trabalhos acadêmicos | Unidade validada no registro; a pesquisa inicial preserva LATEC |
| Produção científica geral | LABTEC.IN |
| Transparência institucional | LABTEC.IN |
| Projetos existentes | Classificação provisória preservada para revisão manual |

## Memberships

Os 43 vínculos iniciais são compostos por:

- ligantes na LATEC;
- professores e pesquisadores no LABTEC.IN;
- coordenação no LABTEC.IN e na LATEC;
- estagiários no LABTEC.IN quando aplicável;
- nove memberships `Mentor` na LATEC, um para cada pessoa presente em `AxisMentorship`.

A chave estável é `(person, unit, role)`, portanto Marta pode possuir `Coordenadora` e `Mentor` na LATEC sem conflito.

## Pesquisa histórica

`pesquisa-de-bioativos-da-amazonia` é semeada idempotentemente como pesquisa formal em rascunho. O comando não infere metodologia, datas, instituição ou autoria científica. Um projeto legado existente não é apagado nem republicado pelo seed caso tenha sido arquivado depois; seu corte só ocorre após revisão e publicação do novo registro.

## Eventos

O seed e o endpoint público de eventos não foram ampliados nesta entrega. Não existem itens internos por horário nem dados detalhados de agenda.

## Métricas

As métricas serão separadas por unidade:

- LABTEC.IN: pesquisas, trabalhos acadêmicos, pesquisadores, produções, projetos, cursos, eventos, parcerias e iniciativas;
- LATEC: ligantes, mentores, eixos e conteúdos específicos.

As métricas atuais permanecem vinculadas ao LABTEC.IN por enquanto; agregação de descendentes não foi acrescentada nesta entrega.

## Idempotência e ordem

- Usar chaves estáveis como `slug`, `key` ou combinação única.
- Criar unidades antes de memberships e conteúdos.
- Criar pessoas antes de vínculos de equipe e autoria.
- Criar eixos antes de mentorias.
- Não apagar registros editoriais criados manualmente.
- Atualizar somente campos sob responsabilidade declarada do seed.
- Não elevar o status editorial de um legado arquivado manualmente.

## Textos e URLs preservadas

- O hero do LABTEC.IN descreve um laboratório, não uma liga acadêmica.
- Conteúdos da unidade filha usam o nome LATEC.
- A biografia da coordenação explicita os papéis no LABTEC.IN e na LATEC.
- As descrições de Professor e Egresso distinguem laboratório e Liga.
- Os slugs públicos existentes são informados explicitamente e não mudam com a correção do título visível.
- O fallback técnico `site_name__in=("LABTEC.IN", "LATEC.IN")` permanece para localizar bancos antigos.

## Validações manuais

- nome oficial, missão, visão, contatos e identidade visual do LABTEC.IN;
- descrição institucional da LATEC;
- papéis de cada pessoa por unidade;
- classificação dos projetos existentes;
- grafia de mentores;
- autoria e arquivos de pesquisas, trabalhos e produções;
- valores iniciais das métricas.

O comando não cria usuários administrativos nem credenciais.
