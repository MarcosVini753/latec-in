# Deploy e ambientes

## Ambientes previstos

### Desenvolvimento local

Ambiente usado por desenvolvedores.

Características:

- SQLite permitido no início.
- `DEBUG=True`.
- arquivos locais para mídia.
- CORS liberado apenas para frontend local.

### Homologação

Ambiente para validação antes da publicação.

Características:

- PostgreSQL.
- `DEBUG=False`.
- domínio ou subdomínio de teste.
- dados próximos da produção.
- validação de fluxo administrativo e API.

### Produção institucional

Ambiente público do portal.

Características:

- PostgreSQL.
- HTTPS obrigatório.
- variáveis de ambiente.
- backups.
- configuração de arquivos estáticos e mídia.
- domínio institucional quando definido.

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
