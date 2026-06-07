
"""
VMTranslator – Orquestrador (Parte 1)

"""

from __future__ import annotations

import sys
import os

from src.parser import Parser
from src.codewriter import CodeWriter


def _resolve_output_path(input_path: str) -> str:
    """Deriva o caminho do .asm a partir do .vm de entrada."""
    base, _ = os.path.splitext(input_path)
    return base + ".asm"


def translate(input_path: str) -> None:
    """
    Orquestra a tradução completa de um arquivo .vm para .asm.

    Args:
        input_path: Caminho para o arquivo .vm de entrada.

    Raises:
        FileNotFoundError: Se o arquivo .vm não existir.
        ValueError: Se o arquivo não tiver extensão .vm.
    """
    if not input_path.endswith(".vm"):
        raise ValueError(f"Expected a .vm file, got: {input_path!r}")

    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"File not found: {input_path!r}")

    output_path = _resolve_output_path(input_path)

    parser = Parser(input_path)
    cw = CodeWriter(output_path)

    try:
        while parser.HasMoreCommands():
            parser.Advance()
            cmd_type = parser.CommandType()

            if cmd_type == "C_ARITHMETIC":
                cw.WriteArithmetic(parser.Arg1())

            elif cmd_type == "C_PUSH":
                cw.WritePush(parser.Arg1(), parser.Arg2())

            elif cmd_type == "C_POP":
                cw.WritePop(parser.Arg1(), parser.Arg2())

    finally:
        cw.Close()

    print(f"[ok] {input_path} -> {output_path}")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python main.py <file.vm>", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]

    try:
        translate(input_path)
    except (FileNotFoundError, ValueError) as exc:
        print(f"[error] {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
