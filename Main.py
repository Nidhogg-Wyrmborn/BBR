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

	# add the arguments
	requiredName = my_parser.add_argument_group("Required Named Arguements")
	requiredName.add_argument("-m", "--message",
							metavar='Message',
							type=str,
							action='store',
							dest='msg',
							required=True,
							help='the message to encrypt (if there is spaces use quotes)')
	my_parser.add_argument("-k", "--key",
							metavar="Key",
							type=str,
							nargs="?",
							action='store',
							dest='key',
							help='the key to encrypt the message (if there is spaces use quotes)')
	my_parser.add_argument("-d", "--decrypt",
							#metavar="Encrypt",
							#type=str,
							#nargs="?",
							action='store_false',
							dest='isencs',
							help='Decrypt otherwise encrypt (if not called)')
	args = my_parser.parse_args()

	msg = args.msg
	key = args.key
	isencs = args.isencs

	if msg == None:
		quit()


	print(main2(msg, key, isencs))