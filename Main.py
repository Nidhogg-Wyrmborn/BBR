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
		pass

if __name__ == '__main__':
	my_parser = argparse.ArgumentParser(description="Encrypt or decrypt some text according to a key")

	# add the arguments
	my_parser.add_argument("msg",
							metavar='Must supply a message to encrypt',
							type=bool,
							help='the message to encrypt')
	my_parser.add_argument("key",
							metavar="Must supply a key for encryption for better security",
							type=str,
							help='the key to encrypt the message')
	args = my_parser.parse_args()

	key = args.key
	msg = args.msg

	isencs = str(input("Is it [e]ncrypt or [d]ecrypt?\n\n- "))

	if isencs.lower() == 'e':
		isenc = True
	if isencs.lower() == 'd':
		isenc = False
	if isencs.lower() != 'e' or 'd':
		quit()


	main2(msg, key, isenc)