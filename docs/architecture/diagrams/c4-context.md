# Diagrama C4 — Contexto do portal LABTEC.IN

```mermaid
flowchart LR
  Visitor["Visitante público"] --> Portal["Portal LABTEC.IN"]
  Researcher["Pesquisador ou professor"] --> Portal
  Researcher --> Admin["Django Admin"]
  Mentor["Mentor da LATEC"] --> Admin
  Coordinator["Coordenador do LABTEC.IN"] --> Admin

  Portal -->|contém| Latec["Seção LATEC<br/>recorte institucional"]
  Portal --> API["API pública /api/v1/"]
  Latec --> API
  Admin --> Backend["Backend Django"]
  API --> Backend

  Backend --> DB[(PostgreSQL)]
  Backend --> Media["Volume de mídia"]
```

O portal pertence ao LABTEC.IN. A LATEC é uma unidade e seção dentro do mesmo sistema, não uma aplicação separada. Visitantes consomem conteúdo público; pesquisadores, professores, mentores e coordenação usam o Django Admin conforme suas permissões institucionais.
