import sys

# THE INSTRUCTION SET ARCHITECTURE (OPCODE MAP)
OPCODES = {
    "MOV AX,BX": "89D8",
    "MOV BX,AX": "89C3",
    "ADD AX,BX": "01D8",
    "SUB AX,BX": "29D8",
    "HLT": "F4"
}

def assemble_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"[!] Error: Could not find the file '{file_path}'")
        return

    print("\n" + "="*50)
    print("      CUSTOM 8086 ASSEMBLER - COMPILATION LOG")
    print("="*50)
    print("Address | Machine Code | Assembly Source")
    print("-" * 50)

    # 8086 COM files traditionally load into memory at offset 0100h
    memory_address = 0x0100  
    machine_code_stream = []
    error_flag = False

    # LEXICAL ANALYSIS AND PARSING
    for line_number, raw_line in enumerate(lines, start=1):
        # Clean the string: remove comments (anything after ';') and whitespace
        clean_line = raw_line.split(';')[0].strip().upper()
        
        # Skip empty lines
        if not clean_line:
            continue

        # Standardize syntax (e.g., "MOV AX, BX" becomes "MOV AX,BX")
        clean_line = clean_line.replace(', ', ',')

        # Translate to Machine Code
        if clean_line in OPCODES:
            hex_opcode = OPCODES[clean_line]
            
            # Print the formatted output table
            print(f"{memory_address:04X}    | {hex_opcode:<12} | {raw_line.strip()}")
            
            machine_code_stream.append(hex_opcode)
            
            # Increment memory address by the number of bytes in the instruction
            # (2 hex characters = 1 byte)
            memory_address += len(hex_opcode) // 2
        else:
            print(f"{memory_address:04X}    | [SYNTAX ERROR] | {raw_line.strip()}")
            print(f"\n[!] Compilation failed at line {line_number}: Unknown instruction.")
            error_flag = True
            break

    # 3. BINARY OUTPUT GENERATION
    if not error_flag:
        print("-" * 50)
        print("Compilation Successful. Zero syntax errors.")
        final_hex = ' '.join(machine_code_stream)
        print(f"\n[FINAL HEX STREAM]: {final_hex}\n")

# EXECUTION BLOCK
if __name__ == "__main__":
    # First, let's write a temporary Assembly file to test our compiler
    test_program = [
        "MOV AX, BX    ; Move data from BX into the AX register",
        "ADD AX, BX    ; Add the values together",
        "SUB AX, BX    ; Subtract the value back",
        "HLT           ; Halt processor execution"
    ]
    
    # Generate the source file
    with open("test_program.asm", "w") as f:
        for instruction in test_program:
            f.write(instruction + "\n")
            
    print("Created 'test_program.asm'. Beginning compilation...")
    
    # Run the compiler on the file we just created
    assemble_file("test_program.asm")