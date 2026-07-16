# Workflow editorial do portal LABTEC.IN

O workflow continua simples e compatível com o Django Admin, mas passa a considerar a unidade proprietária do conteúdo e o escopo institucional do usuário.

## Estado implementado

O backend já define os status editoriais e filtra conteúdos públicos por publicação. Projetos, produções científicas, posts, cursos, eventos e documentos de transparência possuem campos editoriais, embora os nomes ainda variem entre `status` e `editorial_status`.

Ainda não há escopo por unidade nem distinção técnica entre coordenação do laboratório e coordenação de unidade.

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
- Todo conteúdo aplicável possui uma unidade proprietária.
- O usuário só edita conteúdo dentro de seu escopo institucional.

## Fluxo

1. O autor cria o conteúdo como `draft` em uma unidade autorizada.
2. O autor envia o conteúdo como `in_review`.
3. A coordenação competente revisa unidade, autoria, vínculos e conteúdo.
4. A coordenação publica, arquiva ou devolve para ajuste.

## Coordenação

- A coordenação do LABTEC.IN pode revisar e publicar conteúdo da unidade raiz e das unidades descendentes.
- A coordenação de unidade pode revisar e publicar apenas em sua unidade, quando essa permissão estiver habilitada.
- A publicação final continua sendo responsabilidade da coordenação.

## Mentores da LATEC

- Criam e editam conteúdos dos próprios eixos.
- Atuam dentro da unidade LATEC.
- Enviam conteúdo para revisão.
- Não publicam diretamente, salvo permissão adicional.

## Conteúdos sujeitos ao workflow

- pesquisas;
- trabalhos acadêmicos;
- projetos e soluções;
- produções científicas;
- notícias e posts;
- cursos e eventos;
- documentos de transparência;
- seções institucionais quando aplicável.

## Migração

1. Adicionar `unit` opcional.
2. Classificar os conteúdos existentes.
3. Adicionar escopo de unidade aos usuários.
4. Aplicar validação no Django Admin e na camada de API.
5. Tornar a unidade obrigatória onde fizer sentido.

Durante a transição, o workflow atual permanece válido; o escopo institucional é acrescentado sem alterar seus quatro status.
