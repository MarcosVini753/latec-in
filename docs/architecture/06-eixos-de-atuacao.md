# Eixos de atuação da LATEC

A LATEC é uma unidade filha apoiada pelo LABTEC.IN. Seus sete eixos organizam mentorias e atividades próprias da Liga; eles não representam a estrutura global do laboratório.

## Estado implementado

O app `axes` possui `ResearchAxis` e `AxisMentorship`, com sete eixos e nove vínculos de mentoria carregados pelo seed. Cada eixo possui unidade obrigatória e pertence explicitamente à LATEC.

`AxisMentorship` registra a relação entre eixo e pessoa. O papel institucional da pessoa é expresso separadamente por `InstitutionMembership`.

## Eixos iniciais

1. Etnobotânica e Pós-Colheita.
2. Práticas em Laboratório e Nanotecnologia.
3. Nutrição e Ciências dos Alimentos.
4. Saúde e bem-estar.
5. Produção Vegetal e Biotecnologia.
6. Agroindustrialização.
7. Redação Científica.

Os títulos, descrições, palavras-chave e mentorias completos são dados editoriais administrados no backend. A grafia institucional dos nomes de mentores deve ser validada antes de mudanças no seed.

## Modelagem

`ResearchAxis` contém unidade, número, título, slug, descrição, palavras-chave, ativação e ordem estrutural.

`AxisMentorship` contém eixo, pessoa, papel, indicação de mentor principal e ordem. A combinação `(axis, person)` é única.

## Regras

- Cada eixo pertence à LATEC.
- Um eixo pode ter vários mentores e uma pessoa pode atuar em vários eixos.
- Projetos, cursos, notícias, pesquisas e produções podem usar eixo quando aplicável.
- Uma pesquisa do LABTEC.IN pode se relacionar com um eixo da LATEC sem mudar de unidade proprietária.
- Conteúdo geral do laboratório não precisa de eixo.
- Mentor administrativo exige perfil ativo, pessoa vinculada e `AxisMentorship`.
- O vínculo com um eixo não amplia acesso para outros eixos ou conteúdos.

O seed cria nove memberships `Mentor` na LATEC. Marta pode acumular `Coordenadora` e `Mentor` porque a unicidade do membership inclui o papel.
