# Permissões e acesso administrativo

## Papéis iniciais

- Administrador: acesso completo ao Django Admin.
- Coordenador: gerencia conteúdos institucionais, projetos, notícias, membros, cursos e parceiros.
- Editor: cadastra e edita notícias, cursos, materiais e projetos, conforme permissão.
- Leitor administrativo: visualiza registros internos, sem alterar conteúdo.

## Decisões

Nem toda pessoa exibida no site será usuária administrativa. O modelo de pessoas será separado do modelo de usuários. Mensagens de contato não devem ser públicas. Conteúdos editoriais devem ter controle de publicação.

## Segurança

A produção deve usar HTTPS, variáveis de ambiente para segredos, permissões explícitas no admin e proteção básica contra vulnerabilidades comuns. A plataforma deve respeitar princípios da LGPD, evitando coleta desnecessária de dados pessoais.
