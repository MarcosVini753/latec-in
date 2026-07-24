# Ponytail no projeto LABTEC.IN

O repositório usa o conjunto de instruções do projeto Ponytail para orientar agentes de código a preferirem soluções pequenas, reutilização de código existente, recursos nativos da plataforma e dependências já instaladas.

## Integração no repositório

O arquivo `AGENTS.md` na raiz contém as instruções persistentes do Ponytail e regras específicas deste projeto. A extensão do Codex para VS Code lê esse arquivo como instrução de projeto.

Essa integração é versionada junto com o código e vale para qualquer colaborador ou agente que respeite `AGENTS.md`.

## Instalação completa no Codex CLI

A instalação completa adiciona os comandos, níveis e hooks do Ponytail ao ambiente local do desenvolvedor. Ela não é armazenada dentro do repositório e precisa ser executada em cada máquina:

```bash
codex plugin marketplace add DietrichGebert/ponytail
codex plugin add ponytail@ponytail
```

Depois:

1. execute `codex`;
2. abra `/hooks`;
3. revise e confie nos dois hooks do plugin;
4. inicie uma nova conversa do Codex.

O Node.js precisa estar disponível no `PATH` do shell não interativo para que os hooks funcionem. Sem Node.js, as instruções em `AGENTS.md` continuam funcionando, mas os hooks e a ativação automática do plugin não são executados.

## Modos e comandos

A instalação completa disponibiliza recursos como:

- `/ponytail`: ativa ou configura o modo;
- `/ponytail-review`: revisão de excesso de engenharia;
- `/ponytail-audit`: auditoria do repositório;
- `/ponytail-debt`: levantamento de simplificações deliberadas marcadas no código;
- `/ponytail-gain`: medição de impacto;
- `/ponytail-help`: referência rápida.

## Aplicação no LABTEC.IN

As regras gerais do Ponytail não substituem as decisões arquiteturais do projeto. Antes de modificar o backend, os agentes devem consultar:

- `docs/architecture/`;
- `docs/adr/`;
- migrations e models já existentes;
- testes relacionados ao domínio alterado.

Simplicidade não deve remover validações, controle editorial, permissões, integridade referencial, segurança ou acessibilidade.

## Fonte e licença

Integração baseada no projeto `DietrichGebert/ponytail`, distribuído sob licença MIT.
