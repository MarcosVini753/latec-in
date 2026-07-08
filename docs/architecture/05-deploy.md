# Deploy e ambientes

## Ambientes previstos

### Desenvolvimento local

Ambiente usado por desenvolvedores.

Características:

- SQLite permitido no início.
- `DEBUG=True`.
- arquivos locais para mídia.
- CORS liberado apenas para frontend local.
- armazenamento de mídia em diretório local via `MEDIA_ROOT`.

### Homologação

Ambiente para validação antes da publicação.

Características:

- PostgreSQL.
- `DEBUG=False`.
- domínio ou subdomínio de teste.
- dados próximos da produção.
- validação de fluxo administrativo e API.
- armazenamento de mídia em volume persistente no servidor.

### Produção institucional

Ambiente público do portal.

Características:

- PostgreSQL.
- HTTPS obrigatório.
- variáveis de ambiente.
- backups.
- configuração de arquivos estáticos e mídia.
- domínio institucional quando definido.
- armazenamento de mídia em volume persistente no servidor inicialmente.

## Stack recomendada

- Django.
- Django REST Framework.
- PostgreSQL em homologação e produção.
- SQLite apenas no desenvolvimento local inicial.
- `django-environ` ou alternativa equivalente para variáveis de ambiente.
- `django-cors-headers` para CORS.
- `Pillow` para campos de imagem.
- `drf-spectacular` para documentação OpenAPI.
- Servidor WSGI/ASGI conforme estratégia de implantação.

## Política de mídia

- Desenvolvimento: armazenamento local.
- Homologação: volume persistente no servidor.
- Produção: volume persistente no servidor inicialmente.

A migração futura para storage externo poderá ser avaliada se houver crescimento relevante de arquivos, necessidade de CDN ou necessidade institucional específica.

## Configurações mínimas de produção

- `DEBUG=False`.
- `ALLOWED_HOSTS` configurado.
- origens confiáveis configuradas.
- CORS restrito aos domínios esperados.
- banco configurado por variável de ambiente.
- arquivos estáticos coletados por `collectstatic`.
- estratégia definida para mídia enviada por administradores.

## Backups

A produção deve possuir política mínima de backup para banco de dados, arquivos de mídia e configurações de ambiente.

## Premissas

A implantação final deve considerar domínio institucional, HTTPS, backups, controle de ambiente e processo claro de atualização.
