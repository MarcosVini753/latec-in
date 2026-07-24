# ADR 0006: Usar mediahub para arquivos e anexos

## Status

Superada pelo [ADR 0016](0016-simplificar-conteudo-e-cortar-legados.md).

## Estado atual

O app, o model, a tabela, o ContentType e as permissões do MediaHub foram removidos. Arquivos pertencem diretamente aos modelos de domínio. Órfãos são inventariados por `cleanup_orphan_media` e excluídos apenas com `--delete`, sem registro operacional permanente. O restante deste ADR é preservado somente como histórico da decisão superada.

## Contexto

Projetos, notícias, cursos, documentos de transparência e produções científicas podem compartilhar imagens, PDFs, e-books, livros, certificados, documentos técnicos e anexos.

Sem um módulo centralizado, arquivos tenderiam a ficar duplicados ou espalhados por vários modelos.

## Decisão

Criar o app `mediahub` para centralizar ativos de mídia e documentos reutilizáveis.

## Consequências positivas

- Menos duplicação de uploads.
- Melhor organização de arquivos e imagens.
- Possibilidade de metadados como tipo, descrição, texto alternativo e crédito.

## Riscos e cuidados

- Vários módulos dependerão de `mediahub`.
- Será necessário definir validação de tipo e tamanho de arquivo.
