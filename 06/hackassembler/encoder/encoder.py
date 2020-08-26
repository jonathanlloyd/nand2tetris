"""Logic for encoding parsed tokens into binary machine code"""


from parser import (
    AInstruction,
    CInstruction,
    CalcOperation,
    DestRegister,
    JumpCondition,
)


CALC_OPERATION_ENCODING = {
    CalcOperation.ZERO:        '0101010',
    CalcOperation.ONE:         '0111111',
    CalcOperation.MINUS_ONE:   '0111010',
    CalcOperation.D:           '0001100',
    CalcOperation.A:           '0110000',
    CalcOperation.NOT_D:       '0001101',
    CalcOperation.NOT_A:       '0110001',
    CalcOperation.MINUS_D:     '0001111',
    CalcOperation.MINUS_A:     '0110011',
    CalcOperation.D_PLUS_ONE:  '0011111',
    CalcOperation.A_PLUS_ONE:  '0110111',
    CalcOperation.D_MINUS_ONE: '0001110',
    CalcOperation.A_MINUS_ONE: '0110010',
    CalcOperation.D_PLUS_A:    '0000010',
    CalcOperation.D_MINUS_A:   '0010011',
    CalcOperation.A_MINUS_D:   '0000111',
    CalcOperation.D_AND_A:     '0000000',
    CalcOperation.D_OR_A:      '0010101',

    CalcOperation.M:           '1110000',
    CalcOperation.NOT_M:       '1110001',
    CalcOperation.MINUS_M:     '1110011',
    CalcOperation.M_PLUS_ONE:  '1110111',
    CalcOperation.M_MINUS_ONE: '1110010',
    CalcOperation.D_PLUS_M:    '1000010',
    CalcOperation.D_MINUS_M:   '1010011',
    CalcOperation.M_MINUS_D:   '1000111',
    CalcOperation.D_AND_M:     '1000000',
    CalcOperation.D_OR_M:      '1010101',
}

DEST_ENCODING = {
    DestRegister.NULL: '000',
    DestRegister.M:    '001',
    DestRegister.D:    '010',
    DestRegister.MD:   '011',
    DestRegister.A:    '100',
    DestRegister.AM:   '101',
    DestRegister.AD:   '110',
    DestRegister.AMD:  '111',
}

JUMP_CONDITION_ENCODING = {
    JumpCondition.NULL:                  '000',
    JumpCondition.GREATER_THAN:          '001',
    JumpCondition.EQUAL:                 '010',
    JumpCondition.GREATER_THAN_OR_EQUAL: '011',
    JumpCondition.LESS_THAN:             '100',
    JumpCondition.NOT_EQUAL:             '101',
    JumpCondition.LESS_THAN_OR_EQUAL:    '110',
    JumpCondition.UNCONDITIONAL:         '111',
}


def encode(tokens):
    output = ''
    for t in tokens:
        output += f'{_encode_token(t)}\n'
    return output


def _encode_token(token):
    if isinstance(token, AInstruction):
        return _encode_a_instruction(token)
    elif isinstance(token, CInstruction):
        return _encode_c_instruction(token)
    else:
        raise ValueError(f'Unknown token type: {type(token)}')


def _encode_a_instruction(instruction):
    return f'{instruction.value:016b}'


def _encode_c_instruction(instruction):
    calc_operation = _encode_calc_operation(instruction.calc)
    dest = _encode_dest(instruction.dest)
    jump_condition = _encode_jump_condition(instruction.jump_condition)
    return f'111{calc_operation}{dest}{jump_condition}'

def _encode_calc_operation(calc_operation):
    if calc_operation not in CALC_OPERATION_ENCODING:
        raise ValueError(f'Unknown calc operation: {calc_operation}')
    return CALC_OPERATION_ENCODING[calc_operation]

def _encode_dest(dest):
    if dest not in DEST_ENCODING:
        raise ValueError(f'Unknown dest register: {dest}')
    return DEST_ENCODING[dest]

def _encode_jump_condition(jump_condition):
    if jump_condition not in JUMP_CONDITION_ENCODING:
        raise ValueError(f'Unknown jump condition: {jump_condition}')
    return JUMP_CONDITION_ENCODING[jump_condition]
