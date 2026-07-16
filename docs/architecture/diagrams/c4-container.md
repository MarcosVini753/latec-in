# Diagrama C4 — Containers do portal LABTEC.IN

```mermaid
flowchart TB
  Browser["Navegador do usuário"]

  subgraph Portal [Portal LABTEC.IN]
    Frontend["Frontend público<br/>Home LABTEC.IN e seção LATEC"]
    Admin["Django Admin"]
    API["API REST /api/v1/"]
    Django["Aplicação Django"]
  end

  DB[(PostgreSQL)]
  Media["Volume de mídia"]

  Browser --> Frontend
  Browser --> Admin
  Frontend --> API
  Admin --> Django
  API --> Django
  Django --> DB
  Django --> Media
```

Os containers técnicos permanecem os mesmos. A seção LATEC é renderizada pelo frontend e filtrada pela unidade `latec` na mesma API e aplicação Django.
