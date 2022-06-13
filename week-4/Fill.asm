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

// Put your code here.

@past
M=0

(MAIN)
@KBD
D=M

@NOTPRESSED
D;JEQ

@present
M=-1
@COMPARE
0;JMP

(NOTPRESSED)
@present
M=0

(COMPARE)
@past
D=M
@present
D=D-M
@MAIN
D;JEQ

@SCREEN
D=A
@i
M=D
(LOOP)
@present
D=M

@i
A=M
M=D

@past
M=D

@i
M=M+1

@KBD
D=A

@i
D=M-D
@MAIN
D;JGT

@LOOP
0;JMP
