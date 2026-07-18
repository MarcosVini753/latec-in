# Permissões e acesso administrativo

## Princípios

- Visitantes acessam somente conteúdo público e publicado.
- Pessoas públicas continuam separadas de usuários administrativos.
- O sistema usa o `User` padrão do Django e o Django Admin como CMS.
- A autorização administrativa combina papel, estado ativo, unidade e, para mentores, eixo.
- Somente administrador e coordenação do LABTEC.IN realizam publicação final ou arquivamento.

## Perfil administrativo

`accounts.Profile` possui:

- `role`: `admin`, `lab_coordinator`, `unit_coordinator`, `mentor`, `editor` ou `reader`;
- `primary_unit`, opcional;
- `authorized_units`, relação muitos-para-muitos opcional;
- `inherit_descendants`, `False` por padrão;
- `person`, opcional;
- `is_active_admin`.

Superusuários são irrestritos. Um perfil inativo não recebe acesso institucional. Perfis de mentor, editor ou leitor sem unidade ou eixo aplicável não recebem acesso a conteúdo.

A migration de dados converte `coordinator` legado em `lab_coordinator`, define `labtec-in` como unidade principal e habilita descendentes. Mentores legados recebem `latec` apenas quando existe correspondência entre a pessoa vinculada e uma mentoria. Editor e reader são preservados sem ganhar unidades implicitamente. Perfis inexistentes ou inativos não recebem escopo.

## Matriz aplicada

| Papel | Escopo de leitura | Criar/editar | Publicar/arquivar |
| --- | --- | --- | --- |
| Superusuário ou `admin` | Todas as unidades e conteúdo sem unidade | Sim | Sim |
| `lab_coordinator` | LABTEC.IN, descendentes e conteúdo sem unidade | Sim | Sim |
| `unit_coordinator` | Unidade principal, autorizadas e descendentes quando `inherit_descendants` estiver habilitado | Rascunho e revisão | Não |
| `mentor` | LATEC, limitado aos eixos em `AxisMentorship` da pessoa vinculada | Rascunho e revisão | Não |
| `editor` | Unidades explicitamente autorizadas | Rascunho e revisão | Não |
| `reader` | Unidades explicitamente autorizadas | Somente leitura | Não |

Conteúdo sem unidade é visível somente a superusuário, administrador e coordenação do LABTEC.IN. Mentor, editor e coordenador de unidade não podem alterar registros já publicados.

## Aplicação no Django Admin

Um mixin compartilhado recebe `unit_lookup` e, quando necessário, `axis_lookup`. Ele cobre:

- modelos com `unit` direto;
- filhos cujo escopo vem do pai, como resultados, equipes, materiais, snapshots, contribuidores e autorias;
- parceiros com unidades em relação muitos-para-muitos;
- querysets, formulários, inlines, autocomplete e escolhas de unidade ou eixo;
- validação do objeto enviado, impedindo POST adulterado;
- remoção das ações de publicação e arquivamento para papéis sem essa capacidade.

Filtrar as opções visuais não substitui a autorização: inclusão e alteração validam novamente o escopo do registro e de suas relações.

## Regras especiais

- Mentores acessam apenas objetos associados aos seus próprios eixos da LATEC.
- Parceiro associado a mais de uma unidade é editável somente por superusuário, administrador ou coordenação do LABTEC.IN.
- Mensagens de contato são restritas aos mesmos três grupos e nunca aparecem na API pública.
- Usuários, perfis, papéis e unidades são geridos somente por superusuário ou administrador.
- A coordenação do LABTEC.IN pode gerir `InstitutionMembership`, sem elevar papéis administrativos.
- A API pública permanece anônima, somente leitura e independente dos escopos do Admin.

## Limites

O frontend não foi alterado. Permissões públicas por unidade, painel administrativo próprio e novos mecanismos de autenticação permanecem fora do escopo.
