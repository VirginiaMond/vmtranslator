# vmtranslator

## Integrante

- André Luis Aguiar do Nascimento
- Virgínia Maria Mondego Ferreira

## Linguagem e versao

- Python 3.10+ (testado com Python 3.x)

## Estrutura do projeto

```text
vmtranslator/
├── project 7/                  # Casos de teste fornecidos pelo projeto
├── src/
│   ├── parser/
│   │   └── parser.py           # Parser de comandos VM
│   └── __init__.py
└── README.md
```

## Escopo desta entrega 

- Parser de arquivos `.vm` com remocao de comentarios e linhas vazias
- Classificacao dos comandos em:
  - `C_ARITHMETIC`
  - `C_PUSH`
  - `C_POP`
- API do parser com:
  - `HasMoreCommands()`
  - `Advance()`
  - `CommandType()`
  - `Arg1()`
  # VMTranslator

  Autores

  - André Luis Aguiar do Nascimento
  - Virgínia Maria Mondego Ferreira

  Visão geral

  Este repositório contém o projeto VMTranslator (Nand2Tetris — Project 07): o *parser* de arquivos `.vm` e os casos de teste originais do Project 07. A tradução completa para Assembly (CodeWriter / CLI).

  Objetivo desta entrega

  - Fornecer um `Parser` funcional para arquivos `.vm` que:
    - remove comentários e linhas em branco;
    - tokeniza comandos;
    - classifica comandos como `C_ARITHMETIC`, `C_PUSH` ou `C_POP`;
    - expõe a API compatível solicitada pelo enunciado (`HasMoreCommands`, `Advance`, `CommandType`, `Arg1`, `Arg2`).

  Estrutura do repositório

  ```text
  vmtranslator/
  ├── project 7/            # Casos de teste do nand2tetris (fornecidos)
  ├── src/
  │   └── parser/
  │       ├── __init__.py
  │       └── parser.py     # Parser de comandos VM
  ├── assets/               # imagens e screenshots (opcional)
  └── README.md
  ```

  Pré-requisitos

  - Python 3.10+ (recomendado)
  - Nenhuma dependência externa é necessária para o parser.

  Configuração rápida

  Recomendo criar um ambiente virtual (opcional):

  ```bash
  python3 -m venv .venv
  source .venv/bin/activate

  # (opcional) atualizar pip
  pip install --upgrade pip
  ```

  Uso — Parser

  Exemplo mínimo para inspecionar um `.vm` (raiz do repositório):

  ```bash
  python3 - <<'PY'
  from src.parser import Parser

  p = Parser("project 7/MemoryAccess/BasicTest/BasicTest.vm")

  while p.HasMoreCommands():
      p.Advance()
      cmd_type = p.CommandType()
      a1 = p.Arg1()
      a2 = p.Arg2() if cmd_type in {"C_PUSH", "C_POP"} else None
      print(cmd_type, a1, a2)
  PY
  ```

  Testes unitários

  O repositório inclui testes básicos do parser. Para executá-los:

  ```bash
  python3 -m unittest discover -s tests -p "test_*.py"
  ```

  Validação com o CPU Emulator (Nand2Tetris)

  1. Se você dispor de uma implementação `CodeWriter`, gere o `.asm` correspondente a um `.vm` dos diretórios em `project 7/`.
  2. Abra o `CPUEmulator` do Nand2Tetris.
  3. No emulador, carregue o script `.tst` correspondente (por exemplo: `project 7/MemoryAccess/BasicTest/BasicTest.tst`).
  4. Execute o script e verifique se a saída confere com o arquivo `.cmp`.

  Quando a tradução estiver correta, o emulador exibirá:

  ```
  Comparison ended successfully.
  ```

  Entrega e commits

  O histórico desta branch foi organizado em commits atômicos. Mensagens sugeridas para o trabalho:

  - `chore(project07): adiciona arquivos base do Project 07`
  - `feat(parser): implementa analisador de comandos .vm`
  - `docs(readme): documenta escopo.`
  - `chore(gitignore): adiciona regras basicas para Python`

  Como adicionar um screenshot do emulador

  Coloque a imagem desejada em `assets/` com o nome `vm_emulator.png` e commite. Exemplo:

  ```bash
  cp /caminho/para/sua/imagem.png assets/vm_emulator.png
  git add assets/vm_emulator.png README.md
  git commit -m "doc(readme): adiciona screenshot do VM Emulator"
  git push origin feat-parser-readme
  ```

  Exibição automática (se o arquivo existir):

  ![VM Emulator screenshot](assets/vm_emulator.png)

