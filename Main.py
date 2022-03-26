import easygui
import argparse
import os
import sys
import B64B64Rotcipher as bbr
import B64B64RotcipherDECODE as bbrd

def main():
	while True:
		c = easygui.buttonbox("Encrypt or Decrypt", choices = ["Encrypt", "Decrypt", "Quit"])
		if c == "Encrypt":
			easygui.msgbox(bbr.btwc(easygui.enterbox("Message"), easygui.passwordbox("Key")))
		if c == "Decrypt":
			easygui.msgbox(bbrd.decode(easygui.enterbox("Encrypted Message"), easygui.passwordbox("Key")))
		if c == "Quit":
			break

def main2(msg, key, Encrypt=True):
	if Encrypt:
		return(bbr.btwc(msg, key))
	if not Encrypt:
		return(bbrd.decode(msg, key))

if __name__ == '__main__':
	my_parser = argparse.ArgumentParser(description="Encrypt or decrypt some text according to a key")

	key = ''
	msg = ''

	# add the arguments
	my_parser.add_argument("msg",
							metavar='Message',
							type=str,
							action='store',
							help='the message to encrypt (if there is spaces use quotes)')
	my_parser.add_argument("key",
							metavar="Key",
							type=str,
							action='store',
							help='the key to encrypt the message (if there is spaces use quotes)')
	args = my_parser.parse_args()

	key = args.key
	msg = args.msg

	isencs = str(input("Is it [e]ncrypt or [d]ecrypt?\n\n- "))

	if isencs.lower() == 'e':
		isenc = True
	if isencs.lower() == 'd':
		isenc = False
	if isencs.lower() != 'e' and isencs.lower() != 'd':
		quit()


	print(main2(msg, key, isenc))