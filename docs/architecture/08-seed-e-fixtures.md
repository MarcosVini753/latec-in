# Seed e fixtures iniciais

O backend deve nascer com dados mínimos para facilitar desenvolvimento, homologação e migração do protótipo.

## Estratégia

Usaremos dados iniciais em fixtures e/ou comando idempotente de seed.

A estratégia recomendada é criar um comando:

```txt
python manage.py seed_initial_data
```

Esse comando deve criar ou atualizar registros básicos sem duplicar dados já existentes.

## Dados iniciais previstos

```txt
backend/apps/people/fixtures/initial_roles.json
backend/apps/people/fixtures/initial_people.json
backend/apps/axes/fixtures/initial_research_axes.json
backend/apps/portfolio/fixtures/initial_project_categories.json
backend/apps/news/fixtures/initial_post_categories.json
backend/apps/learning/fixtures/initial_course_statuses.json
backend/apps/core/fixtures/initial_site_settings.json
backend/apps/transparency/fixtures/initial_transparency_types.json
```

## Eixos iniciais

O seed inicial deve incluir os sete eixos de atuação da LATEC.IN:

1. Etnobotânica e Pós-Colheita.
2. Práticas em Laboratório e Nanotecnologia.
3. Nutrição e Ciências dos Alimentos.
4. Saúde e bem-estar.
5. Produção Vegetal e Biotecnologia.
6. Agroindustrialização.
7. Redação Científica.

## Categorias iniciais

### Projetos

- Ensino;
- Pesquisa;
- Extensão;
- Produção Científica;
- Startup;
- Premiação.

### Transparência

- Edital;
- Ata;
- Homologação;
- Julgamento de recurso;
- Resultado;
- Comunicado.

### Produção científica

- Artigo;
- Resumo;
- Patente;
- E-book;
- Livro;
- Relatório técnico;
- Projeto;
- Produção científica.

## Observação

Os dados atuais de `js/data.js` devem ser usados como base temporária para gerar fixtures, mas a modelagem do backend passa a ser a fonte principal de verdade.
