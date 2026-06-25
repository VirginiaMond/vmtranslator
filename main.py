
"""
VMTranslator – Orquestrador (Parte 1)

"""

from __future__ import annotations

import sys
import os

from src.parser import Parser
from src.codewriter import CodeWriter


def _get_vm_files(path: str) -> list[str]:
    if os.path.isfile(path):
        return [path] if path.endswith(".vm") else []
    if os.path.isdir(path):
        vm_files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".vm")]
        return sorted(vm_files)
    return []

def _resolve_output_path(input_path: str) -> str:
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if os.path.isfile(input_path):
        base_name = os.path.basename(input_path)
        name_without_ext = os.path.splitext(base_name)[0]
    else:
        name_without_ext = os.path.basename(os.path.normpath(input_path))
    
    return os.path.join(output_dir, f"{name_without_ext}.asm")

def translate(input_path: str) -> None:
    """
    Orquestra a tradução completa de um arquivo .vm para .asm.

    Args:
        input_path: Caminho para o arquivo .vm de entrada.

    Raises:
        FileNotFoundError: Se o arquivo .vm não existir.
        ValueError: Se o arquivo não tiver extensão .vm.
    """
    vm_files = _get_vm_files(input_path)
    if not vm_files:
        raise ValueError(f"Nenhum arquivo .vm encontrado em: {input_path!r}")

    output_path = _resolve_output_path(input_path)
    cw = CodeWriter(output_path)

    try:
        if os.path.isdir(input_path):
            cw.WriteInit()
        for vm_file in vm_files:
            cw.set_filename(os.path.basename(vm_file)) 
            
            parser = Parser(vm_file)   
            while parser.HasMoreCommands():
                parser.Advance()
                cmd_type = parser.CommandType()

                if cmd_type == "C_ARITHMETIC":
                    cw.WriteArithmetic(parser.Arg1())
                elif cmd_type == "C_PUSH":
                    cw.WritePush(parser.Arg1(), parser.Arg2())
                elif cmd_type == "C_POP":
                    cw.WritePop(parser.Arg1(), parser.Arg2())
                elif cmd_type == "C_LABEL":
                    cw.WriteLabel(parser.Arg1())
                elif cmd_type == "C_GOTO":
                    cw.WriteGoto(parser.Arg1())
                elif cmd_type == "C_IF":
                    cw.WriteIf(parser.Arg1())
                elif cmd_type == "C_FUNCTION":
                    cw.WriteFunction(parser.Arg1(), parser.Arg2())
                elif cmd_type == "C_CALL":
                    cw.WriteCall(parser.Arg1(), parser.Arg2())
                elif cmd_type == "C_RETURN":
                    cw.WriteReturn()

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
