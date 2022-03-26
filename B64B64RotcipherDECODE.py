# Change the built-in hash funciton for hashlib's md5 or sha function

from base64 import *
import easygui
import hashlib

def decode(msg, key):
    # take input and key decode using my custom cipher then decode twice using b64
    msg = b64decode(bytes(msg, "UTF-8")).decode()
    #print(msg) # DEBUG
    msg = msg.split("39bgen")
    #print(msg) # DEBUG
    for i in range(len(msg)):
        msg[i] = b85decode(bytes(msg[i], "UTF-8")).decode()

    #print(msg) # DEBUG
    key = b64encode(bytes(str(hashlib.sha256(key.encode()).hexdigest()), "UTF-8")).decode()

    #print(msg)

    InList = list(msg)
    KyList = list(key)

    #print(InList)
    #print(KyList)
    
    counter = -1
    
    try:
        for i in range(len(InList)):
            counter += 1
            if counter > len(KyList)-1:
                counter = counter - len(KyList)-1
            #print(InList[i])   
            InList[i] = chr(int(int(InList[i])/ord(KyList[counter])))
            #print(InList[i])

    except Exception as e:
        print(e)
        print("Custom Cipher Decode Failed (Exit code 1)")
        
    #print(InList)
    tmp = ''
    for i in InList:
        tmp = tmp + i
    output = b64decode(b64decode(bytes(tmp, "UTF-8"))).decode()
    return output

    

#msg = easygui.enterbox("Message")
#key = easygui.enterbox("Key")

#msg = "STUwNlYzOWJnZW5HYyt8WTM5Ymdlbkk1e3ZkMzliZ2VuRyZNM2IzOWJnZW5II2F2bzM5YmdlbkgjYWptMzliZ2VuSFp3VWszOWJnZW5IIXdDYjM5YmdlbkhadzlYMzliZ2VuSDkwbWszOWJnZW5HY3pfWTM5YmdlbkhaP2Ru" # test case
#key = "testing" # test case
#decode(msg, key)
#easygui.msgbox(decode(msg, key))
