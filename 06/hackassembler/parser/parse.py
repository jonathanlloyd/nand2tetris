"""Parsing logic for hackassembler"""

from dataclasses import dataclass
from enum import Enum
import typing


class AInstructionKind(Enum):
    NUMERIC = 1
    SYMBOL = 2


@dataclass
class AInstruction:
    kind: AInstructionKind
    value: typing.Union[str,int]


class DestRegister(Enum):
    NULL = 1
    M    = 2
    D    = 3
    MD   = 4
    A    = 5
    AM   = 6
    AD   = 7
    AMD  = 8

    @staticmethod
    def from_str(s):
        if s == 'M':
            return DestRegister.M
        elif s == 'D':
            return DestRegister.D
        elif s == 'MD':
            return DestRegister.MD
        elif s == 'A':
            return DestRegister.A
        elif s == 'AM':
            return DestRegister.AM
        elif s == 'AD':
            return DestRegister.AD
        elif s == 'AMD':
            return DestRegister.AMD
        else:
            raise ValueError(f'Unknown dest register: {s}')


class CalcOperation(Enum):
    ZERO        = 1
    ONE         = 2
    MINUS_ONE   = 3
    D           = 4
    A           = 5
    NOT_D       = 6
    NOT_A       = 7
    MINUS_D     = 8
    MINUS_A     = 9
    D_PLUS_ONE  = 10
    A_PLUS_ONE  = 11
    D_MINUS_ONE = 12
    A_MINUS_ONE = 13
    D_PLUS_A    = 14
    D_MINUS_A   = 15
    A_MINUS_D   = 16
    D_AND_A     = 17
    D_OR_A      = 18
    M           = 19
    NOT_M       = 20
    MINUS_M     = 21
    M_PLUS_ONE  = 22
    M_MINUS_ONE = 23
    D_PLUS_M    = 24
    D_MINUS_M   = 25
    M_MINUS_D   = 26
    D_AND_M     = 27
    D_OR_M      = 28

    @staticmethod
    def from_str(s):
        if s == '0':
            return CalcOperation.ZERO
        elif s == '1':
            return CalcOperation.ONE
        elif s == '-1':
            return CalcOperation.MINUS_ONE
        elif s == 'D':
            return CalcOperation.D
        elif s == 'A':
            return CalcOperation.A
        elif s == '!D':
            return CalcOperation.NOT_D
        elif s == '!A':
            return CalcOperation.NOT_A
        elif s == '-D':
            return CalcOperation.MINUS_D
        elif s == '-A':
            return CalcOperation.MINUS_A
        elif s == 'D+1':
            return CalcOperation.D_PLUS_ONE
        elif s == 'A+1':
            return CalcOperation.A_PLUS_ONE
        elif s == 'D-1':
            return CalcOperation.D_MINUS_ONE
        elif s == 'A-1':
            return CalcOperation.A_MINUS_ONE
        elif s == 'D+A':
            return CalcOperation.D_PLUS_A
        elif s == 'D-A':
            return CalcOperation.D_MINUS_A
        elif s == 'A-D':
            return CalcOperation.A_MINUS_D
        elif s == 'D&A':
            return CalcOperation.D_AND_A
        elif s == 'D|A':
            return CalcOperation.D_OR_A
        elif s == 'M':
            return CalcOperation.M
        elif s == '!M':
            return CalcOperation.NOT_M
        elif s == '-M':
            return CalcOperation.MINUS_M
        elif s == 'M+1':
            return CalcOperation.M_PLUS_ONE
        elif s == 'M-1':
            return CalcOperation.M_MINUS_ONE
        elif s == 'D+M':
            return CalcOperation.D_PLUS_M
        elif s == 'D-M':
            return CalcOperation.D_MINUS_M
        elif s == 'M-D':
            return CalcOperation.M_MINUS_D
        elif s == 'D&M':
            return CalcOperation.D_AND_M
        elif s == 'D|M':
            return CalcOperation.D_OR_M
        else:
            raise ValueError(f'Unknown calculation: {s}')


class JumpCondition(Enum):
    NULL                  = 1
    GREATER_THAN          = 2
    EQUAL                 = 3
    GREATER_THAN_OR_EQUAL = 4
    LESS_THAN             = 5
    NOT_EQUAL             = 6
    LESS_THAN_OR_EQUAL    = 7
    UNCONDITIONAL         = 8

    @staticmethod
    def from_str(s):
        if s == 'JGT':
            return JumpCondition.GREATER_THAN
        elif s == 'JEQ':
            return JumpCondition.EQUAL
        elif s == 'JGE':
            return JumpCondition.GREATER_THAN_OR_EQUAL
        elif s == 'JLT':
            return JumpCondition.LESS_THAN
        elif s == 'JNE':
            return JumpCondition.NOT_EQUAL
        elif s == 'JLE':
            return JumpCondition.LESS_THAN_OR_EQUAL
        elif s == 'JMP':
            return JumpCondition.UNCONDITIONAL
        else:
            raise ValueError(f'Unknown jump condition: {s}')



@dataclass
class CInstruction:
    dest: DestRegister
    calc: CalcOperation
    jump_condition: JumpCondition


def parse(input_str):
    tokens = []
    for line_num, line in enumerate(input_str.split('\n')):
        try:
            token = _parse_line(line)
        except ValueError as e:
            raise ValueError(f'Error on line {line_num + 1}: {e}')

        if token:
            tokens.append(token)

    return tokens


def _parse_line(line):
    line = _remove_whitespace(line)

    if line == '':
        parsed_line = None
    elif line.startswith('@'):
        parsed_line = _parse_a_instruction(line)
    else:
        parsed_line = _parse_c_instruction(line)

    return parsed_line


def _parse_a_instruction(line):
    instruction_value = line[1:]
    if _is_numeric(instruction_value):
        return AInstruction(
            kind=AInstructionKind.NUMERIC,
            value=int(instruction_value),
        )
    else:
        return AInstruction(
            kind=AInstructionKind.SYMBOL,
            value=instruction_value,
        )


def _parse_c_instruction(line):
    if '=' in line:
        dest_str, line = line.split('=', 1)
        dest = DestRegister.from_str(dest_str)
    else:
        dest = DestRegister.NULL

    if ';' in line:
        calc_str, line = line.split(';', 1)
        calc = CalcOperation.from_str(calc_str)
    else:
        calc = CalcOperation.from_str(line)
        line = ''

    if line:
        jump_condition = JumpCondition.from_str(line)
    else:
        jump_condition = JumpCondition.NULL

    return CInstruction(
        dest=dest,
        calc=calc,
        jump_condition=jump_condition,
    )



def _is_numeric(line):
    is_numeric = True
    try:
        int(line)
    except:
        is_numeric = False

    return is_numeric


def _remove_whitespace(line):
    comment_index = line.find('//')
    if comment_index > -1:
        line = line[:comment_index]
    return line.strip()
