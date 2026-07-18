# Migração para a arquitetura institucional LABTEC.IN

Este documento registra o estado implementado da migração do backend para LABTEC.IN como instituição raiz e LATEC como unidade filha, além dos cortes que ainda exigem revisão manual.

## Estado implementado

- LABTEC.IN e LATEC existem como unidades, com slugs `labtec-in` e `latec`.
- Memberships possuem unicidade por pessoa, unidade e papel e validação de período.
- A hierarquia impede autorreferência e ciclos indiretos em gravações usuais.
- O seed cria 43 memberships, sete eixos da LATEC e nove mentores sem duplicação.
- Conteúdos legados possuem `unit` opcional; parceiros possuem várias unidades.
- `Profile` possui papel, unidade principal, unidades autorizadas e herança opcional de descendentes.
- O Django Admin aplica escopo por unidade e eixo e reserva publicação final a administrador e coordenação do LABTEC.IN.
- O app `research` modela pesquisas, trabalhos acadêmicos, equipes e contribuidores.
- Produções científicas podem apontar para pesquisas e trabalhos e possuem autoria interna ordenada.
- A API `/api/v1/` expõe pesquisas e trabalhos, filtra por unidade e preserva os slugs existentes.
- A Home retorna exclusivamente o conteúdo direto do LABTEC.IN.

## Integridade antes das constraints

A migration institucional executa preflight antes de criar as constraints. Ela procura:

- memberships duplicados por `(person, unit, role)`;
- memberships com `end_date < start_date`;
- ciclos na hierarquia, inclusive indiretos.

Se encontrar dados inválidos, a migration falha e informa IDs claros. Nenhum dado é apagado ou corrigido automaticamente. Depois do preflight, o banco garante unicidade, período válido e ausência de autorreferência.

`InstitutionalUnit.clean()` percorre os ancestrais para detectar ciclos indiretos, e `save()` executa essa validação no Admin, seed e gravações ORM comuns. O manager também bloqueia operações hierárquicas inseguras por `bulk_create()` e `bulk_update()`. `QuerySet.update()` não chama `save()` e pode contornar a validação; migrations ou rotinas que o utilizem devem preservar a hierarquia explicitamente.

## Backfill institucional

| Registro | Classificação inicial |
| --- | --- |
| `SiteSettings`, heroes, seções, links e métricas atuais | LABTEC.IN |
| Sete eixos e mentorias | LATEC |
| Ligantes | Membership na LATEC |
| Professores e pesquisadores | Membership no LABTEC.IN |
| Coordenação | LABTEC.IN e LATEC |
| Nove pessoas em `AxisMentorship` | Membership `Mentor` na LATEC |
| Notícias e cursos explicitamente da Liga | LATEC |
| Projetos existentes | Classificação provisória preservada |

`Person.role` não foi removido. Os memberships são a representação institucional nova, mas o campo antigo continua disponível até o corte de todos os consumidores.

## Perfis e permissões

A migration de perfis aplica somente mapeamentos inequívocos:

- `coordinator` legado vira `lab_coordinator`, com unidade principal LABTEC.IN e herança de descendentes;
- mentor legado recebe LATEC quando sua pessoa está em `AxisMentorship`;
- editor e reader permanecem sem acesso a conteúdo até receberem unidade;
- perfil inativo ou inexistente não recebe escopo;
- superusuário permanece irrestrito.

Somente superusuário, `admin` e `lab_coordinator` podem publicar ou arquivar. Coordenador de unidade, mentor e editor trabalham em rascunho ou revisão e não alteram registros já publicados. Reader possui somente leitura. Conteúdo sem unidade fica restrito a administrador e coordenação do LABTEC.IN.

## Conversão histórica

A conversão é uma migration de dados reversível:

1. exige `unit` nos projetos de categoria `pesquisa` ou `producao-cientifica`;
2. cria `ResearchProject` ou `ScientificOutput` em rascunho;
3. preserva unidade, eixo, título, slug, resumo e status compatível;
4. converte equipe de pesquisa, com líder como coordenador e demais membros como colaboradores;
5. não infere autoria científica, metodologia, datas ou instituição;
6. mantém o projeto legado inalterado e público;
7. registra o ID da origem em `legacy_portfolio_project_id`, campo técnico não exposto;
8. no reverse, remove somente os registros marcados como derivados, sem depender do slug atual.

No banco inicial, `pesquisa-de-bioativos-da-amazonia` gera uma pesquisa em rascunho. Não há produção científica histórica para converter. Em banco novo, o seed cria somente a pesquisa nova; em banco atualizado, o projeto legado continua até o corte manual. O seed não republica um legado arquivado posteriormente.

## Corte manual

O projeto legado só deve ser arquivado depois que a pesquisa derivada for revisada, completada e publicada com aprovação institucional. O corte não integra a migration porque depende da validação de autoria, metodologia, datas, arquivos e responsabilidade institucional.

## Ordem operacional

1. Fazer backup e executar o preflight de duplicatas, datas, ciclos e projetos sem unidade.
2. Aplicar migrations institucionais e de `Profile`.
3. Aplicar a migration inicial de `research` e as relações de `scientific`.
4. Aplicar a conversão histórica.
5. Executar o seed duas vezes para confirmar idempotência.
6. Executar `check`, testes, `makemigrations --check --dry-run` e validação OpenAPI.
7. Revisar manualmente a pesquisa convertida.
8. Arquivar o legado somente após aprovação institucional.

## Migrations desta etapa

| App | Migration | Responsabilidade |
| --- | --- | --- |
| `institutional` | `0002_validate_and_add_institutional_constraints` | Preflight e constraints institucionais. |
| `accounts` | `0002_add_institutional_admin_scope` | Campos de escopo, novos papéis e conversão conservadora dos perfis. |
| `research` | `0001_initial` | Pesquisas, trabalhos, equipes e contribuidores. |
| `scientific` | `0003_scientificoutput_academic_work_and_more` | Relações com `research` e autoria estruturada. |
| `research` | `0002_convert_legacy_portfolio_categories` | Conversão histórica reversível em rascunhos. |

## Compatibilidade preservada

- `Person.role`, papéis administrativos migrados, categorias antigas e dados existentes não foram removidos.
- Os campos `unit` dos models legados continuam `null=True` e `blank=True`.
- Os novos `ResearchProject` e `AcademicWork` exigem unidade com `PROTECT`.
- Tipos científicos `project` e `scientific_production` e o campo textual `authors` permanecem temporariamente.
- Nenhum slug público foi alterado.

## Fora do escopo desta entrega

- frontend `latec-app/`;
- expansão do payload da Home;
- endpoint público de eventos;
- tornar obrigatórios os campos `unit` dos models legados;
- remoção de `Person.role`, categorias ou tipos legados;
- arquivamento automático do projeto convertido;
- autenticação ou permissões por unidade na API pública;
- usuários administrativos ou credenciais criados pelo seed.
