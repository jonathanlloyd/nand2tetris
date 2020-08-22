// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

@0
D=A
// i = 0
@i
M=D
// j = 0
@j
M=D
// acc = 0
@acc
M=D

(LOOP)
// if i >= R0
//   goto END
@i
D=M
@R0
D=D-M
@END
D;JGE

// i += 1
@i
M=M+1

// ACC += R1
@R1
D=M
@acc
M=D+M

// goto LOOP
@LOOP
0;JMP

// END
// R2 = acc
(END)
@acc
D=M
@R2
M=D

@END
0;JMP
