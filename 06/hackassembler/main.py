"""Assembler for Hack assembly -> Hack ISA"""

import sys

from encoder import encode
from parser import parse


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} <assembly file>')
        sys.exit(1)

    assembly_file_name = sys.argv[1]

    assembly_file_name_parts = assembly_file_name.rsplit('.', 1)
    if (
        len(assembly_file_name_parts) != 2
        or assembly_file_name_parts[1] != 'asm'
    ):
        print('Assembly file name must take the form: <name>.asm')
        sys.exit(1)

    with open(assembly_file_name, 'r') as f:
        assembly_file_contents = f.read()

    try:
        machine_code = encode(parse(assembly_file_contents))
    except ValueError as e:
        print(e)
        sys.exit(1)

    output_file_name = f'{assembly_file_name_parts[0]}.hack'
    with open(output_file_name, 'w') as f:
        f.write(machine_code)

