# Backend LATEC.IN

Backend Django para atuar como CMS institucional e API pública do portal LATEC.IN.

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

Endpoints principais:

- Admin: `http://127.0.0.1:8000/admin/`
- API pública: `http://127.0.0.1:8000/api/v1/`
- OpenAPI: `http://127.0.0.1:8000/api/schema/`
- Swagger UI: `http://127.0.0.1:8000/api/docs/`
