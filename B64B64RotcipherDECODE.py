# Change the built-in hash funciton for hashlib's md5 or sha function

from base64 import *
import easygui
import hashlib
from tqdm import tqdm
    
def decode(msg, key):
    if type(msg)!=type(b''):
        msg = bytes(msg, "UTF-8")

    if key == None:
        key = ''
    
    # take input and key decode using my custom cipher then decode twice using b64
    msg = b64decode(msg).decode()
    msg = msg.split("39bgen")
    pbar = tqdm(total=len(msg), position=0, leave=True)
    for i in range(len(msg)):
        msg[i] = b85decode(bytes(msg[i], "UTF-8")).decode()
        pbar.update()

    key = b64encode(bytes(str(hashlib.sha256(key.encode()).hexdigest()), "UTF-8")).decode()

    InList = list(msg)
    KyList = list(key)

    counter = -1

    pbar2 = tqdm(total=len(InList), position=0, leave=True)
    
    try:
        for i in range(len(InList)):
            counter += 1
            if counter > len(KyList)-1:
                counter = counter - len(KyList)-1
            #print(InList[i])   
            InList[i] = chr(int(int(InList[i])/ord(KyList[counter])))
            #print(InList[i])
            pbar2.update()

    except Exception as e:
        print(e)
        print("Custom Cipher Decode Failed (Exit code 1)")
        
    #print(InList)
    tmp = ''.join(InList)
    print(type(tmp))
    output = b64decode(b64decode(tmp.encode()))
    return output
