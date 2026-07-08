# ADR 0011: Usar armazenamento local e volumes no servidor

## Status

Aceita

## Contexto

O sistema terá uploads de imagens, PDFs, documentos, certificados, materiais e anexos. A primeira versão não usará storage externo.

## Decisão

Usar armazenamento local em desenvolvimento. Em homologação e produção, usar volumes persistentes no servidor inicialmente.

## Consequências positivas

- Reduz complexidade inicial.
- Evita dependência de serviços externos na primeira versão.
- Mantém compatibilidade com `FileField` e `ImageField` do Django.

## Riscos e cuidados

- Volumes devem ter backup.
- Migração futura para storage externo deve ser planejada se o volume de arquivos crescer.
