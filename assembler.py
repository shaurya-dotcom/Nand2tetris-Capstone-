#!/usr/bin/env python3
"""Two-pass Hack assembler for the Nand to Tetris Hack ISA."""
import argparse
import re
from pathlib import Path

PREDEFINED = {
    "SP":0, "LCL":1, "ARG":2, "THIS":3, "THAT":4,
    "SCREEN":16384, "KBD":24576,
}
PREDEFINED.update({f"R{i}":i for i in range(16)})

DEST = {
    "": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "DM": "011",
    "A": "100",
    "AM": "101",
    "MA": "101",
    "AD": "110",
    "DA": "110",
    "AMD": "111",
    "ADM": "111",
    "MAD": "111",
    "MDA": "111",
    "DAM": "111",
    "DMA": "111"
}
JUMP = {"": "000", "JGT":"001", "JEQ":"010", "JGE":"011",
        "JLT":"100", "JNE":"101", "JLE":"110", "JMP":"111"}
COMP = {
 "0":"0101010","1":"0111111","-1":"0111010",
 "D":"0001100","A":"0110000","M":"1110000",
 "!D":"0001101","!A":"0110001","!M":"1110001",
 "-D":"0001111","-A":"0110011","-M":"1110011",
 "D+1":"0011111","A+1":"0110111","M+1":"1110111",
 "D-1":"0001110","A-1":"0110010","M-1":"1110010",
 "D+A":"0000010","D+M":"1000010","D-A":"0010011",
 "D-M":"1010011","A-D":"0000111","M-D":"1000111",
 "D&A":"0000000","D&M":"1000000","D|A":"0010101","D|M":"1010101",
}
SYMBOL_RE = re.compile(r"^[A-Za-z_.$:][A-Za-z0-9_.$:]*$")

def clean_lines(path):
    result=[]
    for line_no, raw in enumerate(Path(path).read_text(encoding="utf-8").splitlines(),1):
        line=raw.split("//",1)[0].strip()
        if line:
            result.append((line_no,line))
    return result

def assemble(source, output=None, symbols_path="symbols.txt"):
    lines=clean_lines(source)
    symbols=dict(PREDEFINED)
    rom=0
    # First pass: labels.
    for line_no,line in lines:
        if line.startswith("(") and line.endswith(")"):
            label=line[1:-1].strip()
            if not SYMBOL_RE.match(label):
                raise ValueError(f"Line {line_no}: invalid label '{label}'")
            if label in symbols:
                print(f"Warning: Line {line_no}: label '{label}' already defined")
            else:
                symbols[label]=rom
        else:
            rom+=1

    # Second pass: A/C instructions and variables.
    next_var=16
    machine=[]
    for line_no,line in lines:
        if line.startswith("(") and line.endswith(")"):
            continue
        if line.startswith("@"):
            value=line[1:].strip()
            if value.isdigit():
                address=int(value)
            else:
                if not SYMBOL_RE.match(value):
                    raise ValueError(f"Line {line_no}: invalid instruction '{line}'")
                if value not in symbols:
                    symbols[value]=next_var
                    next_var+=1
                address=symbols[value]
            if not 0 <= address <= 32767:
                raise ValueError(f"Line {line_no}: A-instruction address out of range: {address}")
            machine.append(f"{address:016b}")
            continue

        dest, comp, jump = "", line, ""
        if "=" in line:
            dest,rest=line.split("=",1)
        else:
            rest=line
        if ";" in rest:
            comp,jump=rest.split(";",1)
        else:
            comp=rest
        dest,comp,jump=dest.strip(),comp.strip(),jump.strip()
        if comp not in COMP or dest not in DEST or jump not in JUMP:
            raise ValueError(f"Line {line_no}: invalid instruction '{line}'")
        machine.append("111"+COMP[comp]+DEST[dest]+JUMP[jump])

    output=Path(output or Path(source).with_suffix(".hack"))
    output.write_text("\n".join(machine)+"\n",encoding="utf-8")
    Path(symbols_path).write_text(
        "\n".join(f"{name}={address}" for name,address in sorted(symbols.items(),key=lambda x:(x[1],x[0])))+"\n",
        encoding="utf-8")
    print(f"Assembled {source} -> {output} ({len(machine)} instructions)")
    return machine

if __name__=="__main__":
    parser=argparse.ArgumentParser(description="Assemble Hack .asm to .hack")
    parser.add_argument("source",help="input .asm file")
    parser.add_argument("-o","--output",help="output .hack file")
    parser.add_argument("--symbols",default="symbols.txt",help="symbol table output")
    args=parser.parse_args()
    try:
        assemble(args.source,args.output,args.symbols)
    except (ValueError,OSError) as exc:
        print(exc)
        raise SystemExit(1)
