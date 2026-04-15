# Custom 8086 Assembler

A minimal Python-based assembler for a subset of the Intel 8086 instruction set. Translates human-readable assembly source files (`.asm`) into 16-bit x86 machine code hex streams, with a formatted compilation log showing addresses, opcodes, and source lines.

---

## Overview

The assembler performs single-pass lexical analysis on `.asm` source files, normalises syntax, maps mnemonics to their correct 8086 machine code encodings, and outputs a hex stream. It also auto-generates a `test_program.asm` source file to demonstrate the full pipeline when run directly.

Memory addressing follows the DOS COM file convention, starting at offset `0x0100`.

---

## Supported Instructions

All opcodes are verified against the Intel 8086 instruction encoding specification (ModRM byte, 16-bit register encodings):

| Mnemonic     | Machine Code | Description                        |
|--------------|--------------|------------------------------------|
| `MOV AX, BX` | `89 D8`      | Copy BX into AX                    |
| `MOV BX, AX` | `89 C3`      | Copy AX into BX                    |
| `ADD AX, BX` | `01 D8`      | Add BX to AX, result in AX         |
| `SUB AX, BX` | `29 D8`      | Subtract BX from AX, result in AX  |
| `HLT`        | `F4`         | Halt processor execution           |

> **Note:** These are 2-byte register-to-register encodings using the `89 /r` (MOV), `01 /r` (ADD), and `29 /r` (SUB) opcode forms with a ModRM byte of `0xD8` or `0xC3`. `HLT` is a single-byte instruction.

---

## Requirements

- Python 3.6+
- Standard library only (`sys`)

---

## Usage

### Run with the built-in test program

Running the script directly auto-generates `test_program.asm` and assembles it:

```bash
python custom_assembler.py
```

**Output:**
```
Created 'test_program.asm'. Beginning compilation...

==================================================
      CUSTOM 8086 ASSEMBLER - COMPILATION LOG
==================================================
Address | Machine Code | Assembly Source
--------------------------------------------------
0100    | 89D8         | MOV AX, BX    ; Move data from BX into the AX register
0102    | 01D8         | ADD AX, BX    ; Add the values together
0104    | 29D8         | SUB AX, BX    ; Subtract the value back
0106    | F4           | HLT           ; Halt processor execution
--------------------------------------------------
Compilation Successful. Zero syntax errors.

[FINAL HEX STREAM]: 89D8 01D8 29D8 F4
```

### Assemble a custom file

```python
from custom_assembler import assemble_file
assemble_file("my_program.asm")
```

---

## Assembly Source Format (`test_program.asm`)

```asm
MOV AX, BX    ; Move data from BX into the AX register
ADD AX, BX    ; Add the values together
SUB AX, BX    ; Subtract the value back
HLT           ; Halt processor execution
```

- **Comments** begin with `;` and are stripped before parsing
- **Whitespace** around commas is normalised (`MOV AX, BX` → `MOV AX,BX`)
- Instructions are **case-insensitive** (converted to uppercase internally)
- Empty lines are skipped

---

## Error Handling

If an unrecognised instruction is encountered, assembly halts immediately with a diagnostic:

```
0104    | [SYNTAX ERROR] | PUSH CX
[!] Compilation failed at line 3: Unknown instruction.
```

---

## Limitations & Potential Extensions

- **No immediate operands** — instructions like `MOV AX, 5` or `ADD AX, 42` are not supported
- **No labels or jump instructions** — control flow (`JMP`, `JE`, `CALL`, `RET`) would require a two-pass assembler
- **Register subset only** — only `AX` and `BX` are covered; `CX`, `DX`, segment registers, and memory operands are not implemented
- **No binary file output** — the hex stream is printed but not written to a `.bin` or `.com` file

Extending the `OPCODES` dictionary and adding an immediate-value parser would be the natural next steps.
