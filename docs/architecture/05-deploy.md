# Deploy e ambientes do portal LABTEC.IN

A mudança institucional não altera a estratégia técnica de implantação. O mesmo frontend, backend Django, Django Admin e API `/api/v1/` atendem o LABTEC.IN e suas unidades, incluindo a seção LATEC.

## Ambientes previstos

### Desenvolvimento local

- SQLite permitido no início.
- `DEBUG=True`.
- arquivos locais para mídia.
- CORS liberado apenas para o frontend local.
- mídia em diretório local por `MEDIA_ROOT`.

### Homologação

- PostgreSQL.
- `DEBUG=False`.
- domínio ou subdomínio de teste a definir.
- dados próximos da produção.
- validação do fluxo administrativo, escopo institucional e API.
- mídia em volume persistente no servidor.

### Produção institucional

- PostgreSQL.
- HTTPS obrigatório.
- variáveis de ambiente.
- backups.
- configuração de arquivos estáticos e mídia.
- domínio institucional quando definido.
- mídia em volume persistente no servidor inicialmente.

Nenhum domínio definitivo é estabelecido por esta documentação.

## Stack

- Django.
- Django REST Framework.
- PostgreSQL em homologação e produção.
- SQLite apenas no desenvolvimento local inicial.
- `django-environ` ou alternativa equivalente para variáveis de ambiente.
- `django-cors-headers` para CORS.
- `Pillow` para campos de imagem.
- `drf-spectacular` para OpenAPI.
- servidor WSGI ou ASGI conforme a estratégia de implantação.

## Política de mídia

- Desenvolvimento: armazenamento local.
- Homologação: volume persistente no servidor.
- Produção: volume persistente no servidor inicialmente.

A migração futura para storage externo poderá ser avaliada se houver crescimento relevante, necessidade de CDN ou requisito institucional.

LABTEC.IN e LATEC compartilham a mesma infraestrutura de mídia. A propriedade lógica de um arquivo será representada por `mediahub.MediaAsset.unit`, sem separar volumes por unidade nesta fase.

## Configurações mínimas de produção

- `DEBUG=False`.
- `ALLOWED_HOSTS` configurado.
- origens confiáveis configuradas.
- CORS restrito aos domínios esperados.
- banco configurado por variável de ambiente.
- arquivos estáticos coletados por `collectstatic`.
- volume de mídia persistente e com backup.
- segredos fora do repositório.

## Backups

A produção deve possuir política mínima de backup para:

- PostgreSQL;
- arquivos de mídia;
- configurações de ambiente;
- procedimento testado de restauração.

## Migração institucional

Os apps `institutional` e `research` não exigem novos containers. A implantação deve fazer backup, executar o preflight institucional, aplicar as migrations incrementais, rodar o seed idempotente e validar o rascunho convertido antes de qualquer corte manual. Vínculos de unidade legados continuam opcionais.

## Premissas

A implantação final deve considerar domínio institucional, HTTPS, backups, controle de ambiente, persistência de mídia e processo claro de atualização, sem criar infraestrutura separada para a LATEC.
