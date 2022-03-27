import easygui
import argparse
import os
import sys
import zipfile
from tqdm import tqdm
import tarfile
import B64B64Rotcipher as bbr
import B64B64RotcipherDECODE as bbrd

def compress(tar_file, members):
	"""
	Adds files (`members`) to a tar_file and compresses it
	"""
	# open file for gzip compressed writing
	tar = tarfile.open(tar_file, mode="w:gz")
	# with progress bar
	# set the progress bar
	progress = tqdm(members)
	for member in progress:
		# add file/folder/link to the tar file (Compress)
		tar.add(member)
		# set the progress description of the progress bar
		progress.set_description(f"Compressing {member}")
	# close the file
	tar.close()

def decompress(tar_file, path, members=None):
	"""
	Extracts `tar_file` and puts the `members` to `path`
	If members is None, all members on `tar_file` will be extracted.
	"""
	tar = tarfile.open(tar_file, mode="r:gz")
	if members is None:
		members = tar.getmembers()
	# with progress bar
	# set the progress bar
	progress = tqdm(members)
	for member in progress:
		tar.extract(member, path=path)
		# set the progress description of the progress bar
		progress.set_description(f"Extracting {member.name}")
	# or use this
	# tar.extractall(members=members, path=path)
	# close the file
	tar.close()

#def main():
#	while True:
#		c = easygui.buttonbox("Encrypt or Decrypt", choices = ["Encrypt", "Decrypt", "Quit"])
#		if c == "Encrypt":
#			easygui.msgbox(bbr.btwc(easygui.enterbox("Message"), easygui.passwordbox("Key")))
#		if c == "Decrypt":
#			easygui.msgbox(bbrd.decode(easygui.enterbox("Encrypted Message"), easygui.passwordbox("Key")))
#		if c == "Quit":
#			break

def main(msg, key, Encrypt, isfile):
	if Encrypt:
		if not isfile:
			return(bbr.btwc(msg, key))
		if isfile:
			with open(msg, 'r', encoding='latin1') as file:
				rl = file.readlines()
			
			with tqdm(rl, position=0, leave=True) as pbar:
				rs = ''
				for i in rl:
					rs = rs + i

			with open(msg+".bbr", 'w', encoding='latin1') as file:
				file.write(bbr.btwc(rs, key))

			return f"encrypted file is {msg}.bbr"

	if not Encrypt:
		if not isfile:
			return(bbrd.decode(msg, key))
		if isfile:
			with open(msg, 'r', encoding='latin1') as file:
				rl = file.readlines()

			rs = ''
			for i in rl:
				rs = rs + i

			with open(msg.replace(".bbr", ''), 'w', encoding='latin1') as file:
				file.write(bbrd.decode(rs, key))
			return f"decrypted file is {msg.replace('.bbr','')}"

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
	my_parser.add_argument("-f", "--file",
							action='store_true',
							dest='isfile',
							help='Is not file unless this argument is called, if this argument is called -m must be a filepath')
	args = my_parser.parse_args()

	msg = args.msg
	key = args.key
	isencs = args.isencs
	isfile = args.isfile

	if msg == None:
		quit()


	print(main(msg, key, isencs, isfile))