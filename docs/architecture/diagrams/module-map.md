# Mapa de relações de modelo consolidadas

```mermaid
flowchart LR
  accounts --> institutional
  accounts --> people
  institutional --> people

  core --> institutional
  axes --> institutional
  axes --> people

  research --> institutional
  research --> axes
  research --> people

  portfolio --> institutional
  portfolio --> axes
  portfolio --> people

  scientific --> institutional
  scientific --> axes
  scientific --> research
  scientific --> people

  news --> institutional
  news --> axes

  learning --> institutional
  learning --> axes
  learning --> people

  transparency --> institutional
  partnerships --> institutional
  metrics --> institutional
```

Cada seta parte do app que mantém a FK ou M2M e aponta para o app referenciado. Relações internas e o autorrelacionamento de `InstitutionalUnit` foram omitidos.

`common` fornece `BaseModel`, workflow, viewsets e escopo administrativo sem relações próprias de banco. Arquivos pertencem aos apps de domínio; não existe app central de mídia no grafo ou em `INSTALLED_APPS`.
