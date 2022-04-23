# First Iteration of Chat will be terminal then windowed
import socket
import struct
from datetime import datetime
import B64B64Rotcipher as bbr
import B64B64RotcipherDECODE as bbrd
from threading import Thread

# Server's IP Address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002 # Port we want to use
separator_token = "<SEP>"

roomkey = str(input("roomkey\n\n- "))

# initialize list/set of all connected client's sockets
client_sockets = set()
# create a TCP socket
s = socket.socket()
# make the port as reusable port
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind the socket to the address we specified
s.bind((SERVER_HOST, SERVER_PORT))
# listen for upcoming connections
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

def recvall(sock, n):
	data = bytearray()
	while len(data) < n:
		packet = sock.recv(n-len(data))
		if not packet:
			return None
		data.extend(packet)
	return data

def listen_for_client(cs):
	"""
	This function keep listening for a message from `cs` socket
	Whenever a message is received, broadcast it to all other connected clients
	"""
	while True:
		try:
			# keep listening for a message from `cs` socket
			raw_msglen = recvall(cs, 4)
			if not raw_msglen:
				raise Exception("NO DATA")
			msglen = struct.unpack('>I', raw_msglen)[0]
			msg = recvall(cs, msglen).decode()
		except Exception as e:
			# client no longer connected
			# remove it from the set
			print(f"[!] Error: Client No Longer Connected")
			with open("Log.log", 'a') as file:
				file.write(str("["+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"] | "+str(e)+"\n"))
				file.close()
			client_sockets.remove(cs)
		else:
			#print(msg) #DEBUG
			#print("\n"+str(type(msg))) #DEBUG
			msg = bbrd.decode(msg, roomkey, 2).decode()
			# if we received a message, replace the <SEP>
			# token with ": " for nice printing
			msg = bbr.btwc(msg.replace(separator_token, ": "),roomkey,2)
		# iterate over all connected sockets
		for client_socket in client_sockets:
			# and send the message
			msg = struct.pack('>I', len(msg)) + msg
			client_socket.sendall(msg)

while True:
	# we keep listening for new connections all the time
	client_socket, client_address = s.accept()
	print(f"[+] {client_address} connected.")
	rk = bbrd.decode(client_socket.recv(1024).decode(), None, 2).decode()
	if rk != roomkey:
		client_socket.send(bbr.btwc("WrongKey".encode(), None, 2))
		client_socket.close()
		continue
	if rk == roomkey:
		client_socket.send(bbr.btwc("Welcome".encode(), None, 2))
	# add the new connected client to connected sockets
	client_sockets.add(client_socket)
	# start a new thread that listens for each client's messages
	t = Thread(target=listen_for_client,args=(client_socket,))
	# make the thread daemon so it ends whenever the main thread ends
	t.daemon = True
	# start the thread
	t.start()

# close client sockets
for cs in client_sockets:
	cs.close()
# close server socket
s.close()