# Transparência, repositório científico e vitrine do LABTEC.IN

O portal do LABTEC.IN cumpre funções públicas de transparência, preservação acadêmica, difusão científica e apresentação de soluções. Conteúdos específicos da LATEC são identificados pela unidade `latec`.

## Estado implementado

O backend possui:

- `transparency.TransparencyDocument`;
- `scientific.ScientificOutput`;
- `portfolio.Project`;
- cursos e eventos em `learning`;
- arquivos em `mediahub`.

`TransparencyDocument`, `ScientificOutput`, `Project` e `MediaAsset` possuem unidade institucional opcional durante a transição. `research` modela pesquisas e trabalhos acadêmicos, e `ScientificAuthorship` registra autoria interna ordenada.

## Transparência

O app `transparency` mantém editais, atas, homologações, julgamentos de recursos, resultados e comunicados.

Regras implementadas:

- cada documento pode possuir `unit` durante a transição;
- o padrão institucional é LABTEC.IN;
- a LATEC e futuras unidades podem possuir documentos próprios;
- a API pública expõe apenas documentos publicados;
- a política de armazenamento permanece inalterada.

## Repositório de pesquisas e trabalhos acadêmicos

O app `research` registra:

- pesquisas formais em `ResearchProject`;
- TCCs e outros trabalhos acadêmicos em `AcademicWork`;
- equipes e contribuições por relações com `Person`;
- arquivos e links externos;
- vínculo institucional e relação opcional com eixos da LATEC.

## Produção científica

O app `scientific` mantém resultados publicados:

- artigos;
- resumos;
- patentes;
- livros;
- e-books;
- relatórios.

`ScientificOutput` possui unidade, autoria estruturada e relações opcionais com `ResearchProject` e `AcademicWork`. O campo textual `authors` permanece para autores externos e pode coexistir com `ScientificAuthorship`.

## Vitrine de projetos e soluções

O app `portfolio` apresenta:

- ações de extensão;
- produtos e serviços;
- startups;
- soluções tecnológicas;
- protótipos e projetos de inovação.

Portfólio não substitui pesquisas, TCCs ou produções científicas. A migration reversível cria equivalentes em rascunho para as categorias históricas compatíveis e preserva o projeto original inalterado até revisão manual.

## Exemplo de encadeamento

- Pesquisa: “Desenvolvimento de bioativo amazônico”.
- Trabalho acadêmico: “Avaliação fitoquímica da espécie X”.
- Produção científica: “Artigo com os resultados da avaliação fitoquímica”.
- Portfólio: “Protótipo de bioproduto desenvolvido a partir do bioativo”.

## Difusão, capacitação e extensão

O app `learning` contempla cursos, trilhas, materiais e eventos.

`Event` pode representar simpósios, palestras, cursos abertos, inaugurações, visitas institucionais, divulgação e extensão. O registro contém somente informações gerais; não existe modelagem para atividades internas por horário e seu endpoint público permanece fora desta entrega.

## Recorte LATEC

A seção LATEC reúne:

- ligantes e mentores;
- sete eixos;
- projetos, publicações, cursos e eventos específicos;
- documentos de transparência próprios, quando existirem.

Pesquisas e produções do LABTEC.IN só aparecem no recorte da LATEC quando estiverem vinculadas à unidade ou relacionadas explicitamente a um de seus eixos.

## Relações entre módulos

- `institutional` define a unidade proprietária.
- `research` registra o processo de pesquisa e os trabalhos acadêmicos.
- `scientific` registra resultados publicados.
- `portfolio` registra soluções e iniciativas práticas.
- `mediahub` mantém o catálogo de arquivos; os demais domínios ainda não possuem FK para `MediaAsset`.
- `transparency` publica documentos institucionais.
- `learning` promove difusão, cursos e eventos.
- `metrics` registra indicadores e snapshots por unidade, sem agregação automática nesta etapa.

## Páginas e filtros públicos

- `/api/v1/research-projects/?unit=labtec-in`;
- `/api/v1/academic-works/?work_type=tcc`;
- `/api/v1/scientific-outputs/?unit=labtec-in`;
- `/api/v1/projects/?unit=latec`;
- `/api/v1/transparency-documents/?unit=labtec-in`;

Essas rotas estão implementadas e retornam somente conteúdo publicado. Pesquisas aceitam também `axis`, `project_status`, `year`, `featured` e `search`; trabalhos aceitam `work_type`, `year`, `featured` e `search`.

## Conversão e corte

- projetos da categoria `pesquisa` geram `ResearchProject` em rascunho;
- projetos da categoria `producao-cientifica` geram `ScientificOutput` em rascunho;
- a conversão exige unidade preenchida e não infere autoria, metodologia, datas ou instituição;
- a equipe do projeto vira equipe de pesquisa, com líder como coordenador e demais participantes como colaboradores;
- a reversão remove somente os registros derivados;
- o projeto legado permanece público e inalterado até revisão e publicação do novo registro; o arquivamento é um corte manual posterior.
