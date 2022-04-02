#!/usr/bin/env python3
import easygui
import argparse
import os
import sys
import shutil
import time
import zipfile
from tqdm import tqdm
import tarfile
import B64B64Rotcipher as bbr
import B64B64RotcipherDECODE as bbrd

exceptions = []

def compress(tar_file, members):
    """
    Adds files (`members`) to a tar_file and compresses it
    """
    # open file for gzip compressed writing
    tar = tarfile.open(tar_file, mode="w:gz")
    # with progress bar
    # set the progress bar
    progress = tqdm(members)
    for member in progress:
        # add file/folder/link to the tar file (Compress)
        tar.add(member)
        # set the progress description of the progress bar to the file being compressed
        progress.set_description(f"Compressing {member}")
    # close the file
    tar.close()

def decompress(tar_file, path, members=None):
    """
    Extracts `tar_file` and puts the `members` to `path`
    If members is None, all members on `tar_file` will be extracted.
    """
    tar = tarfile.open(tar_file, mode="r:gz")
    if members is None:
        members = tar.getmembers()
    # with progress bar
    # set the progress bar
    progress = tqdm(members)
    for member in progress:
        tar.extract(member, path=path)
        # set the progress description of the progress bar
        progress.set_description(f"Extracting {member.name}")
    # or use this
    # tar.extractall(members=members, path=path)
    # close the file
    tar.close()

#def main():
#    while True:
#            c = easygui.buttonbox("Encrypt or Decrypt", choices = ["Encrypt", "Decrypt", "Quit"])
#           if c == "Encrypt":
#               easygui.msgbox(bbr.btwc(easygui.enterbox("Message"), easygui.passwordbox("Key")))
#            if c == "Decrypt":
#               easygui.msgbox(bbrd.decode(easygui.enterbox("Encrypted Message"), easygui.passwordbox("Key")))
#            if c == "Quit":
#               break

def main(msg, key, Encrypt, isfile, iswindow=False, ismultiple=False):
    iscompressed = False
    isall = False
    if "*" in msg or type(msg) == type(list):
        ismultiple = True
    if Encrypt:
        if not isfile:
            return(bbr.btwc(msg, key).decode())
        if isfile:
            try:
                if ismultiple:
                    if not iswindow:
                        filename = str(input('Filename to save as: '))
                    if iswindow:
                        finalfilename = easygui.filesavebox()
                        filename = finalfilename.split('/')[-1]
                        print(filename)
                    isall = True
                    l = list()
                    if msg == "*" and type(msg)==type(''):
                        for r, d, f in os.walk("./"):
                            for file in f:
                                l.append(os.path.join(r, file))
                    elif msg != "*" and type(msg)==type(''):
                        msg = msg.replace("*", '')
                        #print(msg)
                        for r, d, f in os.walk(msg):
                            for file in f:
                                l.append(os.path.join(r, file))
                    os.makedirs(f"{filename}")
                    if len(l)==0:
                        l = msg
                    for i in l:
                        with open(i, 'rb') as file:
                            fl = file.readlines()
                            flb = b''.join(fl)
                            file.close()

                        while i.startswith("../"):
                            il = i.split("/")
                            il.pop(0)
                            i = '/'.join(il)
                        #print(i)

                        if i.startswith("./"):
                            il = i.split("/")
                            il.pop(0)
                            i = ''
                            for f in il:
                                i = i + f
                        #print(i)

                        while "\\" in i:
                            i = i.replace("\\", "/")
                        
                        im = ''

                        a = i.split("/")
                        #print(a, type(a))
                        if type(a) == type(['','']):
                            i = a[-1]
                            a = a[:-1]
                            im = '/'.join(a)
                        #print(im)
                        
                        if im != '':
                            try:
                                os.makedirs(f"./{filename}/{im}")
                            except Exception as e:
                                exceptions.append(e)
                                pass
                            with open(f"./{filename}/{im}/"+i, 'wb') as file:
                                    file.write(flb)
                        if im == '':
                            with open(f"./{filename}/"+i, 'wb') as file:
                                file.write(flb)


                    for i in range(len(l)):
                        l[i] = f"./{filename}/"+l[i].split("/")[len(l[i].split("/"))-1]
                    
                    #print(l)
                    l=list()
                    for r, d, f in os.walk(f"./{filename}/"):
                        for file in f:
                            l.append(os.path.join(r, file))
                    compress(f"{filename}.tar.gz", l)
                    shutil.rmtree(f"{filename}")
                    msg = f"{filename}.tar.gz"

                with open(msg, 'rb') as file:
                    rl = file.readlines()
                    file.close()
                
                rs = b''.join(rl)

                with open(msg+".bbr", 'wb') as file:
                    file.write(bbr.btwc(rs, key))
                    file.close()
                if isall:
                    os.remove(f"./{msg}")
                    #pass # DEBUG
                
                return f"encrypted file is {msg}.bbr"

            except KeyboardInterrupt as e:
                print("User Interrupted")
                print("Removing Temporary Folders/Files...")
                try:
                    shutil.rmtree(f"{filename}")
                except:
                    pass
                try:
                    os.remove(f"{filename}.tar.gz.bbr")
                except:
                    pass
                try:
                    os.remove(f"{filename}.tar.gz")
                except:
                    pass
                try:
                    os.remove(f"{msg}.bbr")
                except:
                    pass


    if not Encrypt:
        if not isfile:
            return(bbrd.decode(msg, key).decode())
        if isfile:
            if msg.endswith(".tar.gz.bbr"):
                iscompressed = True
            with open(msg, 'rb') as file:
                rl = file.readlines()

            rs = b''.join(rl)
            
            with open(msg.replace(".bbr", ''), 'wb') as file:
                file.write(bbrd.decode(rs, key))

            if iscompressed:
                decompress(msg.replace(".bbr", ''), "./"+msg.replace(".tar.gz.bbr",''))
                os.remove(msg.replace(".bbr",''))
                return f"Decrypted Folder is {msg.replace('.tar.gz.bbr','')}"
            return f"decrypted file is {msg.replace('.bbr','')}"


