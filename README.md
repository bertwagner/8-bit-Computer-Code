# 8-bit Computer EEPROM Code

Code to generate lookup tables stored in the 7-segment display and microcode EEPROMs for [Ben Eater's 8-bit computer design](https://www.youtube.com/watch?v=HyznrdDSSGM&list=PLowKtXNTBypGqImE405J2565dvjafglHU&index=1).

Ben's [original source code](https://github.com/beneater/eeprom-programmer) was for a homemade Arduino based EEPROM programmer.  I have a TL866 II Plus EEPROM Programmer, so I rewrote Ben's scripts in Python to generate the .bin files to flash onto the EEPROM directly.