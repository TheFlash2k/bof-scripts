#!/usr/bin/env python3 

'''
I do know that i can use struct to actually convert the address to raw bytes
but i prefer using stuff that i create myself idk ;--;

If you don't know about how to do that using struct (you can also use pwntools and p32 function)

import struct
struct.pack('<I', 0x123123)
# '<I' here represents the little endian format
'''

from sys import argv

def usage():
	print(f"Usage: {argv[0]} <address>\nExample: {argv[0]} 0x12312323")
	exit()

try:
	addr = argv[1]
except:
	print(f"[-] No Address Provided! Provide an address.")
	usage()

if "0x" == addr[:2]:
	addr = addr.replace('0x', '')

addr = addr[::-1]

f_addr = list()

try:
	for i in range(0, len(addr), 2):
		curr_addr = addr[i + 1]
		curr_addr += addr[i]
		curr_addr = r'\x' + curr_addr
		f_addr.append(curr_addr)
except IndexError:
	print("[-] Invalid Address Provided!")
	usage()
	
f_addr = ''.join(f_addr)
print(f_addr)
