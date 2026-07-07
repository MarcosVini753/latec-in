# Módulos do backend

O backend será dividido em apps Django por domínio.

## Apps planejados

- `accounts`: autenticação, perfis e permissões.
- `core`: configurações institucionais, hero, seções e links sociais.
- `people`: membros, professores, coordenadores, ligantes e pesquisadores.
- `portfolio`: projetos, categorias, resultados, equipe, links e anexos.
- `news`: notícias, blog, editais, jornal e tags.
- `learning`: cursos, trilhas, workshops, materiais e instrutores.
- `mediahub`: imagens, documentos, PDFs e arquivos reutilizáveis.
- `partnerships`: parceiros e mensagens de contato.
- `metrics`: números de impacto da Home.

## Dependências principais

- `people` se relaciona com `portfolio`, `news` e `learning`.
- `mediahub` se relaciona com `portfolio`, `news`, `learning` e `core`.
- `metrics` consolida dados públicos para a Home.
- `accounts` protege a área administrativa.
