# Change the built-in hash funciton for hashlib's md5 or sha function
from base64 import *
import easygui
import hashlib
from tqdm import tqdm
import threading, queue

def Cstm(Input, Key, windowed):
    # change the Input and Key to string rather than bytes
    Input = Input.decode()
    Key = Key.decode()
    
    # Using multiplication, Multiply the ord of the input with the ord of the key
    InList = list(Input)
    KyList = list(Key)

    if not windowed:
        print("[**] beginning custom cipher")

    counter = -1
    #cycle = 0
    #cyclewhole = 0
    if not windowed:
        total = len(InList)
        pbar = tqdm(total=total, position=0, leave=True)
    if windowed:
        pass
    # then try to cycle through the inputt list (InList) and apply the multiplication to it if the key reaches the end of it's limit then cycle back to beginning (VERY INSECURE)
    try:
        for i in range(len(InList)):
            counter += 1

            if counter > len(KyList)-1:
                counter = counter - len(KyList)-1
            
            #if i % 89457:
            #cycle += 1
            #if cycle > 499999:
            #    cyclewhole = cyclewhole + cycle
            #    cycle = 0
            #    print(f"[**] Cycle: {cyclewhole}")

            InList[i] = b85encode(bytes(str(ord(InList[i])*ord(KyList[counter])), "UTF-8"))
            InList[i] = InList[i].decode()

            if i > 0:
                InList[i] = "39bgen" + InList[i]
            pbar.update()

    except Exception as e:
        # if there is an exception print it and then print "exit code 1 (Custom Encryption Failed)
        print(e)
        print(f"\nInList = {InList}\nKyList = {KyList}")
        print()
        print(f"Input = {Input}\nKey = {Key}")
        print()
        print(f"was up to {i}, counter was up to {counter}")
        print("\nexit code 1 (Custom Encryption Failed")
        # then return a None-type object
        return None

    print("[**] Finished custom cipher, turning list into string...")

    op = ''.join(InList)
    
    print("[**] beginning final encoding")

    op = b64encode(op.encode())

    # convert bytes-like object to pure string no b'asofoiasjfoawejf' stuff
    print("[**] Finished")
    return op


def btwc(Input, key, windowed=False):
    if type(Input)!=type(b''):
        # convert input to bytes-like object
        Input = Input.encode()

    # encode the input with base 64 twice
    I2 = b64encode(Input)
    GfCstm = b64encode(I2)

    if key == None:
        key = ''

    # convert the key to hash then base64
    Key = b64encode(bytes(str(hashlib.sha256(key.encode()).hexdigest()), "UTF-8"))
    if not windowed:
        print("[**] Step 1: Complete")
    # return the completed encryption using my custom encryption method
    return Cstm(GfCstm, Key, windowed)





















