#!/usr/bin/env python3

## NOTE: The 32 lines from the ESP dump must be copied and then pasted into the file from the immunity debugger for this script to work.

from sys import argv

# All the 255 hex characters
good_chars = (
	"01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F 10 11 12 13 14 15 "
	"16 17 18 19 1A 1B 1C 1D 1E 1F 20 21 22 23 24 25 26 27 28 29 2A "
	"2B 2C 2D 2E 2F 30 31 32 33 34 35 36 37 38 39 3A 3B 3C 3D 3E 3F "
	"40 41 42 43 44 45 46 47 48 49 4A 4B 4C 4D 4E 4F 50 51 52 53 54 "
	"55 56 57 58 59 5A 5B 5C 5D 5E 5F 60 61 62 63 64 65 66 67 68 69 "
	"6A 6B 6C 6D 6E 6F 70 71 72 73 74 75 76 77 78 79 7A 7B 7C 7D 7E "
	"7F 80 81 82 83 84 85 86 87 88 89 8A 8B 8C 8D 8E 8F 90 91 92 93 "
	"94 95 96 97 98 99 9A 9B 9C 9D 9E 9F A0 A1 A2 A3 A4 A5 A6 A7 A8 "
	"A9 AA AB AC AD AE AF B0 B1 B2 B3 B4 B5 B6 B7 B8 B9 BA BB BC BD "
	"BE BF C0 C1 C2 C3 C4 C5 C6 C7 C8 C9 CA CB CC CD CE CF D0 D1 D2 "
	"D3 D4 D5 D6 D7 D8 D9 DA DB DC DD DE DF E0 E1 E2 E3 E4 E5 E6 E7 "
	"E8 E9 EA EB EC ED EE EF F0 F1 F2 F3 F4 F5 F6 F7 F8 F9 FA FB FC "
	"FD FE FF"
)

def get_int(var):
	return int(var.replace(r'\x', '0x'), 16)

def get_args():
	file_name = ""
	verbose = False
	try:
		file_name = argv[1]
	except:
		print(f"[-] No file name provided!. Usage: {argv[0]} <file_name> [-v|--verbose]")
		exit(1)

	check = None
	try:
		check = argv[2]
	except:
		pass

	if check:
		if check.lower() != '-v' and check.lower() != '--verbose':
			print(f"[-] Invalid argument {check} provided!")
			exit(1)
		else:
			verbose = True

	return file_name, verbose

def get_received_chars():
	rcvd_chars = list()
	try:
		handle = open(file_name)
	except:
		print("[-] Invalid File Name. Please enter a valid file that contains the output from Immunity in order to identify bad chars!")
		exit(1)

	# Reading the data:
	while(True):
		data = handle.readline()
		data = data.split()[1:9]
		if data == []:
			break
		for item in data:
			rcvd_chars.append(item)

	handle.close()
	return rcvd_chars

if __name__ == "__main__":

	file_name, verbose = get_args()
	good_chars = good_chars.split()
	rcvd_chars = get_received_chars()

	i = 0
	err = False
	bad_chars = list()
	for char in good_chars:
		if char != rcvd_chars[i]:
			if verbose:
				print(f"Invalid char found: {rcvd_chars[i]}. Should have been: {char}")
			bad_chars.append(char)
			err = True
		i += 1

	if not err:
		print("[*] No bad chars found! Nullbyte (0x00) maybe a badchar.")

	else:
		for i in range(len(bad_chars)):
			bad_chars[i] = r'\x' + bad_chars[i]
		print(f"[+] Following badchars were found: \\x00,{','.join(bad_chars)}")
		print("[*] NOTE: If you see an incremented badchar (\\x07,\\x08), that would most probably mean that the first one is the badchar and the second one is affected by it somehow.")


		print("[*] Following may be the correct bad chars that were found: ", end = '')
		
		# Removing all the alternate ones: (There may some cleaner method, but idk ;-;)
		last_item = bad_chars[-1]
		i = 0
		while True:
			if last_item == bad_chars[i]:
				break
			if i < (len(bad_chars[i]) - 1):
				curr = get_int(bad_chars[i])
				next = get_int(bad_chars[i + 1])
				if curr + 1 == next:
					bad_chars.pop(i+1)
			i += 1

		# Checking for last one:
		prev = get_int(bad_chars[-2])
		last = get_int(bad_chars[-1])

		if prev + 1 == last:
			bad_chars.pop(-1)

		print(f"\\x00,{','.join(bad_chars)}")
