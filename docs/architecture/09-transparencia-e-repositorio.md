# Transparência, repositório científico e vitrine do LABTEC.IN

O portal cumpre funções públicas de transparência, preservação acadêmica, difusão científica e apresentação de soluções. Cada registro possui uma unidade proprietária; conteúdos da LATEC podem integrar opcionalmente o ecossistema público do LABTEC.IN.

## Transparência

`TransparencyDocument` mantém editais, atas, homologações, julgamentos de recursos, resultados e comunicados. Cada documento exige unidade, arquivo e workflow editorial. A API expõe somente registros publicados.

## Repositório acadêmico

O app `research` registra:

- pesquisas formais em `ResearchProject`;
- TCCs e outros trabalhos em `AcademicWork`;
- equipes e contribuidores por relações com `Person`;
- metadados mínimos, arquivo ou URL externa;
- unidade obrigatória e eixo opcional.

## Produção científica

`ScientificOutput` representa artigos, resumos, patentes, livros, e-books, relatórios técnicos e outros resultados. Pode apontar para uma pesquisa, um trabalho acadêmico ou ambos. A autoria interna e sua ordem são registradas exclusivamente por `ScientificAuthorship`.

## Vitrine de projetos

`portfolio.Project` apresenta extensão, produtos, serviços, startups, protótipos e soluções. Pesquisa formal, trabalho acadêmico e produção científica não são categorias do portfólio.

Exemplo de encadeamento:

- pesquisa: desenvolvimento de um bioativo amazônico;
- trabalho: avaliação fitoquímica de uma espécie;
- produção: artigo com os resultados;
- portfólio: protótipo de bioproduto derivado.

## Arquivos

Cada domínio mantém seus próprios campos `file`, imagem ou URL externa. O app, a tabela e os registros administrativos do antigo MediaHub foram removidos porque não possuíam integração estrutural com esses conteúdos.

`cleanup_orphan_media` compara os arquivos do storage com todos os `FileField` e `ImageField` atuais. O comando apenas inventaria por padrão e exclui os órfãos somente com `--delete`; uma raiz personalizada exige também `--confirm-root` com o caminho absoluto exato. O resultado é exibido no terminal e não cria registro operacional permanente.

## Cursos

`learning` mantém apenas cursos e materiais ordenados. Trilhas e eventos foram removidos. Todo material de um curso publicado é público; não existe flag de privacidade por material. Atividades de capacitação que devam aparecer no portal são representadas como cursos quando esse conceito for suficiente.

## Recorte LATEC e ecossistema

A seção LATEC reúne memberships públicos, sete eixos e conteúdos próprios. O filtro de uma unidade também inclui conteúdos publicados de filhas diretas marcados com `include_in_parent_ecosystem=True`. Relação com eixo, isoladamente, não muda o recorte institucional.

Exemplos:

```txt
GET /api/v1/research-projects/?unit=labtec-in
GET /api/v1/academic-works/?work_type=tcc
GET /api/v1/scientific-outputs/?unit=latec
GET /api/v1/projects/?unit=latec
GET /api/v1/transparency-documents/?unit=labtec-in
```

Não existe filtro de destaque. Todos os catálogos editoriais retornam somente `editorial_status=published`.

## Corte histórico

A pesquisa de Bioativos é o registro científico canônico e publicado. O projeto de portfólio anterior foi arquivado e desvinculado da categoria histórica. O identificador técnico de proveniência foi removido após o corte; rastreabilidade adicional permanece no histórico de migrations e no banco de backup.
