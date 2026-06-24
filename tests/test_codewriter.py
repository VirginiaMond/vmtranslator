"""
Testes unitários – CodeWriter (Parte 1)

Contém:
  - Todas as operações aritméticas/lógicas (add, sub, neg, eq, gt, lt, and, or, not)
  - push/pop para todos os segmentos suportados
  - Labels únicos em comparações encadeadas
  - Erro esperado ao tentar pop constant
"""

from __future__ import annotations

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.codewriter import CodeWriter

def _make_writer(tmp_dir: str, name: str = "Test") -> tuple[CodeWriter, str]:
    """Cria um CodeWriter apontando para um arquivo temporário."""
    path = os.path.join(tmp_dir, f"{name}.asm")
    return CodeWriter(path), path


def _read(path: str) -> list[str]:
    """Lê o arquivo gerado e retorna as linhas sem comentários nem blanks."""
    with open(path, encoding="utf-8") as f:
        lines = []
        for line in f:
            stripped = line.strip()
            if stripped and not stripped.startswith("//"):
                lines.append(stripped)
    return lines

class TestWriteArithmetic(unittest.TestCase):

    def setUp(self) -> None:
        self.tmp = tempfile.mkdtemp()

    def test_add_contains_d_plus_m(self) -> None:
        cw, path = _make_writer(self.tmp)
        cw.write_arithmetic("add")
        cw.close()
        self.assertIn("M=D+M", _read(path))

    def test_sub_contains_m_minus_d(self) -> None:
        cw, path = _make_writer(self.tmp)
        cw.write_arithmetic("sub")
        cw.close()
        self.assertIn("M=M-D", _read(path))

    def test_and_contains_d_and_m(self) -> None:
        cw, path = _make_writer(self.tmp)
        cw.write_arithmetic("and")
        cw.close()
        self.assertIn("M=D&M", _read(path))

    def test_or_contains_d_or_m(self) -> None:
        cw, path = _make_writer(self.tmp)
        cw.write_arithmetic("or")
        cw.close()
        self.assertIn("M=D|M", _read(path))

    def test_neg_contains_neg_m(self) -> None:
        cw, path = _make_writer(self.tmp)
        cw.write_arithmetic("neg")
        cw.close()
        self.assertIn("M=-M", _read(path))

    def test_not_contains_not_m(self) -> None:
        cw, path = _make_writer(self.tmp)
        cw.write_arithmetic("not")
        cw.close()
        self.assertIn("M=!M", _read(path))

    def test_eq_uses_jeq(self) -> None:
        cw, path = _make_writer(self.tmp)
        cw.write_arithmetic("eq")
        cw.close()
        self.assertIn("D;JEQ", _read(path))

    def test_gt_uses_jgt(self) -> None:
        cw, path = _make_writer(self.tmp)
        cw.write_arithmetic("gt")
        cw.close()
        self.assertIn("D;JGT", _read(path))

    def test_lt_uses_jlt(self) -> None:
        cw, path = _make_writer(self.tmp)
        cw.write_arithmetic("lt")
        cw.close()
        self.assertIn("D;JLT", _read(path))

    def test_comparison_labels_are_unique(self) -> None:
        """Duas chamadas de eq devem gerar labels distintos."""
        cw, path = _make_writer(self.tmp)
        cw.write_arithmetic("eq")
        cw.write_arithmetic("eq")
        cw.close()
        asm = _read(path)
        true_labels = [l for l in asm if l.startswith("(CMP_TRUE_")]
        self.assertEqual(len(true_labels), 2)
        self.assertNotEqual(true_labels[0], true_labels[1])

    def test_unknown_command_raises(self) -> None:
        cw, _ = _make_writer(self.tmp)
        with self.assertRaises(ValueError):
            cw.write_arithmetic("xor")
        cw.close()

