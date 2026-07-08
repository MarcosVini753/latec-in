# Workflow editorial

O portal da LATEC.IN terá fluxo editorial simples, suficiente para o Django Admin e para a primeira versão da API.

## Status editoriais

```txt
draft       -> rascunho
in_review   -> em revisão
published   -> publicado
archived    -> arquivado
```

## Regras gerais

- Visitantes públicos só acessam conteúdos publicados.
- Conteúdos publicados devem ter `is_published=True` e status `published`.
- Conteúdos com página pública devem possuir `slug`.
- Conteúdos publicados devem registrar `published_at` quando aplicável.

## Fluxo de publicação

1. O autor cria o conteúdo como rascunho.
2. O autor envia o conteúdo para revisão.
3. A coordenação revisa o conteúdo.
4. A coordenação publica, arquiva ou devolve para ajuste.

## Professores, orientadores e mentores

Professores, orientadores e mentores poderão cadastrar conteúdos referentes aos seus eixos de atuação.

Regra inicial:

- o mentor pode criar e editar conteúdo do próprio eixo;
- o mentor pode enviar conteúdo para revisão;
- a coordenadora decide a publicação final;
- a API pública só exibe itens publicados.

## Conteúdos sujeitos ao workflow

- Projetos;
- produções científicas;
- notícias e posts;
- cursos, simpósios e palestras;
- documentos de transparência, quando aplicável.
