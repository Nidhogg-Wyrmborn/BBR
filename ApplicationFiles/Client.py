import socket
import B64B64Rotcipher as bbr
import B64B64RotcipherDECODE as bbrd
from threading import Thread
from datetime import datetime

# server's IP address
# if the server is not on this machine,
# put the private (network) IP address (e.g 192.168.1.2)
SERVER_HOST = str(input("Server's IP:\n\n- "))
SERVER_PORT = 5002
separator_token = "<SEP>"

s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
# connect to the server
s.connect((SERVER_HOST,SERVER_PORT))
print("[+] Connected.")

# prompt the client for a name
name = input("Enter your name: ")

def listen_for_messages():
	while True:
		message = bbrd.decode(s.recv(1024).decode(), roomkey, 2)
		print("\n" + message)

# make a thread that listens for messages to this client & print them
t = Thread(target=listen_for_messages)
# make the thread daemon so it ends whenever the main thread ends
t.daemon = True
# start the thread
t.start()

while True:
	# input message we want to send to the server
	to_send = input()
	# a way to exit the program
	if to_send.lower() == 'q':
		break
	# add the datetime & name
	date_now = datetime.now().strftime('%Y-%m-%d %H"%M:%S')
	to_send = bbr.btwc(f"[{date_now}] {name}{separator_token}{to_send}", roomkey, 2)
	# finally, send the message
	s.send(to_send.encode())

# close the socket
s.close()