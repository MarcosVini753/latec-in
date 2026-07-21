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

Os containers técnicos permanecem os mesmos. A seção LATEC usa `?unit=latec` na mesma API; recortes institucionais podem incluir conteúdo de filhas diretas que tenha optado pelo ecossistema da unidade consultada. O volume guarda arquivos referenciados diretamente pelos modelos de domínio, sem catálogo ou container MediaHub.
