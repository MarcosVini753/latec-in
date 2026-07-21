# Pesquisas e trabalhos acadêmicos do LABTEC.IN

O domínio científico separa processo de pesquisa, trabalho acadêmico, produção publicada e resultado prático. Todos os registros possuem unidade obrigatória e workflow editorial único.

## Delimitação

| Domínio | Pergunta respondida |
| --- | --- |
| `ResearchProject` | Qual pesquisa formal está sendo ou foi executada? |
| `AcademicWork` | Qual trabalho acadêmico foi apresentado e por quem? |
| `ScientificOutput` | Qual resultado científico foi publicado? |
| `portfolio.Project` | Qual solução, produto ou iniciativa prática foi desenvolvida? |

Um mesmo esforço pode gerar registros relacionados nos quatro domínios sem tratá-los como o mesmo conteúdo.

## Pesquisa

`ResearchProject` mantém somente os metadados necessários para catálogo e descoberta:

- unidade e eixo opcional;
- título, slug e resumo curto;
- datas opcionais e situação da execução;
- arquivo e URL externa opcionais;
- `editorial_status`, `published_at` e opção de ecossistema;
- equipe ordenada.

Objetivos, metodologia e resultados esperados podem estar no arquivo anexado; não existem campos textuais independentes nem capa específica. Arquivo e URL podem coexistir.

`project_status` aceita `planned`, `in_progress`, `completed`, `suspended` e `canceled`. Quando ambas existem, a data final não pode anteceder a inicial.

### Equipe

`ResearchProjectMember` relaciona pessoa, pesquisa, papel e ordem. Os papéis são coordenador, pesquisador, orientador, bolsista, voluntário e colaborador. O papel `coordinator` é a única indicação de coordenação; cada pessoa aparece uma vez por pesquisa.

## Trabalho acadêmico

`AcademicWork` registra:

- unidade e pesquisa opcional;
- título, slug e tipo;
- curso, instituição e ano;
- resumo e palavras-chave;
- arquivo e URL externa;
- workflow, data de publicação e opção de ecossistema;
- contribuidores ordenados.

Os tipos são TCC, monografia, iniciação científica, dissertação, tese e outro.

`AcademicWorkContributor` relaciona pessoa, papel e ordem. Uma pessoa pode acumular papéis diferentes; `(academic_work, person, role)` é único.

## Produção científica

`ScientificOutput` registra:

- unidade, eixo, pesquisa e trabalho acadêmico relacionados;
- título, slug e tipo;
- abstract e data de publicação bibliográfica;
- arquivo e URL externa;
- workflow, data editorial e opção de ecossistema;
- autoria estruturada.

Os tipos são artigo, resumo, patente, e-book, livro, relatório técnico e outro. Os antigos tipos genéricos de projeto e produção científica foram normalizados como `other`.

`ScientificAuthorship` contém pessoa, ordem única e papel textual opcional. Não existe campo paralelo de autores livres; autoria deve ser cadastrada como pessoa antes do corte.

## API

```txt
GET /api/v1/research-projects/
GET /api/v1/research-projects/{slug}/
GET /api/v1/academic-works/
GET /api/v1/academic-works/{slug}/
GET /api/v1/scientific-outputs/
GET /api/v1/scientific-outputs/{slug}/
```

Exemplos:

```txt
GET /api/v1/research-projects/?unit=labtec-in
GET /api/v1/research-projects/?axis=praticas-em-laboratorio-e-nanotecnologia
GET /api/v1/academic-works/?work_type=tcc&year=2026
GET /api/v1/scientific-outputs/?unit=latec
```

Pesquisas aceitam `unit`, `axis`, `project_status`, `year` e `search`. Trabalhos aceitam `unit`, `work_type`, `year` e `search`. Produções aceitam `unit`, `axis`, `year` e `search`.

Somente `editorial_status=published` é retornado. Pesquisa inclui equipe, trabalho inclui pesquisa resumida e contribuidores, e produção inclui relações e autorias resumidas sem ciclos de serialização.

## Ecossistema institucional

Um registro pertence a uma única unidade. `include_in_parent_ecosystem=True` permite que um conteúdo de uma filha direta também apareça no filtro da mãe. A unidade serializada continua sendo a proprietária original e a agregação não alcança netos.

## Corte de Bioativos

`pesquisa-de-bioativos-da-amazonia` é uma `ResearchProject` publicada da LATEC, mesmo sem arquivo. O projeto de portfólio de origem foi arquivado e desvinculado da classificação histórica.

A conversão preservou título, slug, unidade, eixo, resumo e equipe semanticamente compatíveis. Não inferiu metodologia, autoria científica, instituição ou datas. Depois da validação e publicação, foram removidos o identificador técnico de proveniência e as categorias históricas `pesquisa` e `producao-cientifica`.

## Validações editoriais

Antes de publicar, a coordenação deve confirmar unidade, eixo, equipe/autoria, direitos do arquivo, resumo público, datas e tipo documental. O arquivo pode ficar ausente quando a instituição decidir publicar somente os metadados.
