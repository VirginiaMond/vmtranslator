# vmtranslator

Tradutor de VM para Assembly Hack desenvolvido para os Projects 07 e 08 do
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
├── project-8/                      # Testes oficiais do Nand2Tetris Project 08
└── output/                         # Arquivos .asm gerados pelo tradutor
```

## Funcionalidades implementadas

### Parte 1 - Project 07

- Operações aritméticas e lógicas: `add`, `sub`, `neg`, `eq`, `gt`, `lt`,
  `and`, `or`, `not`
- Comandos de memória: `push` e `pop`
- Segmentos: `constant`, `local`, `argument`, `this`, `that`, `temp`,
  `pointer` e `static`

### Parte 2 - Project 08

- Código de bootstrap com inicialização de `SP = 256` e chamada para
  `Sys.init`
- Controle de fluxo: `label`, `goto` e `if-goto`
- Sub-rotinas: `function`, `call` e `return`
- Escopo de labels no formato `NomeDaFuncao$NomeDoLabel`
- Suporte a múltiplos arquivos `.vm` em um mesmo diretório
- Símbolos `static` separados por nome de arquivo

## Como executar

Não há etapa de compilação, pois o projeto é escrito em Python.

Para traduzir um único arquivo `.vm`:

```bash
python3 main.py caminho/do/arquivo.vm
```

Para traduzir todos os arquivos `.vm` de um diretório:

```bash
python3 main.py caminho/do/diretorio
```

Os arquivos `.asm` são gerados na pasta `output/`.

## Exemplos

Traduzindo um teste simples da Parte 1:

```bash
python3 main.py project-7/StackArithmetic/SimpleAdd/SimpleAdd.vm
```

Saída esperada:

```text
[ok] project-7/StackArithmetic/SimpleAdd/SimpleAdd.vm -> output/SimpleAdd.asm
```

Traduzindo um diretório da Parte 2:

```bash
python3 main.py project-8/FunctionCalls/NestedCall
```

Saída esperada:

```text
[ok] project-8/FunctionCalls/NestedCall -> output/NestedCall.asm
```

Exemplo de validação esperada para `BasicLoop` no CPU Emulator:

```text
| RAM[0] |RAM[256]|
|    257 |      6 |
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
4. Execute o script e compare a saída com o arquivo `.cmp`.

Os scripts oficiais procuram o `.asm` no mesmo diretório do `.tst`. Como este
projeto gera os arquivos em `output/`, carregue o arquivo gerado manualmente no
CPU Emulator ou copie o `.asm` para a pasta do teste antes de executar o script.

Comandos úteis para gerar os testes principais do Project 08:

```bash
python3 main.py project-8/ProgramFlow/BasicLoop/BasicLoop.vm
python3 main.py project-8/ProgramFlow/FibonacciSeries/FibonacciSeries.vm
python3 main.py project-8/FunctionCalls/SimpleFunction/SimpleFunction.vm
python3 main.py project-8/FunctionCalls/NestedCall
python3 main.py project-8/FunctionCalls/FibonacciElement
python3 main.py project-8/FunctionCalls/StaticsTest
```

Arquivos de comparação correspondentes:

- `project-8/ProgramFlow/BasicLoop/BasicLoop.cmp`
- `project-8/ProgramFlow/FibonacciSeries/FibonacciSeries.cmp`
- `project-8/FunctionCalls/SimpleFunction/SimpleFunction.cmp`
- `project-8/FunctionCalls/NestedCall/NestedCall.cmp`
- `project-8/FunctionCalls/FibonacciElement/FibonacciElement.cmp`
- `project-8/FunctionCalls/StaticsTest/StaticsTest.cmp`

## Histórico de commits

O histórico pode ser consultado com:

```bash
git log --oneline
```
