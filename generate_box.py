#!/usr/bin/env python3
"""Generate Box.asm for the capstone using personal number K."""
import argparse
from pathlib import Path

def make_box(k):
    if not 0 <= k <= 99:
        raise ValueError("K must be between 0 and 99.")
    words=(k % 4)+1
    start=16384+32*k
    gap=32-words
    return f"""// Capstone Box program
// Personal number K = {k}
// Starts at row {k}; height 20 rows; width {words*16} pixels.
// Hold any key to draw; release it to erase.

(LOOP)
@KBD
D=M
@DRAW
D;JGT
@ERASE
0;JMP

(DRAW)
@{start}
D=A
@R13
M=D
@20
D=A
@R14
M=D
(DRAW_ROW)
@{words}
D=A
@R15
M=D
(DRAW_WORD)
@R13
A=M
M=-1
@R13
M=M+1
@R15
M=M-1
@DRAW_WORD
D;JGT
@{gap}
D=A
@R13
M=D+M
@R14
M=M-1
@DRAW_ROW
D;JGT
@LOOP
0;JMP

(ERASE)
@{start}
D=A
@R13
M=D
@20
D=A
@R14
M=D
(ERASE_ROW)
@{words}
D=A
@R15
M=D
(ERASE_WORD)
@R13
A=M
M=0
@R13
M=M+1
@R15
M=M-1
@ERASE_WORD
D;JGT
@{gap}
D=A
@R13
M=D+M
@R14
M=M-1
@ERASE_ROW
D;JGT
@LOOP
0;JMP
"""

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("K",type=int,help="last two digits of university roll number")
    p.add_argument("-o","--output",default="Box.asm")
    a=p.parse_args()
    Path(a.output).write_text(make_box(a.K),encoding="utf-8")
    print(f"Generated {a.output}: row {a.K}, height 20, width {((a.K%4)+1)*16}px")