class TestWritePush(unittest.TestCase):

    def setUp(self) -> None:
        self.tmp = tempfile.mkdtemp()

    def test_push_constant_loads_literal(self) -> None:
        cw, path = _make_writer(self.tmp)
        cw.write_push("constant", 42)
        cw.close()
        asm = _read(path)
        self.assertIn("@42", asm)
        self.assertIn("D=A", asm)

    def test_push_local_uses_lcl(self) -> None:
        cw, path = _make_writer(self.tmp)
        cw.write_push("local", 2)
        cw.close()
        self.assertIn("@LCL", _read(path))

    def test_push_argument_uses_arg(self) -> None:
        cw, path = _make_writer(self.tmp)
        cw.write_push("argument", 0)
        cw.close()
        self.assertIn("@ARG", _read(path))

    def test_push_this_uses_this(self) -> None:
        cw, path = _make_writer(self.tmp)
        cw.write_push("this", 1)
        cw.close()
        self.assertIn("@THIS", _read(path))

    def test_push_that_uses_that(self) -> None:
        cw, path = _make_writer(self.tmp)
        cw.write_push("that", 3)
        cw.close()
        self.assertIn("@THAT", _read(path))

    def test_push_temp_uses_fixed_address(self) -> None:
        cw, path = _make_writer(self.tmp)
        cw.write_push("temp", 3)   
        cw.close()
        self.assertIn("@8", _read(path))

    def test_push_pointer_0_uses_ram3(self) -> None:
        cw, path = _make_writer(self.tmp)
        cw.write_push("pointer", 0)  
        cw.close()
        self.assertIn("@3", _read(path))

    def test_push_pointer_1_uses_ram4(self) -> None:
        cw, path = _make_writer(self.tmp)
        cw.write_push("pointer", 1)  
        cw.close()
        self.assertIn("@4", _read(path))

    def test_push_static_uses_prefixed_symbol(self) -> None:
        cw, path = _make_writer(self.tmp, name="Foo")
        cw.write_push("static", 5)
        cw.close()
        self.assertIn("@Foo.5", _read(path))

    def test_push_increments_sp(self) -> None:
        """Toda push deve incluir M=M+1 para incrementar SP."""
        cw, path = _make_writer(self.tmp)
        cw.write_push("constant", 0)
        cw.close()
        self.assertIn("M=M+1", _read(path))

    def test_push_unknown_segment_raises(self) -> None:
        cw, _ = _make_writer(self.tmp)
        with self.assertRaises(ValueError):
            cw.write_push("unknown", 0)
        cw.close()

class TestWritePop(unittest.TestCase):

    def setUp(self) -> None:
        self.tmp = tempfile.mkdtemp()

    def test_pop_constant_raises(self) -> None:
        cw, _ = _make_writer(self.tmp)
        with self.assertRaises(ValueError):
            cw.write_pop("constant", 0)
        cw.close()

    def test_pop_local_decrements_sp(self) -> None:
        cw, path = _make_writer(self.tmp)
        cw.write_pop("local", 0)
        cw.close()
        self.assertIn("AM=M-1", _read(path))

    def test_pop_local_uses_r13(self) -> None:
        """Pop para segmentos base+index usa R13 como endereço intermediário."""
        cw, path = _make_writer(self.tmp)
        cw.write_pop("local", 1)
        cw.close()
        self.assertIn("@R13", _read(path))

    def test_pop_argument_uses_arg(self) -> None:
        cw, path = _make_writer(self.tmp)
        cw.write_pop("argument", 0)
        cw.close()
        self.assertIn("@ARG", _read(path))

    def test_pop_temp_uses_fixed_address(self) -> None:
        cw, path = _make_writer(self.tmp)
        cw.write_pop("temp", 2)  
        cw.close()
        self.assertIn("@7", _read(path))

    def test_pop_pointer_0_writes_ram3(self) -> None:
        cw, path = _make_writer(self.tmp)
        cw.write_pop("pointer", 0)
        cw.close()
        self.assertIn("@3", _read(path))

    def test_pop_static_uses_prefixed_symbol(self) -> None:
        cw, path = _make_writer(self.tmp, name="Bar")
        cw.write_pop("static", 2)
        cw.close()
        self.assertIn("@Bar.2", _read(path))

    def test_pop_unknown_segment_raises(self) -> None:
        cw, _ = _make_writer(self.tmp)
        with self.assertRaises(ValueError):
            cw.write_pop("unknown", 0)
        cw.close()


