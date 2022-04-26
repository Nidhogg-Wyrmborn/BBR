import socket
import struct
import easygui
import tkinter as tk
import B64B64Rotcipher as bbr
import B64B64RotcipherDECODE as bbrd
from threading import Thread
from datetime import datetime

# events dict {Send:"To_send", Recv:"recv", Disconnect:"Disconnect message", Connect:"Connect message", Error:"Error Message", Fatal Error:"Error Message", Quit:True/False}
# events dictionary will be used as a global variable between the server thread and the gui thread
# if an error occurs then the client will try to continue, if it can't it changes the events from "Error" to "FError" (Fatal Error) and closes the program while printing error logs
# there are going to be 3 threads Main thread, Server thread, and the log thread which will log all errors and save it in a file which will be read and printed on fatal error
# there will also be 2 subthreads under the main thread which will be update chat and send

events = {"connected":False,"send":None, "recv":None, "disconnect":None, "connect":True, "Error":None, "FError":None, "Quit":False}

def recvall(sock, n):
	data = bytearray()
	while len(data) < n:
		packet = sock.recv(n-len(data))
		if not packet:
			return None
		data.extend(packet)
	return data

def logger():
	global events
	while True:
		if events["Error"] != None:
			try:
				with open("Errors.log", 'a') as file:
					file.write(events["Error"])
					file.write()
					file.close()
				events["Error"] = None
			except:
				with open("Errors.log", 'w') as file:
					file.write(events["Error"]+"\n")
					file.close()
		if events["FError"] != None:
			print(f"Fatal Error\n\n{events['FError']}\n\nfile logs:\n")
			with open("Errors.log", 'r') as file:
				logs = ''.join(file.readlines())
				file.close()
			print(logs)
			quit()
		if events["Quit"]:
			quit()

def Server():
	global events
	while True:
		if events["Quit"] == True:
			break
		if events["connect"] == True:
			events["connect"] = False
			# server's IP address
			# if the server is not on this machine, 
			# put the private (network) IP address (e.g 192.168.1.2)
			SERVER_HOST = easygui.enterbox("IP address of server")
			if SERVER_HOST == None:
				events["Quit"] == True
				quit()
			SERVER_PORT = 5002 # server's port
			separator_token = "<SEP>" # we will use this to separate the client name & message

			roomkey = easygui.enterbox("Roomkey")

			# initialize TCP socket
			s = socket.socket()
			print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
			# connect to the server
			s.connect((SERVER_HOST, SERVER_PORT))

			s.send(bbr.btwc(roomkey, None, 2))

			rspns = bbrd.decode(s.recv(1024).decode(), None, 2).decode()

			if rspns == "Welcome":
				print("Continue")
			if rspns != "Welcome":
				print("Halt")
				event["FError"] = "Incorrect Room Key"
				quit()

			print("[+] Connected.")

			# prompt the client for a name
			name = easygui.enterbox("Enter your name: ")

			events["connected"] = True

			def recvmsg(sock, msglen, key):
				message = bbrd.decode(recvall(sock,msglen).decode(),key,2)
				event["recv"] = message

			def listen_for_messages():
				global events
				while True:
					raw_msglen = recvall(s, 4)
					if not raw_msglen:
						raise Exception("NO DATA")
					msglen = struct.unpack('>I', raw_msglen)[0]
					Thread(target=recvmsg,args=(s,msglen,roomkey), daemon=True).start()

			# make a thread that listens for messages to this client & print them
			t = Thread(target=listen_for_messages)
			# make the thread daemon so it ends whenever the main thread ends
			t.daemon = True
			# start the thread
			t.start()

			def sendalldata(to_send, key):
				s.sendall(bbr.btwc(to_send, key, 2))

			while True:
				if events["disconnect"] != None:
					break
				if events["send"] != None:
					# input message we want to send to the server
					to_send = events["send"]
					events["send"] = None
					# a way to exit the program
					if to_send.lower() == 'q':
						break
					# add the datetime, name & the color of the sender
					date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
					to_send = f"[{date_now}] {name}{separator_token}{to_send}"
					# finally, send the message
					to_send = struct.pack('>I', len(to_send)) + to_send.encode()
					Thread(target=sendalldata, args=(to_send,roomkey,), daemon=True).start()

			# close the socket
			s.close()

class GUI():
	def __init__(self):
		global events
		self.txtval = []
		self.nochngtxtval = []
		self.root = tk.Tk()
		self.root.title("Chatroom")
		self.root.geometry("400x200")
		self.labl = tk.Label(self.root, text="", justify=tk.LEFT, anchor='nw', width=45, relief=tk.RIDGE, height=8)
		self.labl.pack()
		count = 1
		while events["connected"] == False:
			if events["Quit"] == True:
				quit()
			if events["FError"] != None:
				quit()
			self.labl["text"] = "Loading"+"."*count
			count += 1
			if count > 3:
				count = 1
		self.labl["text"] = ""
		self.inputtxt = tk.Text(self.root,height=1,width=40)
		#self.inputtxt.bind("<Return>", self.sendinput)
		self.sendButton = tk.Button(self.root, text="Send", command=self.sendinput)
		#self.sendButton.bind("<Button-1>", self.sendinput)
		self.sendButton.pack(padx=5,pady=5,side=tk.BOTTOM)
		self.inputtxt.pack(padx=5,pady=5,side=tk.BOTTOM)

		def on_closing():
			global events
			self.root.destroy()
			events["Quit"] = True
			quit()

		uc = Thread(target=self.updatechat,daemon=True)
		uc.start()

		self.root.protocol("WM_DELETE_WINDOW", on_closing)
		self.root.mainloop()

	def updatechat(self):
		global events
		while True:
			if events["recv"] != None:
				try:
					current = events["recv"]
					events["recv"] = None
					n = 45
					if len(current)>n:
						currentl = [current[i:i+n] for i in range(0, len(current), n)]
						counter = 0
						for i in range(len(currentl)):
							currentl.insert(i+counter, '\n')
							counter += 1
						currentl.pop(0)
						current = ''
						for i in currentl:
							current = current + i
					self.labl['text'] = ''
					self.txtval = []
					self.nochngtxtval.append(new+"\n")
					for i in range(len(nochngtxtval)):
						self.txtval.append(nochngtxtval[i])
					self.txtval.pop(len(self.txtval)-1)
					self.txtval.append(new+"\n")
					self.txtval[len(self.txtval)-1] = self.txtval[len(self.txtval)-1][:-1]
					for i in range(len(self.txtval)):
						self.labl['text'] = self.labl['text']+self.txtval[i]
				except Exception as e:
					events["Error"] = str(e)
					pass

	def sendinput(self):#, event):
		global events
		inp = self.inputtxt.get("1.0", "end").strip()
		events["send"] = inp
		self.inputtxt.delete('1.0', "end")

loggerthread = Thread(target=logger,daemon=True)
loggerthread.start()

serverthread = Thread(target=Server,daemon=True)
serverthread.start()

GUI()
while events["FError"] == None or not events["Quit"]:
	pass