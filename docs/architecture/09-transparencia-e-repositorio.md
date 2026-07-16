# Transparência, repositório científico e vitrine do LABTEC.IN

O portal do LABTEC.IN cumpre funções públicas de transparência, preservação acadêmica, difusão científica e apresentação de soluções. Conteúdos específicos da LATEC são identificados pela unidade `latec`.

## Estado implementado

O backend já possui:

- `transparency.TransparencyDocument`;
- `scientific.ScientificOutput`;
- `portfolio.Project`;
- cursos e eventos em `learning`;
- arquivos em `mediahub`.

Esses models ainda não possuem unidade institucional. Também não existem models próprios para pesquisas e trabalhos acadêmicos, nem autoria científica estruturada.

## Transparência

O app `transparency` mantém editais, atas, homologações, julgamentos de recursos, resultados e comunicados.

Na arquitetura alvo:

- cada documento possui `unit`;
- o padrão institucional é LABTEC.IN;
- a LATEC e futuras unidades podem possuir documentos próprios;
- a API pública expõe apenas documentos publicados;
- a política de armazenamento permanece inalterada.

## Repositório de pesquisas e trabalhos acadêmicos

O app `research` passa a registrar:

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

`ScientificOutput` recebe unidade, autoria estruturada e relações opcionais com `ResearchProject` e `AcademicWork`.

## Vitrine de projetos e soluções

O app `portfolio` apresenta:

- ações de extensão;
- produtos e serviços;
- startups;
- soluções tecnológicas;
- protótipos e projetos de inovação.

Portfólio não substitui pesquisas, TCCs ou produções científicas. Categorias históricas incompatíveis serão revisadas durante a migração.

## Exemplo de encadeamento

- Pesquisa: “Desenvolvimento de bioativo amazônico”.
- Trabalho acadêmico: “Avaliação fitoquímica da espécie X”.
- Produção científica: “Artigo com os resultados da avaliação fitoquímica”.
- Portfólio: “Protótipo de bioproduto desenvolvido a partir do bioativo”.

## Difusão, capacitação e extensão

O app `learning` contempla cursos, trilhas, materiais e eventos.

`Event` pode representar simpósios, palestras, cursos abertos, inaugurações, visitas institucionais, divulgação e extensão. O registro contém somente informações gerais; não existe modelagem prevista para atividades internas por horário.

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
- `mediahub` armazena arquivos reutilizáveis.
- `transparency` publica documentos institucionais.
- `learning` promove difusão, cursos e eventos.
- `metrics` consolida indicadores por unidade.

## Páginas e filtros públicos

- `/api/v1/research-projects/?unit=labtec-in`;
- `/api/v1/academic-works/?work_type=tcc`;
- `/api/v1/scientific-outputs/?unit=labtec-in`;
- `/api/v1/projects/?unit=latec`;
- `/api/v1/transparency-documents/?unit=labtec-in`;
- `/api/v1/events/?unit=labtec-in`.

Todas essas rotas são alvo documental; somente os endpoints já identificados em [API pública](03-api-publica.md) estão implementados hoje.
