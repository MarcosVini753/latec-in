# Workflow editorial do portal LABTEC.IN

O portal usa um único campo de workflow e o escopo institucional do usuário para controlar edição e publicação.

## Status

```txt
draft       rascunho
in_review   em revisão
published   publicado
archived    arquivado
```

`editorial_status` é a única fonte de visibilidade dos conteúdos editoriais. Não existe `is_published` paralelo nem flag de destaque. `published_at` registra quando a publicação ocorreu.

## Fluxo

1. Coordenador de unidade ou mentor cria o conteúdo como `draft` dentro do escopo autorizado.
2. Completa os metadados, vínculos, arquivo ou texto necessários e escolhe se o registro participará do ecossistema da unidade mãe.
3. Move o registro para `in_review`.
4. A coordenação do LABTEC.IN revisa unidade, eixo, autoria, arquivo, direitos e a opção de ecossistema.
5. Superusuário ou coordenação do LABTEC.IN define `published`, `archived` ou devolve o conteúdo para ajuste.

Coordenadores de unidade e mentores não publicam, arquivam, excluem nem alteram registros já publicados.

## Conteúdos sujeitos ao workflow

- projetos de portfólio;
- pesquisas;
- trabalhos acadêmicos;
- produções científicas;
- notícias;
- cursos;
- documentos de transparência.

Banners e seções institucionais usam `is_published` simples, pois sua publicação é estrutural e não passa pelo workflow editorial completo.

`CourseMaterial` também não possui workflow próprio. O material herda o estado editorial do curso: todos os seus arquivos e links tornam-se públicos quando o curso está `published` e deixam de ser descobertos pela API quando o curso sai desse estado.

## Ecossistema da unidade mãe

`include_in_parent_ecosystem` é editável durante rascunho e revisão. Quando verdadeiro, um conteúdo publicado pode aparecer no filtro da mãe direta, preservando sua unidade proprietária. A publicação final também aprova essa inclusão.

## Proteções

- Todo conteúdo editorial exige unidade.
- Querysets, formulários, inlines, autocomplete, ações e validação do POST aplicam o mesmo escopo.
- A API pública oculta `draft`, `in_review` e `archived` independentemente do perfil administrativo.
- Slugs publicados não são recalculados automaticamente.
