# Workflow editorial do portal LABTEC.IN

O workflow continua simples e compatível com o Django Admin e considera a unidade proprietária do conteúdo e o escopo institucional do usuário.

## Estado implementado

O backend define os status editoriais, filtra conteúdos públicos por publicação e aplica no Admin o escopo de unidade e eixo. Projetos, pesquisas, trabalhos acadêmicos, produções científicas, posts, cursos, eventos e documentos de transparência possuem campos editoriais, embora modelos legados ainda variem entre `status` e `editorial_status`.

## Status editoriais

```txt
draft       -> rascunho
in_review   -> em revisão
published   -> publicado
archived    -> arquivado
```

## Regras gerais

- Visitantes acessam somente conteúdos publicados.
- Conteúdos publicados devem combinar status `published` e `is_published=True`.
- Conteúdos com página pública possuem `slug`.
- `published_at` registra a publicação quando aplicável.
- Novas pesquisas e trabalhos exigem unidade; conteúdos legados ainda podem permanecer sem unidade durante o backfill.
- O usuário só edita conteúdo dentro de seu escopo institucional.

## Fluxo

1. O autor cria o conteúdo como `draft` em uma unidade autorizada.
2. O autor envia o conteúdo como `in_review`.
3. A coordenação revisa unidade, autoria, vínculos e conteúdo.
4. Administrador ou coordenação do LABTEC.IN publica, arquiva ou devolve para ajuste.

## Coordenação

- A coordenação do LABTEC.IN pode revisar e publicar conteúdo da unidade raiz e das unidades descendentes.
- A coordenação de unidade pode criar, editar e revisar rascunhos em seu escopo, mas não publica nem arquiva.
- Apenas superusuário, administrador e coordenação do LABTEC.IN realizam publicação final.

## Mentores da LATEC

- Criam e editam conteúdos dos próprios eixos.
- Atuam dentro da unidade LATEC.
- Enviam conteúdo para revisão.
- Não publicam nem arquivam.

## Conteúdos sujeitos ao workflow

- pesquisas;
- trabalhos acadêmicos;
- projetos e soluções;
- produções científicas;
- notícias e posts;
- cursos e eventos;
- documentos de transparência;
- seções institucionais quando aplicável.

## Proteções administrativas

- Mentores, editores e coordenadores de unidade não alteram registros já publicados.
- Querysets, formulários, inlines, autocomplete, ações e POSTs validam o mesmo escopo.
- Conteúdo sem unidade é restrito a administrador e coordenação do LABTEC.IN.
- A API pública continua somente leitura e oculta rascunhos, independentemente do perfil administrativo.
