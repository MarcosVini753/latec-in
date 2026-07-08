# Diagrama C4 — Contexto

```mermaid
flowchart LR
  Visitor[Visitante público] --> Site[Portal LATEC.IN]
  Member[Membro da liga] --> Site
  Partner[Parceiro institucional] --> Site
  Mentor[Professor ou mentor] --> Admin[Django Admin]
  Coordinator[Coordenadora] --> Admin

  Site --> API[API pública /api/v1]
  Admin --> Backend[Backend Django]
  API --> Backend

  Backend --> DB[(PostgreSQL)]
  Backend --> Media[Volume de mídia]
  Site --> Social[Redes sociais e canais oficiais]
```

O visitante público consome páginas e dados publicados. Mentores e coordenadora usam o Django Admin. O backend persiste dados em PostgreSQL e gerencia arquivos no volume de mídia.
