// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.


// LOOP
(LOOP)
// if key is down
//   color = -1
// else
//   color = 0
@KBD
D=M // Load keyboard into D
@KEY_NOT_DOWN
D;JEQ // If it's not set, jump to else
@0 // Load 0 (intended value + 1)
D=A
@STORE
0;JMP
(KEY_NOT_DOWN)
@1 // Load 1 (indended value + 1)
D=A
(STORE)
@color
D=D-1
M=D

// i = 0
@0
D=A
@i
M=D
(PAINT_LOOP)
// if i >= 8192
//   goto END
@i
D=M
@8192
D=D-A
@END
D;JGE
// m[SCREEN + i] = color
// Store SCREEN + i -> to_paint
@i
D=M
@SCREEN
D=A+D
@to_paint
M=D
// Load color
@color
D=M
// Store color -> to_paint
@to_paint
A=M
M=D

// i++
@i
M=M+1

@PAINT_LOOP
0;JMP

(END)
@LOOP
0;JMP
