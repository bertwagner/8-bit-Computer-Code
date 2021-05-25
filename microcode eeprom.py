# https://www.reddit.com/r/beneater/comments/m0f6xl/generating_a_bin_file_for_the_eeprom/
# https://github.com/beneater/eeprom-programmer/blob/master/microcode-eeprom-with-flags/microcode-eeprom-with-flags.ino

import math
import sys
import copy

rom_size = 2048  # However big your EEPROM is

data = [0] * rom_size   # Preallocate the data, all zeros

HLT = 0b1000000000000000  # Halt clock
MI  = 0b0100000000000000  # Memory address register in
RI  = 0b0010000000000000  # RAM data in
RO  = 0b0001000000000000  # RAM data out
IO  = 0b0000100000000000  # Instruction register out
II  = 0b0000010000000000  # Instruction register in
AI  = 0b0000001000000000  # A register in
AO  = 0b0000000100000000  # A register out
EO  = 0b0000000010000000  # ALU out
SU  = 0b0000000001000000  # ALU subtract
BI  = 0b0000000000100000  # B register in
OI  = 0b0000000000010000  # Output register in
CE  = 0b0000000000001000  # Program counter enable
CO  = 0b0000000000000100  # Program counter out
J   = 0b0000000000000010  # Jump (program counter in)
FI  = 0b0000000000000001  # Flags register in

FLAGS_Z0C0 = 0 
FLAGS_Z0C1 = 1
FLAGS_Z1C0 = 2
FLAGS_Z1C1 = 3

JC = 0b0111
JZ = 0b1000

template = [
  [MI|CO,  RO|II|CE,  0,      0,      0,             0, 0, 0],   # 0000 - NOP No operation
  [MI|CO,  RO|II|CE,  IO|MI,  RO|AI,  0,             0, 0, 0],   # 0001 - LDA Load A
  [MI|CO,  RO|II|CE,  IO|MI,  RO|BI,  EO|AI|FI,      0, 0, 0],   # 0010 - ADD Add
  [MI|CO,  RO|II|CE,  IO|MI,  RO|BI,  EO|AI|SU|FI,   0, 0, 0],   # 0011 - SUB Subtract
  [MI|CO,  RO|II|CE,  IO|MI,  AO|RI,  0,             0, 0, 0],   # 0100 - STA Store A
  [MI|CO,  RO|II|CE,  IO|AI,  0,      0,             0, 0, 0],   # 0101 - LDI Load In
  [MI|CO,  RO|II|CE,  IO|J,   0,      0,             0, 0, 0],   # 0110 - JMP Jump
  [MI|CO,  RO|II|CE,  0,      0,      0,             0, 0, 0],   # 0111 - JC Jump Carry
  [MI|CO,  RO|II|CE,  0,      0,      0,             0, 0, 0],   # 1000 - JZ Jump Zero
  [MI|CO,  RO|II|CE,  0,      0,      0,             0, 0, 0],   # 1001
  [MI|CO,  RO|II|CE,  0,      0,      0,             0, 0, 0],   # 1010
  [MI|CO,  RO|II|CE,  0,      0,      0,             0, 0, 0],   # 1011
  [MI|CO,  RO|II|CE,  0,      0,      0,             0, 0, 0],   # 1100
  [MI|CO,  RO|II|CE,  0,      0,      0,             0, 0, 0],   # 1101
  [MI|CO,  RO|II|CE,  AO|OI,  0,      0,             0, 0, 0],   # 1110 - OUT Output
  [MI|CO,  RO|II|CE,  HLT,    0,      0,             0, 0, 0],   # 1111 - HLT Halt
]

# Copy the template 4 times into microcode, one for each combo of carry and zero flag values
microcodes = [
    # ZF = 0, CF = 0
    copy.deepcopy(template),
    
    # ZF = 0, CF = 1
    copy.deepcopy(template),
    
    # ZF = 1, CF =0
    copy.deepcopy(template),
    
    # ZF = 1, CF =1
    copy.deepcopy(template)
]

# update the commands for the copies that have carry and zero flag bits
microcodes[FLAGS_Z0C1][JC][2] = IO|J
microcodes[FLAGS_Z1C0][JZ][2] = IO|J
microcodes[FLAGS_Z1C1][JC][2] = IO|J
microcodes[FLAGS_Z1C1][JZ][2] = IO|J

# Program the 8 high-order bits of microcode into the first 128 bytes of EEPROM
for address in range(1024):

    flags       = (address & 0b1100000000) >> 8
    byte_sel    = (address & 0b0010000000) >> 7
    instruction = (address & 0b0001111000) >> 3
    step        = (address & 0b0000000111)

    if address == 128:
        t=0

    if (byte_sel):
      data[address] = (microcodes[flags][instruction][step] & 0b0000000011111111)
    else:
      data[address] = (microcodes[flags][instruction][step] & 0b1111111100000000) >> 8

# Convert the data array to binary bytes and write it to a file
with open("microcode eeprom.bin", "wb") as f:
    f.write(bytes(data))
    f.close()
