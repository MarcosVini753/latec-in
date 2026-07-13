# Permissões e acesso administrativo

## Princípios

O visitante público acessa apenas conteúdos publicados. A equipe autorizada acessa o Django Admin conforme seu papel.

O modelo público de pessoas será separado do usuário administrativo. O sistema usará o usuário padrão do Django, com autenticação básica por usuário e senha.

## Papéis iniciais

- Administrador: acesso completo ao Django Admin.
- Coordenadora: gerencia conteúdos institucionais, usuários administrativos, eixos, publicações, mensagens de contato e publicação final.
- Mentor/Professor: cria e edita conteúdos referentes aos próprios eixos de atuação.
- Editor: cadastra e edita notícias, cursos, materiais e projetos conforme permissão.
- Leitor administrativo: visualiza registros internos, sem alterar conteúdo.

## Regras por eixo

- Cada professor, orientador ou mentor pode ser vinculado a um ou mais eixos.
- O mentor pode criar e editar publicações, projetos, cursos ou produções científicas referentes aos seus eixos.
- O mentor pode enviar conteúdo para revisão.
- A publicação final cabe à coordenadora.
- Visitantes públicos só visualizam conteúdos publicados.

## Conteúdos públicos

Conteúdos públicos devem possuir controle de publicação por `is_published`, `published_at`, `status` e `slug`, quando aplicável.

O workflow editorial inicial será `draft`, `in_review`, `published` e `archived`.

## Mensagens de contato

Mensagens de contato não devem ser públicas.

Na fase inicial, mensagens de contato ficarão armazenadas por tempo indeterminado e serão acessíveis somente pela coordenadora. Superusuários técnicos podem ter acesso operacional ao banco e ao admin, mas a regra funcional de uso será acesso restrito à coordenação.

## Decisões consolidadas

- Não haverá login por e-mail.
- Não haverá múltiplos tipos de autenticação na primeira versão.
- O sistema usará `User` padrão do Django.
- O vínculo entre usuário administrativo e pessoa pública será opcional via `Profile`.

## Decisões futuras

- Definir o nível de auditoria necessário para alterações editoriais.
- Definir política formal de revisão periódica das mensagens de contato.
