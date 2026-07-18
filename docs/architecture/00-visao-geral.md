# Visão geral da arquitetura — Portal LABTEC.IN

O LABTEC.IN — Laboratório de Biotecnologia, Biodiversidade e Inovação — é a instituição raiz, proprietária do portal, do backend e dos conteúdos institucionais.

A LATEC é uma liga acadêmica ou iniciativa vinculada ao LABTEC.IN. Ela será apresentada como uma aba ou seção do portal do laboratório e terá conteúdo identificado pelo vínculo com sua unidade institucional.

## Estado implementado

O repositório possui:

- frontend em HTML, CSS e JavaScript puro, com rotas por hash e dados históricos em `js/data.js`;
- backend Django com Django REST Framework, Django Admin e API `/api/v1/`;
- apps para estrutura institucional, conteúdo institucional, pessoas, eixos, pesquisas e trabalhos acadêmicos, portfólio, produção científica, notícias, aprendizagem, transparência, mídia, parcerias e métricas;
- workflow editorial e comando idempotente `seed_initial_data`.

O app `institutional` modela LABTEC.IN como raiz e LATEC como filha. O seed cria 43 memberships sem duplicação, associa os sete eixos e os nove mentores à LATEC e classifica os conteúdos iniciais por unidade. A hierarquia e os memberships possuem validações de integridade no modelo e no banco.

Os conteúdos legados possuem `unit` opcional durante a transição, parceiros podem se relacionar com várias unidades e a API aceita `?unit=<slug>`. Os novos `ResearchProject` e `AcademicWork` exigem unidade desde a criação. O Admin aplica escopo por unidade e eixo; apenas administrador e coordenação do LABTEC.IN realizam publicação final.

## Estrutura institucional

```txt
LABTEC.IN
├── conteúdos institucionais do laboratório
├── pessoas e vínculos institucionais
├── pesquisas
├── TCCs e trabalhos acadêmicos
├── produções científicas
├── projetos e soluções
├── notícias
├── cursos e capacitações
├── eventos
├── transparência
├── parceiros
└── LATEC
    ├── ligantes
    ├── mentores
    ├── sete eixos de atuação
    ├── projetos específicos
    ├── publicações específicas
    ├── cursos específicos
    └── atividades próprias da Liga
```

Todo conteúdo é gerenciado dentro da estrutura do LABTEC.IN e pode pertencer diretamente ao laboratório, à LATEC ou a futuras unidades. O vínculo usa `institutional.InstitutionalUnit`, sem booleanos específicos para cada unidade.

## Objetivo do backend

Atuar como CMS institucional e API pública do portal LABTEC.IN, permitindo administrar:

- identidade, missão, visão, histórico e canais institucionais;
- pessoas e seus diferentes vínculos com unidades;
- pesquisas, TCCs e outros trabalhos acadêmicos;
- produções científicas;
- projetos, soluções, ações de extensão e inovação;
- notícias, cursos, eventos e materiais;
- transparência, parceiros, mídia, métricas e mensagens de contato;
- conteúdo próprio da LATEC, incluindo ligantes, mentores e sete eixos.

## Áreas públicas

- Home do LABTEC.IN, com conteúdo institucional, destaques e métricas do laboratório.
- Institucional, com missão, visão, valores, histórico, pessoas e unidades.
- Pesquisas, com projetos científicos formais.
- Trabalhos acadêmicos, incluindo TCCs e demais tipos previstos.
- Produções científicas, com artigos, resumos, patentes, livros, e-books e relatórios.
- Portfólio, com soluções, produtos, iniciativas práticas, extensão, startups e inovação.
- Notícias, cursos, capacitações e eventos.
- Transparência, parceiros e canais de contato.
- Seção LATEC, como recorte institucional com ligantes, mentores, eixos e conteúdos próprios.

Eventos possuem somente dados gerais de divulgação, como título, tipo, período, local e inscrição. O detalhamento interno por horários e atividades não integra esta arquitetura. O endpoint público de eventos permanece fora desta entrega.

## Eixos de atuação

Os sete eixos pertencem à LATEC e organizam prioritariamente as atividades da Liga. Eles não são a estrutura global do LABTEC.IN.

Pesquisas do laboratório podem se relacionar opcionalmente com um eixo quando houver vínculo acadêmico com a LATEC. Conteúdos gerais do LABTEC.IN não precisam de eixo.

## Papel da plataforma web

A plataforma mantém quatro funções institucionais:

- transparência;
- repositório científico e acadêmico;
- vitrine de projetos, produtos e soluções;
- difusão, capacitação e extensão.

Essas funções passam a existir no contexto institucional do LABTEC.IN, com possibilidade de recortes por unidade.

## Direção técnica

- Python e Django.
- Django REST Framework.
- API pública em `/api/v1/`.
- Django Admin como CMS inicial.
- `User` padrão do Django.
- PostgreSQL em homologação e produção.
- SQLite no desenvolvimento local inicial.
- mídia local em desenvolvimento e volumes persistentes nos demais ambientes.
- OpenAPI, preferencialmente com `drf-spectacular`.

## Regras consolidadas

- `institutional` é a dependência central de organização.
- LABTEC.IN é a unidade raiz; LATEC é sua unidade filha.
- Uma pessoa pode ter múltiplos papéis na mesma unidade ou em unidades diferentes.
- A Home principal usa exclusivamente conteúdo direto do LABTEC.IN; a API oferece o recorte LATEC por `?unit=latec`.
- Mentores da LATEC atuam somente sobre os próprios eixos.
- Apenas superusuários, administradores e coordenação do LABTEC.IN publicam ou arquivam.
- Conteúdos públicos terão controle editorial, publicação e `slug` quando possuírem página própria.
- Campos `unit` dos modelos legados continuam opcionais; sua obrigatoriedade, o frontend e a expansão da Home permanecem etapas posteriores.
