# Estrutura institucional do portal LABTEC.IN

## Motivação

A arquitetura anterior tratava a LATEC.IN como proprietária direta do portal. A organização institucional aprovada estabelece:

- LABTEC.IN — Laboratório de Biotecnologia, Biodiversidade e Inovação — como instituição raiz;
- LATEC como liga acadêmica ou iniciativa vinculada ao laboratório;
- possibilidade de futuras unidades sem remodelar todos os conteúdos.

Essa mudança exige uma camada institucional genérica, em vez de renomear textos ou adicionar booleanos específicos.

## Estado implementado

O backend atual:

- possui o app `institutional`, com `InstitutionalUnit` e `InstitutionMembership`;
- cria LABTEC.IN e LATEC por seed idempotente;
- expõe unidades ativas e públicas em `/api/v1/institutional-units/`;
- associa conteúdos a unidades e parceiros a uma ou mais unidades;
- preserva `Person.role`, mas usa memberships para os papéis por unidade;
- cria 43 memberships no seed, incluindo nove mentores da LATEC;
- associa explicitamente os sete eixos à LATEC;
- aplica escopo administrativo por unidade, descendência e eixo.

Referências persistidas à antiga identificação LATEC.IN são tratadas somente por fallback de compatibilidade, sem alterar os slugs públicos.

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

O banco impede `parent_id == id`. O preflight anterior à constraint informa os IDs de qualquer ciclo existente, inclusive indireto. `clean()` percorre ancestrais e rejeita ciclos indiretos; `save()` chama a validação para Admin, seed e gravações ORM comuns. O manager impede `bulk_create()` de inserir unidades com pai e impede mudanças de pai por `bulk_update()`. `QuerySet.update()` não executa `save()` e continua sendo o único caminho ORM capaz de contornar essa validação; seu uso deve garantir a integridade explicitamente.

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

A combinação `(person, unit, role)` é única. Datas podem ser nulas, mas `end_date` não pode anteceder `start_date`. As regras existem no modelo e em constraints de banco. Uma migration de preflight lista os IDs de duplicatas ou períodos inválidos e falha antes de criar as constraints, sem apagar dados.

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
- manter unidade opcional nos modelos legados durante a migração e exigi-la nos novos models de `research`;
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

## Consultas públicas

- `?unit=labtec-in` e `?unit=latec` filtram propriedade direta, sem agregarem descendentes implicitamente;
- a Home retorna exclusivamente conteúdo direto do LABTEC.IN;
- a API oferece o recorte LATEC por `?unit=latec`;
- agregação futura não alterará a propriedade do conteúdo.

## Permissões

- Superusuário e administrador: todas as unidades e conteúdo sem unidade.
- Coordenação do LABTEC.IN: unidade raiz, descendentes, conteúdo sem unidade e publicação final.
- Coordenação de unidade e editor: unidades autorizadas, sem publicação final.
- Mentor da LATEC: somente os próprios eixos, sem publicação final.
- Reader: somente leitura nas unidades autorizadas.

O acesso a descendentes deve ser uma permissão declarada, não uma consequência automática para todos os papéis.

## Futuras unidades

Novos programas, grupos de pesquisa ou iniciativas serão criados como `InstitutionalUnit` com `parent` adequado. Os conteúdos existentes reutilizarão o mesmo campo `unit`, sem novas colunas específicas.

## Estado da migração

LABTEC.IN, LATEC, memberships, `unit` opcional, backfill inicial, filtros públicos e escopo do Admin estão implementados. Permanecem para etapas posteriores a obrigatoriedade dos campos institucionais legados, a retirada de `Person.role`, o frontend e a eventual agregação da Home.

O detalhamento e o corte dos legados estão em [Migração para a arquitetura LABTEC.IN](12-migracao-labtec.md).
