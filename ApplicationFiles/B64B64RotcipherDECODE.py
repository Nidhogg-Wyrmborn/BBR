# Change the built-in hash funciton for hashlib's md5 or sha function

from base64 import *
import easygui
import hashlib
from tkinter import *
import tkPBar as tpb
from tqdm import tqdm
    
def decode(msg, key, windowed=0):
    if type(msg)!=type(b''):
        msg = bytes(msg, "UTF-8")

    if key == None:
        key = ''
    
    # take input and key decode using my custom cipher then decode twice using b64
    msg = b64decode(msg).decode()
    msg = msg.split("39bgen")
    if windowed==0:
        pbar = tqdm(total=len(msg), position=0, leave=True)
    if windowed==1:
        pbar = tpb.tkProgressbar(total=len(msg),Title="Decoding",Determinate=True)
    for i in range(len(msg)):
        if windowed==1:
            pbar.description(f"{i}/{len(msg)}")
        msg[i] = b85decode(bytes(msg[i], "UTF-8")).decode()
        if windowed==1:
            pbar.update(1)
            if pbar.cancel:
                raise Exception("User Canceled")
        if windowed==0:
            pbar.update()

    key = b64encode(bytes(str(hashlib.sha256(key.encode()).hexdigest()), "UTF-8")).decode()

    InList = list(msg)
    KyList = list(key)

    counter = -1

    if windowed==0:
        pbar2 = tqdm(total=len(InList), position=0, leave=True)
    if windowed==1:
        pbar2 = tpb.tkProgressbar(total=len(InList),Title="Decoding",Determinate=True)
    
    try:
        for i in range(len(InList)):
            counter += 1
            if counter > len(KyList)-1:
                counter = counter - len(KyList)-1
            #print(InList[i])   
            InList[i] = chr(int(int(InList[i])/ord(KyList[counter])))
            #print(InList[i])
            if windowed==0:
                pbar2.update()
            if windowed==1:
                pbar2.description(f"{i}/{len(InList)}")
                pbar2.update(1)
                if pbar2.cancel:
                    raise Exception("User Canceled")

    except Exception as e:
        print(e)
        print("Custom Cipher Decode Failed (Exit code 1)")
        
    #print(InList)

    if windowed==1:
        root = Tk()
        root.title("Warning")
        root.geometry('400x250+1000+300')
        def closewin():
            root.destroy()
        def sepwin():
            lab = Label(root)
            lab['text'] = "Finished decoding custom cipher, turning list into string\nbe prepared for delay"
            lab.pack()
            but = Button(root, text='Close this warning', command=closewin)
            but.pack()
        root.after(0, sepwin)
    
    tmp = ''.join(InList)

    try:
        closewin()
    except:
        pass
    #print(type(tmp))
    output = b64decode(b64decode(tmp.encode()))
    return output
