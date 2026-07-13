# Visão geral da arquitetura — LATEC.IN

A LATEC.IN é a Liga Acadêmica de Biotecnologia, Biodiversidade e Inovação. O portal deve funcionar como site institucional, vitrine de projetos e canal de comunicação entre a liga, a comunidade acadêmica, parceiros, setor produtivo e sociedade.

O projeto atual possui um protótipo frontend em HTML, CSS e JavaScript puro. O frontend simula uma SPA com rotas por hash e dados locais em `js/data.js`. A próxima etapa é criar um backend em Django para persistir os dados e permitir administração de conteúdo.

## Objetivo do backend

Construir uma plataforma backend para atuar como CMS institucional e API pública da LATEC.IN.

O backend deverá permitir gerenciar informações institucionais, membros, professores, coordenadores, ligantes, pesquisadores, eixos de atuação, projetos, produções científicas, notícias, cursos, eventos, materiais, arquivos, parceiros, documentos de transparência, mensagens de contato, métricas e permissões administrativas.

## Áreas públicas previstas

- Home, com hero section, destaques e números de impacto.
- Quem Somos, com histórico, propósito, missão, visão, valores, linhas de atuação e equipe.
- Eixos de Atuação, com os sete eixos institucionais e suas mentorias.
- Portfólio, como vitrine central de projetos, pesquisas, extensão, produção científica, startups e premiações.
- Repositório Científico, com artigos, resumos, patentes e produções vinculadas aos eixos.
- Transparência, com editais, atas, homologações, julgamentos de recursos, resultados e comunicados.
- Capacitação & Cursos, com trilhas, bootcamps, workshops, simpósios, palestras e materiais.
- Notícias / Blog / Jornal Trimestral, com artigos, eventos, premiações e registros da rotina da liga.
- Contato & Parcerias, com formulário parametrizado e canais oficiais.

## Eixos de atuação

Os eixos de atuação são parte central da arquitetura informacional da plataforma. Eles devem organizar projetos, publicações, cursos, eventos e produções científicas.

Eixos iniciais:

1. Etnobotânica e Pós-Colheita.
2. Práticas em Laboratório e Nanotecnologia.
3. Nutrição e Ciências dos Alimentos.
4. Saúde e bem-estar.
5. Produção Vegetal e Biotecnologia.
6. Agroindustrialização.
7. Redação Científica.

## Papel da plataforma web

A plataforma web deve cumprir quatro funções institucionais:

- Transparência: editais, atas, homologações e julgamentos de recursos.
- Repositório científico: artigos, resumos, patentes e produções vinculadas aos eixos.
- Vitrine biotecnológica: patentes, bioprodutos e soluções das startups ou projetos parceiros.
- Difusão e extensão: inscrições e divulgação de simpósios, cursos e palestras abertas.

## Direção técnica

- Linguagem principal: Python.
- Framework backend: Django.
- API: Django REST Framework.
- API pública versionada em `/api/v1/`.
- Administração inicial: Django Admin.
- Autenticação administrativa com usuário padrão do Django.
- Banco de dados em produção: PostgreSQL.
- Banco de dados local inicial: SQLite.
- Armazenamento local em desenvolvimento.
- Volumes persistentes no servidor para homologação e produção.
- Documentação de API: OpenAPI, preferencialmente com `drf-spectacular`.

## Premissas

- O Django Admin será suficiente para o CMS inicial.
- Nem toda pessoa cadastrada como membro da liga será usuária administrativa.
- Professores, orientadores e mentores poderão cadastrar publicações referentes aos seus eixos de atuação.
- A publicação final ficará sob responsabilidade da coordenação.
- Conteúdos públicos devem possuir controle de publicação.
- Conteúdos com página própria devem possuir `slug`.
- Arquivos e imagens devem ser tratados como parte relevante da plataforma.
- A API pública deve facilitar a migração do atual `js/data.js` para chamadas HTTP.
