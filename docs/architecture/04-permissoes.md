# Permissões e acesso administrativo

## Princípios

O visitante público acessa apenas conteúdos publicados. A equipe autorizada acessa o Django Admin conforme seu papel.

O modelo público de pessoas será separado do usuário administrativo.

## Papéis iniciais

- Administrador: acesso completo ao Django Admin.
- Coordenador: gerencia conteúdos institucionais, projetos, notícias, membros, cursos e parceiros.
- Editor: cadastra e edita notícias, cursos, materiais e projetos conforme permissão.
- Leitor administrativo: visualiza registros internos, sem alterar conteúdo.

## Conteúdos públicos

Conteúdos públicos devem possuir controle de publicação por `is_published`, `published_at`, `status` e `slug`, quando aplicável.

A API pública deve retornar apenas itens publicados e ativos.

## Mensagens de contato

Mensagens de contato não devem ser públicas. Devem ficar restritas à área administrativa.

## Decisões abertas

- Definir se o projeto usará usuário customizado ou o `User` padrão do Django.
- Definir o nível de auditoria necessário para alterações editoriais.
- Definir a política de retenção de mensagens de contato.
