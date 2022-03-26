import easygui
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

if __name__ == '__main__':
	main()
