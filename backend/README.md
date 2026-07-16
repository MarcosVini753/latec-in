# Backend do portal LABTEC.IN

Backend Django para atuar como CMS institucional e API pública do LABTEC.IN, tendo a LATEC como unidade vinculada.

## Rodando localmente

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements/dev.txt
cp .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py seed_initial_data
python manage.py createsuperuser
python manage.py runserver
```

O seed inicial cria LABTEC.IN e LATEC, associa as configurações centrais ao laboratório e popula eixos, papéis públicos, pessoas, projetos, notícias, cursos, métricas, hero e seções institucionais com base nos dados do protótipo atual.

## Validação

```bash
python manage.py test
python manage.py check
python manage.py spectacular --file /tmp/latec-openapi.yaml --validate
```

Endpoints principais:

- Admin: `http://127.0.0.1:8000/admin/`
- API pública: `http://127.0.0.1:8000/api/v1/`
- OpenAPI: `http://127.0.0.1:8000/api/schema/`
- Swagger UI: `http://127.0.0.1:8000/api/docs/`