class TestWriteProgramFlow(unittest.TestCase):

    def setUp(self) -> None:
        self.tmp = tempfile.mkdtemp()

    def test_label_without_function_uses_original_name(self) -> None:
        cw, path = _make_writer(self.tmp)
        cw.write_label("LOOP")
        cw.close()
        self.assertIn("(LOOP)", _read(path))

    def test_label_is_scoped_to_current_function(self) -> None:
        cw, path = _make_writer(self.tmp)
        cw._current_function = "Main.main"
        cw.write_label("LOOP")
        cw.close()
        self.assertIn("(Main.main$LOOP)", _read(path))

    def test_goto_jumps_to_scoped_label(self) -> None:
        cw, path = _make_writer(self.tmp)
        cw._current_function = "Main.main"
        cw.write_goto("LOOP")
        cw.close()
        asm = _read(path)
        self.assertIn("@Main.main$LOOP", asm)
        self.assertIn("0;JMP", asm)

    def test_if_goto_pops_and_jumps_when_nonzero(self) -> None:
        cw, path = _make_writer(self.tmp)
        cw.write_if("CONTINUE")
        cw.close()
        asm = _read(path)
        self.assertIn("AM=M-1", asm)
        self.assertIn("@CONTINUE", asm)
        self.assertIn("D;JNE", asm)

    def test_camel_case_flow_api(self) -> None:
        cw, path = _make_writer(self.tmp)
        cw.WriteLabel("START")
        cw.WriteGoto("START")
        cw.WriteIf("START")
        cw.close()
        asm = _read(path)
        self.assertIn("(START)", asm)
        self.assertEqual(asm.count("@START"), 2)


class TestWriteCallAndBootstrap(unittest.TestCase):

    def setUp(self) -> None:
        self.tmp = tempfile.mkdtemp()

    def test_call_pushes_return_address_and_saved_segments(self) -> None:
        cw, path = _make_writer(self.tmp)
        cw.write_call("Main.main", 2)
        cw.close()
        asm = _read(path)
        self.assertIn("@VM$ret.0", asm)
        self.assertIn("(VM$ret.0)", asm)
        for segment in ("@LCL", "@ARG", "@THIS", "@THAT"):
            self.assertIn(segment, asm)
        self.assertEqual(asm.count("M=M+1"), 5)

    def test_call_repositions_arg_and_lcl(self) -> None:
        cw, path = _make_writer(self.tmp)
        cw.write_call("Math.multiply", 2)
        cw.close()
        asm = _read(path)
        arg_setup = [
            "@SP", "D=M", "@5", "D=D-A", "@2", "D=D-A", "@ARG", "M=D"
        ]
        start = next(
            index
            for index in range(len(asm))
            if asm[index:index + len(arg_setup)] == arg_setup
        )
        self.assertGreaterEqual(start, 0)
        self.assertIn("@Math.multiply", asm)

    def test_calls_use_unique_return_labels(self) -> None:
        cw, path = _make_writer(self.tmp)
        cw.write_call("Foo.first", 0)
        cw.write_call("Foo.second", 0)
        cw.close()
        labels = [line for line in _read(path) if line.startswith("(VM$ret.")]
        self.assertEqual(labels, ["(VM$ret.0)", "(VM$ret.1)"])

    def test_call_rejects_negative_argument_count(self) -> None:
        cw, _ = _make_writer(self.tmp)
        with self.assertRaises(ValueError):
            cw.write_call("Main.main", -1)
        cw.close()

    def test_bootstrap_sets_sp_and_calls_sys_init(self) -> None:
        cw, path = _make_writer(self.tmp)
        cw.write_init()
        cw.close()
        asm = _read(path)
        self.assertEqual(asm[:4], ["@256", "D=A", "@SP", "M=D"])
        self.assertIn("@Sys.init", asm)
        self.assertIn("(VM$ret.0)", asm)

    def test_camel_case_call_and_bootstrap_api(self) -> None:
        cw, path = _make_writer(self.tmp)
        cw.WriteInit()
        cw.WriteCall("Main.main", 0)
        cw.close()
        asm = _read(path)
        self.assertIn("@Sys.init", asm)
        self.assertIn("@Main.main", asm)

class TestIntegration(unittest.TestCase):

    def setUp(self) -> None:
        self.tmp = tempfile.mkdtemp()

    def test_push_constant_and_add(self) -> None:
        """push constant 3 / push constant 4 / add → deve gerar M=D+M."""
        cw, path = _make_writer(self.tmp)
        cw.write_push("constant", 3)
        cw.write_push("constant", 4)
        cw.write_arithmetic("add")
        cw.close()
        asm = _read(path)
        self.assertIn("M=D+M", asm)

    def test_close_writes_infinite_loop(self) -> None:
        cw, path = _make_writer(self.tmp)
        cw.close()
        asm = _read(path)
        self.assertIn("(END)", asm)
        self.assertIn("0;JMP", asm)


if __name__ == "__main__":
    unittest.main(verbosity=2)
