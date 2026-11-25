# Nand to Tetris Capstone source code

## Included
- `CPU.hdl`, `Memory.hdl`, `Computer.hdl`
- `assembler.py`: two-pass Hack assembler
- `generate_box.py`: generates a K-specific `Box.asm`
- `Box.asm`: example template for K=41 (edit/regenerate for your K)

## Generate your own box
Use the last two digits of your roll number:

```bash
python generate_box.py 41
python assembler.py Box.asm -o Box.hack --symbols symbols.txt
```

Replace `41` with your own K. Width is 16*((K mod 4)+1) pixels, height 20 rows,
starting at row K. The program draws while a keyboard key is pressed and erases
when released.

## Assemble standard programs
```bash
python assembler.py Add.asm
python assembler.py Max.asm
python assembler.py Rect.asm
python assembler.py Pong.asm
```

## Important
These HDL files are intended for the standard Nand2Tetris Project 5 chip set.
Run the official CPU, Memory, and Computer test scripts in the HDL simulator.
If your course simulator has different built-in chip names or syntax, adjust
the chip interfaces to match it. Make sure you can explain every part for viva.
