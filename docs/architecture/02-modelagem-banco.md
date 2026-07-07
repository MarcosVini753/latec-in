# Modelagem inicial do banco de dados — LATEC.IN

## Convenções gerais

Todos os modelos devem possuir `id`, `created_at` e `updated_at`. Conteúdos públicos devem possuir `is_published`. Conteúdos com página própria devem possuir `slug`. Entidades editoriais devem ter status, data de publicação e possibilidade de destaque na Home quando fizer sentido.

## Apps considerados

- accounts: usuários administrativos, perfis e auditoria.
- core: configurações institucionais, hero, seções da Home e links sociais.
- people: membros, professores, ligantes, pesquisadores e linhas de atuação.
- portfolio: projetos, categorias, resultados, links, equipe e anexos.
- news: notícias, blog, editais, jornal e tags.
- learning: cursos, trilhas, workshops, materiais e instrutores.
- mediahub: imagens, documentos, PDFs e arquivos reutilizáveis.
- partnerships: parceiros e mensagens de contato.
- metrics: números de impacto da Home.

## Entidades iniciais

`Person` representa pessoas exibidas no site. `User` representa acesso administrativo. A separação evita transformar todos os membros em usuários do sistema.

`Project` será a entidade central do portfólio. Deve se relacionar com categorias, equipe, resultados, links e anexos.

`Post` concentrará notícias, editais, artigos institucionais e registros do jornal/blog.

`Course` representará capacitações, bootcamps, workshops e trilhas.

`MediaAsset` será usado para imagens, PDFs, e-books, livros, documentos técnicos e anexos reaproveitáveis.

`ImpactMetric` poderá armazenar métricas manuais ou calculadas para exibição na Home.
