# https://www.reddit.com/r/beneater/comments/m0f6xl/generating_a_bin_file_for_the_eeprom/
# https://github.com/beneater/eeprom-programmer/blob/master/multiplexed-display/multiplexed-display.ino
import math
rom_size = 2048  # However big your EEPROM is

data = [0] * rom_size   # Preallocate the data, all zeros

# Bit patterns for the digits 0..9
digits = [0x7e, 0x30, 0x6d, 0x79, 0x33, 0x5b, 0x5f, 0x70, 0x7f, 0x7b]


print("Programming ones place")
for x in range(256):
  data[x] = digits[math.floor(x % 10)]

print("Programming tens place")
for x in range(256):
  data[x+256] = digits[math.floor((x / 10) % 10)]

print("Programming hundreds place")
for x in range(256):
  data[x+512] =  digits[math.floor((x / 100) % 10)]
  
print("Programming sign")
for x in range(256):
  data[x+768] = 0

print("Programming ones place (twos complement)")
for x in range (-128,128):
  twos_comp = x.to_bytes( 1 , byteorder='big' , signed=True )[0]
  data[twos_comp + 1024] = digits[math.floor(abs(x) % 10)]

print("Programming tens place (twos complement)")
for x in range (-128,128):
  twos_comp = x.to_bytes( 1 , byteorder='big' , signed=True )[0]
  data[twos_comp + 1280] = digits[math.floor(abs(x / 10) % 10)]

print("Programming hundreds place (twos complement)")
for x in range (-128,128):
  twos_comp = x.to_bytes( 1 , byteorder='big' , signed=True )[0]
  data[twos_comp + 1536] = digits[math.floor(abs(x / 100) % 10)]

print("Programming sign (twos complement)")
for x in range (-128,128):
  twos_comp = x.to_bytes( 1 , byteorder='big' , signed=True )[0]
  if (x < 0):
    data[twos_comp + 1792] = 0x01
  else:
    data[twos_comp + 1792] = 0

# Convert the data array to binary bytes and write it to a file
with open("7 segment display eeprom.bin", "wb") as f:
    f.write(bytes(data))
    f.close()