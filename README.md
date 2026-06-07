# vmtranslator

Implementacao da parte da pessoa 1 no Project 07 (Nand2Tetris), em Python.

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

## Escopo desta entrega (Pessoa 1)

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
  - `Arg2()`

## Como usar o parser

Exemplo rapido no Linux (na raiz do projeto):

```bash
python3 - << 'PY'
from src.parser import Parser

p = Parser("project 7/MemoryAccess/BasicTest/BasicTest.vm")

while p.HasMoreCommands():
    p.Advance()
    print(p.CommandType(), p.Arg1(), p.Arg2() if p.CommandType() in {"C_PUSH", "C_POP"} else "")
PY
```

## Observacao

- A parte de traducao para Assembly (`CodeWriter` e `main`) faz parte da pessoa 2.
- Os arquivos do `project 7/` ja estao no repositorio para validacao da etapa completa em dupla.

## Commits sugeridos

- `feat(parser): adiciona parser para comandos VM da parte 1`
- `docs(readme): documenta escopo da pessoa 1 e uso do parser`