def mainwindow():
    # using easygui and tkinter create windows to show progress and create a
    # way for users to interact with the program away from the command-line
    #
    # Requirements: Uses either Easygui or Tkinter for the windows
    # adds Progress bars (Use Tkinter for this)
    # adds File Selection (Easygui has something for this)
    # adds file saving (allows the program to save to a location)
    # make sure the user can select multiple files (e.g. *, or just 2 out of 9)
    #
    # Please be familiar with python and feel free to experiment in the IDLE
    # window. If there is an error it's fine find a way to fix it
    running = True
    while running:
        c = easygui.buttonbox("Encrypt or Decrypt", choices = ['Encrypt','Encrypt File','Decrypt','Decrypt File','Quit'])
        if c == "Encrypt":
            easygui.msgbox(main(easygui.enterbox("Message"), easygui.enterbox("Key"), True, False, True))
        if c == "Encrypt File":
            Filename = main(easygui.fileopenbox(multiple=True), easygui.enterbox("Key"), True, True, True, True)
            easygui.msgbox(f"File is saved as {Filename}")
        if c == "Quit":
            running = False


if __name__ == '__main__':
    my_parser = argparse.ArgumentParser(description="Encrypt or decrypt some text according to a key")

    # add the arguments
    requiredName = my_parser.add_argument_group("Required Named Arguements")
    requiredName.add_argument("-m", "--message",
                            metavar='<Message>',
                            type=str,
                            action='store',
                            dest='msg',
                            #required=True,
                            help='the message to encrypt (if there is spaces use quotes)')
    my_parser.add_argument("-k", "--key",
                            metavar="Key",
                            type=str,
                            nargs="?",
                            action='store',
                            dest='key',
                            help='the key to encrypt the message (if there is spaces use quotes)')
    my_parser.add_argument("-d", "--decrypt",
                            #metavar="Encrypt",
                            #type=str,
                            #nargs="?",
                            action='store_false',
                            dest='isencs',
                            help='Decrypt otherwise encrypt (if not called)')
    my_parser.add_argument("-f", "--file",
                            action='store_true',
                            dest='isfile',
                            help='Is not file unless this argument is called, if this argument is called -m must be a filepath')
    args = my_parser.parse_args()

    msg = args.msg
    key = args.key
    isencs = args.isencs
    isfile = args.isfile

    if msg == None:
        mainwindow()
        quit()

    try:
        print(main(msg, key, isencs, isfile))
    except Exception as e:
        print(e)
        print("\n\n",exceptions, "Have occured")

