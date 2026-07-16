# Estrutura institucional do portal LABTEC.IN

## Motivação

A arquitetura anterior tratava a LATEC.IN como proprietária direta do portal. A organização institucional aprovada estabelece:

- LABTEC.IN — Laboratório de Biotecnologia, Biodiversidade e Inovação — como instituição raiz;
- LATEC como liga acadêmica ou iniciativa vinculada ao laboratório;
- possibilidade de futuras unidades sem remodelar todos os conteúdos.

Essa mudança exige uma camada institucional genérica, em vez de renomear textos ou adicionar booleanos específicos.

## Estado implementado

O backend atual:

- não possui app `institutional`;
- guarda nome e instituição em campos textuais de `SiteSettings`;
- representa uma pessoa com um papel público principal;
- não associa conteúdos a uma unidade;
- trata os sete eixos como estrutura central sem vínculo explícito com a LATEC.

As referências à LATEC.IN como instituição raiz são históricas e deverão ser migradas gradualmente no código e nos dados.

## Hierarquia alvo

```txt
LABTEC.IN
├── conteúdos institucionais do laboratório
├── pessoas e vínculos institucionais
├── pesquisas e trabalhos acadêmicos
├── produções científicas
├── projetos e soluções
├── notícias, cursos e eventos
├── transparência, parceiros e métricas
└── LATEC
    ├── ligantes
    ├── mentores
    ├── sete eixos de atuação
    └── conteúdos próprios da Liga
```

LABTEC.IN não é apenas um rótulo visual: é a unidade proprietária do portal e a raiz da hierarquia.

## `InstitutionalUnit`

`institutional.InstitutionalUnit` representa qualquer unidade organizacional.

Campos conceituais:

- `id`;
- `name`;
- `acronym`;
- `slug`;
- `unit_type`;
- `parent`;
- `description`;
- `mission`;
- `vision`;
- `logo`;
- `cover_image`;
- `contact_email`;
- `website_url`;
- `is_active`;
- `is_public`;
- `display_order`;
- timestamps.

Tipos iniciais:

- `laboratory`;
- `academic_league`;
- `program`;
- `research_group`;
- `initiative`.

Dados iniciais:

| Nome | Slug | Tipo | Pai |
| --- | --- | --- | --- |
| LABTEC.IN | `labtec-in` | `laboratory` | nenhum |
| LATEC | `latec` | `academic_league` | LABTEC.IN |

## `InstitutionMembership`

`institutional.InstitutionMembership` representa o papel de uma pessoa em uma unidade e em um período.

Campos conceituais:

- `person`;
- `unit`;
- `role`;
- `start_date`;
- `end_date`;
- `is_active`;
- `is_public`;
- `display_order`;
- timestamps.

O vínculo não substitui `people.Person`; ele acrescenta contexto institucional.

Exemplo:

| Pessoa | Unidade | Papel |
| --- | --- | --- |
| Marta Adelino | LABTEC.IN | Coordenadora |
| Marta Adelino | LABTEC.IN | Pesquisadora |
| Marta Adelino | LATEC | Coordenadora |
| Marta Adelino | LATEC | Mentora de eixo |

## Propriedade dos conteúdos

Todo conteúdo é gerenciado dentro da estrutura do LABTEC.IN.

Um conteúdo pode pertencer:

- diretamente ao LABTEC.IN;
- à LATEC;
- a uma futura unidade.

Regras:

- usar relação com `InstitutionalUnit`;
- não criar `is_latec`, `belongs_to_latec` ou equivalentes;
- manter eixo separado de unidade;
- permitir unidade opcional apenas durante migração ou em casos técnicos documentados;
- validar a compatibilidade entre eixo e unidade; uma pesquisa do LABTEC.IN pode se relacionar explicitamente com um eixo da unidade filha LATEC.

## Escopo inicial por domínio

| Domínio | LABTEC.IN | LATEC |
| --- | --- | --- |
| Institucional | Home, missão, visão, contatos | Perfil e seções próprias |
| Pessoas | Coordenação, pesquisadores, professores | Ligantes, mentores e coordenação da Liga |
| Eixos | Não organiza globalmente o laboratório | Sete eixos |
| Pesquisa | Pesquisas e trabalhos acadêmicos | Relação opcional por unidade ou eixo |
| Portfólio | Projetos e soluções do laboratório | Projetos específicos |
| Produção científica | Produção geral | Produção específica |
| Notícias e aprendizagem | Conteúdo geral | Conteúdo específico |
| Transparência | Documentos institucionais | Documentos próprios, quando existirem |
| Métricas | Valores diretos ou agregados | Valores próprios |

## Regras de agregação

A unidade raiz poderá agregar conteúdos ou métricas de descendentes quando a consulta ou métrica declarar esse comportamento.

- conteúdo direto: pertence exatamente à unidade solicitada;
- conteúdo agregado: inclui a unidade e suas descendentes;
- a API deve tornar esse comportamento explícito;
- a Home do LABTEC.IN pode usar agregação;
- a seção LATEC usa somente o recorte da LATEC, salvo vínculo editorial explícito.

Agregação não altera propriedade: um conteúdo da LATEC continua pertencendo à LATEC mesmo quando aparece na Home do laboratório.

## Permissões

- Coordenador do LABTEC.IN: unidade raiz e descendentes.
- Coordenador de unidade: unidade atribuída.
- Mentor da LATEC: unidade LATEC e próprios eixos.

O acesso a descendentes deve ser uma permissão declarada, não uma consequência automática para todos os papéis.

## Futuras unidades

Novos programas, grupos de pesquisa ou iniciativas serão criados como `InstitutionalUnit` com `parent` adequado. Os conteúdos existentes reutilizarão o mesmo campo `unit`, sem novas colunas específicas.

## Migração resumida

1. Criar LABTEC.IN e LATEC.
2. Adicionar memberships.
3. Adicionar `unit` opcional aos conteúdos.
4. Classificar e preencher os registros existentes.
5. Atualizar API, Admin, permissões e frontend.
6. Tornar vínculos obrigatórios onde fizer sentido.
7. Retirar nomes e campos legados.

O detalhamento está em [Migração para a arquitetura LABTEC.IN](12-migracao-labtec.md).
