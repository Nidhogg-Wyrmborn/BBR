# Change the built-in hash funciton for hashlib's md5 or sha function
from base64 import *
import easygui
import hashlib

def Cstm(Input, Key):
    # change the Input and Key to string rather than bytes
    Input = str(Input)
    Key = str(Key)
    Input = Input.replace("b'", '')
    Input = Input.replace("'", '')
    Key = Key.replace("b'", '')
    Key = Key.replace("'", '')
    
    # Using multiplication, Multiply the ord of the input with the ord of the key
    InList = list(Input)
    KyList = list(Key)

    #print(InList) # DEBUG
    #print(KyList) # DEBUG
    
    #print(len(KyList)) # DEBUG
    # cycle through the input and key and separte them into separate lists
    #for i in Input:
    #    InList.append(i)

    #for i in Key:
    #    KyList.append(i)
    counter = -1
    #print(InList) # DEBUG
    #print(KyList) # DEBUG
    # then try to cycle through the inputt list (InList) and apply the multiplication to it if the key reaches the end of it's limit then cycle back to beginning (VERY INSECURE)
    try:
        for i in range(len(InList)):
            counter += 1
            #print(i) # DEBUG
            #print(InList[i]) # DEBUG
            #print(len(InList)) # DEBUG
            if counter > len(KyList)-1:
                counter = counter - len(KyList)-1
            #print(len(KyList)) # DEBUG
            #print(counter) # DEBUG
            #print(str(ord(InList[i])*ord(KyList[counter]))) # DEBUG
            InList[i] = b85encode(bytes(str(ord(InList[i])*ord(KyList[counter])), "UTF-8"))
            InList[i] = InList[i].decode()
            #print(InList[i]) # DEBUG
            #print(type(InList[i])) # DEBUG
            #InList[i] = InList[i].replace("b'", '')
            #InList[i] = InList[i].replace("'", '')
            #print(InList[i]) # DEBUG
            if i > 0:
                InList[i] = "39bgen" + InList[i]

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

    # create the op string (OutPut)
    op = ''
    for i in InList:
        #print(i) # DEBUG
        op = op + str(i)

    op = b64encode(bytes(op, "UTF-8"))

    # convert bytes-like object to pure string no b'asofoiasjfoawejf' stuff
    output = str(op)
    output = output.replace("b'", '')
    output = output.replace("'", '')

    return output


def btwc(Input, key):
    # convert input to bytes-like object
    Input = bytes(Input, "UTF-8")

    # encode the input with base 64 twice
    I2 = b64encode(Input)
    GfCstm = b64encode(I2)

    # convert the key to hash then base64
    Key = b64encode(bytes(str(hashlib.sha256(key.encode()).hexdigest()), "UTF-8"))

    # return the completed encryption using my custom encryption method
    return Cstm(GfCstm, Key)





















