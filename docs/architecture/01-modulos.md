# Módulos do backend

O backend será dividido em apps Django por domínio.

## Apps planejados

- `accounts`: autenticação, perfis administrativos e permissões.
- `core`: configurações institucionais, hero, seções e links sociais.
- `people`: membros, professores, coordenadores, ligantes e pesquisadores.
- `axes`: eixos de atuação da LATEC.IN e suas mentorias.
- `portfolio`: projetos, categorias, resultados, equipe, links e anexos.
- `scientific`: repositório científico, artigos, resumos, patentes e produções vinculadas aos eixos.
- `news`: notícias, blog, editais editoriais, jornal e tags.
- `learning`: cursos, trilhas, workshops, simpósios, palestras e materiais.
- `transparency`: editais, atas, homologações, julgamentos de recursos e comunicados institucionais.
- `mediahub`: imagens, documentos, PDFs e arquivos reutilizáveis.
- `partnerships`: parceiros e mensagens de contato.
- `metrics`: números de impacto da Home.

## Dependências principais

- `axes` é uma entidade central para projetos, publicações científicas, posts e cursos.
- `people` se relaciona com `axes`, `portfolio`, `scientific`, `news` e `learning`.
- `mediahub` se relaciona com `core`, `portfolio`, `scientific`, `news`, `learning` e `transparency`.
- `metrics` consolida dados públicos para a Home.
- `accounts` protege a área administrativa.

## Papel da plataforma web

A plataforma web deve contemplar quatro funções institucionais: transparência, repositório científico, vitrine biotecnológica e difusão/extensão.
