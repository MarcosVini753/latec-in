# Deploy e ambientes

## Ambientes previstos

- Desenvolvimento local.
- Homologação.
- Produção institucional.

## Stack recomendada

- Django.
- Django REST Framework.
- PostgreSQL em homologação e produção.
- SQLite apenas no desenvolvimento inicial.
- Servidor ASGI/WSGI conforme estratégia de implantação.
- Arquivos estáticos e mídia configurados separadamente.

## Premissas

A implantação final deve considerar domínio institucional, HTTPS, backups do banco, controle de variáveis de ambiente e processo claro de atualização.
