# vmtranslator

Tradutor VM para Assembly Hack desenvolvido para o Project 07 do
Nand2Tetris.

## Integrantes

- André Luis Aguiar do Nascimento
- Virgínia Maria Mondego Ferreira

## Linguagem e versão

- Python 3.10 ou superior
- Validado localmente com Python 3.12.3

## Estrutura do projeto

```text
vmtranslator/
├── main.py                         # CLI/orquestrador da tradução
├── src/
│   ├── parser/
│   │   └── parser.py               # Leitura e classificação dos comandos VM
│   └── codewriter/
│       └── codewriter.py           # Geração de Assembly Hack
├── tests/                          # Testes unitários
├── project-7/                      # Testes oficiais do Nand2Tetris Project 07
└── README.md
```

## Escopo

Esta entrega traduz comandos do Project 07:

- Operações aritméticas e lógicas: `add`, `sub`, `neg`, `eq`, `gt`, `lt`,
  `and`, `or`, `not`
- Comandos de memória: `push` e `pop`
- Segmentos: `constant`, `local`, `argument`, `this`, `that`, `temp`,
  `pointer` e `static`

## Como executar

Não há etapa de compilação, pois o projeto é escrito em Python.

Para traduzir um arquivo `.vm`, execute:

```bash
python3 main.py caminho/do/arquivo.vm
```

O arquivo `.asm` é gerado no mesmo diretório do `.vm`, com o mesmo nome base.

## Exemplo de uso

```bash
python3 main.py project-7/StackArithmetic/SimpleAdd/SimpleAdd.vm
```

Saída esperada:

```text
[ok] project-7/StackArithmetic/SimpleAdd/SimpleAdd.vm -> project-7/StackArithmetic/SimpleAdd/SimpleAdd.asm
```

Outro exemplo:

```bash
python3 main.py project-7/MemoryAccess/BasicTest/BasicTest.vm
```

## Testes unitários

Execute:

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

## Validação com o CPU Emulator

Para validar com as ferramentas oficiais do Nand2Tetris:

1. Gere o arquivo `.asm` do teste desejado.
2. Abra o `CPUEmulator`.
3. Carregue o script `.tst` correspondente.
4. Execute o script e compare com o arquivo `.cmp`.

Testes exigidos pela entrega:

```bash
python3 main.py project-7/StackArithmetic/SimpleAdd/SimpleAdd.vm
python3 main.py project-7/MemoryAccess/BasicTest/BasicTest.vm
```

Arquivos de comparação:

- `project-7/StackArithmetic/SimpleAdd/SimpleAdd.cmp`
- `project-7/MemoryAccess/BasicTest/BasicTest.cmp`
