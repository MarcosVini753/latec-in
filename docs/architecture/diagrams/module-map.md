# Mapa de módulos alvo

```mermaid
flowchart LR
  institutional --> accounts
  institutional --> core
  institutional --> people
  institutional --> axes
  institutional --> research
  institutional --> portfolio
  institutional --> scientific
  institutional --> news
  institutional --> learning
  institutional --> transparency
  institutional --> mediahub
  institutional --> partnerships
  institutional --> metrics

  accounts --> people

  people --> axes
  people --> research
  people --> portfolio
  people --> scientific
  people --> news
  people --> learning

  axes --> research
  axes --> portfolio
  axes --> scientific
  axes --> news
  axes --> learning

  research --> scientific
  research --> portfolio

  mediahub --> core
  mediahub --> research
  mediahub --> portfolio
  mediahub --> scientific
  mediahub --> news
  mediahub --> learning
  mediahub --> transparency

  partnerships --> portfolio

  people --> metrics
  axes --> metrics
  research --> metrics
  portfolio --> metrics
  scientific --> metrics
  news --> metrics
  learning --> metrics
  transparency --> metrics
  partnerships --> metrics
```

As setas indicam conceitos fornecidos ou relações consumidas pelo módulo de destino. `institutional` é a raiz organizacional; `axes` organiza a LATEC; `research` separa pesquisa e trabalhos acadêmicos; `metrics` consolida indicadores por unidade.
