import tkinter as tk
from datetime import datetime
from threading import Thread, Lock
recvd = None

lock = Lock()

class chatroom():
	def __init__(self):
		global to_send, message
		self.to_send = None
		self.recvd = None
		self.txtval = []
		self.nochngtxtval = []
		self.frame = tk.Tk()
		def update():
			global recvd
			if recvd == None:
				#print(f"is none {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
			if recvd != None:
				#print(f"not none {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
				self.recvd = recvd
				recvd = None
			self.frame.after(10,update)
		update()
		self.frame.title("Chatroom")
		self.frame.geometry("400x200")
		self.lbl = tk.Label(self.frame, text = "", justify=tk.LEFT, anchor='nw', width=45, relief=tk.RIDGE, height=8)
		self.lbl.pack()
		self.inputtxt = tk.Text(self.frame,height=1,width=40,undo=True)
		self.inputtxt.bind("<Return>", self.sendInput)
		self.sendButton = tk.Button(self.frame, text="Send")
		self.sendButton.bind("<Button-1>", self.sendInput)
		self.sendButton.pack(padx=5,pady=5,side=tk.BOTTOM)
		self.inputtxt.pack(padx=5,pady=5,side=tk.BOTTOM)
		self.updateChat(self.recvd)
		self.frame.mainloop()

	def sendInput(self, event):
		global to_send, message
		inp = self.inputtxt.get("1.0", "end").strip()
		self.to_send = inp
		to_send = inp
		self.inputtxt.delete('1.0', "end")

	def updateChat(self,new):
		if new==None:
			#print('e')
			self.frame.after(10, lambda: self.updateChat(self.recvd))
			return
		n = 45
		if len(new)>n:
			newl = [new[i:i+n] for i in range(0, len(new), n)]
			counter = 0
			for i in range(len(newl)):
				newl.insert(i+counter, '\n')
				counter+=1
			newl.pop(0)
			new = ''
			for i in newl:
				new = new + i
		self.lbl['text'] = ''
		self.txtval = []
		self.nochngtxtval.append(new+"\n")
		for i in range(len(self.nochngtxtval)):
			self.txtval.append(self.nochngtxtval[i])
		self.txtval.pop(len(self.txtval)-1)
		self.txtval.append(new+"\n")
		self.txtval[len(self.txtval)-1] = self.txtval[len(self.txtval)-1][:-1]
		for i in range(len(self.txtval)):
			self.lbl['text'] = self.lbl['text']+self.txtval[i]
		#print(self.lbl['text']+new)
		self.to_send = None
		self.recvd = None
		self.frame.after(10, lambda: self.updateChat(self.recvd))

def main():
	global recvd
	cr = chatroom()

def setrecvd():
	global recvd
	while True:
		with lock:
			recvd = str(input("set Recvd to: "))

if __name__ == "__main__":
	Thread(target=setrecvd,daemon=True).start()
	main()