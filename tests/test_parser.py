"""
Testes unitários – Parser (Parte 1)

Cobre:
  - Leitura e limpeza de linhas (comentários, linhas em branco)
  - has_more_commands / advance
  - command_type para C_ARITHMETIC, C_PUSH, C_POP
  - arg1 e arg2
  - Erros esperados
"""

from __future__ import annotations

import os
import sys
import tempfile
import textwrap
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.parser import Parser, CommandType


def _write_vm(content: str) -> str:
    """Grava conteúdo VM em arquivo temporário e retorna o caminho."""
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".vm", delete=False, encoding="utf-8"
    )
    tmp.write(textwrap.dedent(content))
    tmp.close()
    return tmp.name


class TestParserBasic(unittest.TestCase):

    def test_ignores_blank_lines_and_comments(self) -> None:
        path = _write_vm("""
            // this is a comment
            
            push constant 7  // inline comment
        """)
        p = Parser(path)
        self.assertTrue(p.has_more_commands())
        p.advance()
        self.assertFalse(p.has_more_commands())

    def test_arithmetic_command_type(self) -> None:
        for cmd in ("add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"):
            path = _write_vm(f"{cmd}\n")
            p = Parser(path)
            p.advance()
            self.assertEqual(p.command_type(), CommandType.C_ARITHMETIC, cmd)

    def test_push_command_type(self) -> None:
        path = _write_vm("push constant 0\n")
        p = Parser(path)
        p.advance()
        self.assertEqual(p.command_type(), CommandType.C_PUSH)

    def test_pop_command_type(self) -> None:
        path = _write_vm("pop local 1\n")
        p = Parser(path)
        p.advance()
        self.assertEqual(p.command_type(), CommandType.C_POP)

    def test_arg1_arithmetic(self) -> None:
        path = _write_vm("add\n")
        p = Parser(path)
        p.advance()
        self.assertEqual(p.arg1(), "add")

    def test_arg1_push(self) -> None:
        path = _write_vm("push local 3\n")
        p = Parser(path)
        p.advance()
        self.assertEqual(p.arg1(), "local")

    def test_arg2_push(self) -> None:
        path = _write_vm("push argument 7\n")
        p = Parser(path)
        p.advance()
        self.assertEqual(p.arg2(), 7)

    def test_arg2_invalid_for_arithmetic_raises(self) -> None:
        path = _write_vm("add\n")
        p = Parser(path)
        p.advance()
        with self.assertRaises(ValueError):
            p.arg2()

    def test_advance_without_commands_sets_none(self) -> None:
        path = _write_vm("")
        p = Parser(path)
        self.assertFalse(p.has_more_commands())
        p.advance()  

    def test_camel_case_api(self) -> None:
        """Verifica que a API camelCase delega corretamente."""
        path = _write_vm("push constant 5\n")
        p = Parser(path)
        self.assertTrue(p.HasMoreCommands())
        p.Advance()
        self.assertEqual(p.CommandType(), "C_PUSH")
        self.assertEqual(p.Arg1(), "constant")
        self.assertEqual(p.Arg2(), 5)


if __name__ == "__main__":
    unittest.main(verbosity=2)