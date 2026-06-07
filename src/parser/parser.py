from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class CommandType(str, Enum):
    C_ARITHMETIC = "C_ARITHMETIC"
    C_PUSH = "C_PUSH"
    C_POP = "C_POP"


ARITHMETIC_COMMANDS = {
    "add",
    "sub",
    "neg",
    "eq",
    "gt",
    "lt",
    "and",
    "or",
    "not",
}


@dataclass(frozen=True)
class ParsedCommand:
    tokens: list[str]


class Parser:
    def __init__(self, filename: str) -> None:
        self._commands: list[ParsedCommand] = []
        self._index = 0
        self._current: ParsedCommand | None = None

        with open(filename, "r", encoding="utf-8") as source:
            for raw_line in source:
                clean_line = raw_line.split("//", maxsplit=1)[0].strip()
                if not clean_line:
                    continue

                tokens = clean_line.split()
                self._commands.append(ParsedCommand(tokens=tokens))

    def has_more_commands(self) -> bool:
        return self._index < len(self._commands)

    def advance(self) -> None:
        if not self.has_more_commands():
            self._current = None
            return

        self._current = self._commands[self._index]
        self._index += 1

    def command_type(self) -> CommandType:
        current = self._require_current_command()
        command = current.tokens[0]

        if command in ARITHMETIC_COMMANDS:
            return CommandType.C_ARITHMETIC
        if command == "push":
            return CommandType.C_PUSH
        if command == "pop":
            return CommandType.C_POP

        raise ValueError(f"Unsupported VM command: {command}")

    def arg1(self) -> str:
        current = self._require_current_command()
        if self.command_type() == CommandType.C_ARITHMETIC:
            return current.tokens[0]

        return current.tokens[1]

    def arg2(self) -> int:
        current = self._require_current_command()
        cmd_type = self.command_type()
        if cmd_type not in {CommandType.C_PUSH, CommandType.C_POP}:
            raise ValueError("arg2 is only valid for C_PUSH and C_POP commands")

        return int(current.tokens[2])

    # API compatível com o enunciado
    def HasMoreCommands(self) -> bool:  # noqa: N802
        return self.has_more_commands()

    def Advance(self) -> None:  # noqa: N802
        self.advance()

    def CommandType(self) -> str:  # noqa: N802
        return self.command_type().value

    def Arg1(self) -> str:  # noqa: N802
        return self.arg1()

    def Arg2(self) -> int:  # noqa: N802
        return self.arg2()

    def _require_current_command(self) -> ParsedCommand:
        if self._current is None:
            raise ValueError("No current command. Call advance() first.")

        return self._current
