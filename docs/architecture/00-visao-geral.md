# Visão geral da arquitetura — LATEC.IN

A LATEC.IN é a Liga Acadêmica de Biotecnologia, Biodiversidade e Inovação. O portal deve funcionar como site institucional, vitrine de projetos e canal de comunicação entre a liga, a comunidade acadêmica, parceiros, setor produtivo e sociedade.

O projeto atual possui um protótipo frontend em HTML, CSS e JavaScript puro. O frontend simula uma SPA com rotas por hash e dados locais em `js/data.js`. A próxima etapa é criar um backend em Django para persistir os dados e permitir administração de conteúdo.

## Objetivo do backend

Construir uma plataforma backend para atuar como CMS institucional e API pública da LATEC.IN.

O backend deverá permitir gerenciar informações institucionais, membros, professores, coordenadores, ligantes, pesquisadores, projetos, notícias, cursos, materiais, arquivos, parceiros, mensagens de contato, métricas e permissões administrativas.

## Áreas públicas previstas

- Home, com hero section, destaques e números de impacto.
- Quem Somos, com histórico, propósito, missão, visão, valores, linhas de atuação e equipe.
- Portfólio, como vitrine central de projetos, pesquisas, extensão, produção científica, startups e premiações.
- Capacitação & Cursos, com trilhas, bootcamps, workshops e materiais.
- Notícias / Blog / Jornal Trimestral, com artigos, eventos, editais, premiações e registros da rotina da liga.
- Contato & Parcerias, com formulário parametrizado e canais oficiais.

## Direção técnica

- Linguagem principal: Python.
- Framework backend: Django.
- API: Django REST Framework.
- Administração inicial: Django Admin.
- Banco de dados em produção: PostgreSQL.
- Banco de dados local inicial: SQLite.
- Documentação de API: OpenAPI, preferencialmente com `drf-spectacular`.

## Premissas

- O Django Admin será suficiente para o CMS inicial.
- Nem toda pessoa cadastrada como membro da liga será usuária administrativa.
- Conteúdos públicos devem possuir controle de publicação.
- Conteúdos com página própria devem possuir `slug`.
- Arquivos e imagens devem ser tratados como parte relevante da plataforma.
- A API pública deve facilitar a migração do atual `js/data.js` para chamadas HTTP.
