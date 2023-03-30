#!/usr/bin/env python3
import B64B64RotcipherDECODE as bbrd
import B64B64Rotcipher as bbr
import tarfile
import os
import sys
import shutil
import tkPBar as tpb
from threading import Thread
from tqdm import tqdm
from tkinter import *
from tkinter.ttk import *
import easygui
import fingerprint

def compresstree(tar_file, members):
    os.mkdir(f"./{tar_file.replace('.tar.gz','')}")
    for i in range(len(members)):
        members[i] = members[i].replace("\\", "/")
        
    for i in members:
        with open(i, 'rb') as file:
            with open(f"./{tar_file.replace('.tar.gz','')}/{i.split('/')[len(i.split('/'))-1]}", 'wb') as file2write:
                fl = file.readlines()
                fs = b''.join(fl)
                file2write.write(fs)
    for i in range(len(members)):
        members[i] = f"./{tar_file.replace('.tar.gz','')}/{members[i].split('/')[len(members[i].split('/'))-1]}"
    #print(f"{tar_file}--{members}")
    return compress(tar_file,members)


def compress(tar_file, members):
    """
    Adds files (`members`) to a tar_file and compresses it
    """
    # open file for gzip compressed writing
    tar = tarfile.open(tar_file, mode="w:gz")
    # with progress bar
    # set the progress bar
    progress = tpb.tkProgressbar(len(members), "Compressing", Determinate=True)
    #Thread(target=progress.InitializeWindow, args=(), daemon=True).start()
    for member in members:
        progress.description(f"Compressing {member}")
        # add file/folder/link to the tar file (Compress)
        tar.add(member)
        # set the progress description of the progress bar to the file being compressed
        progress.update(1)
        if progress.cancel:
            return False
    # close the file
    tar.close()
    return True

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
    progress = tpb.tkProgressbar(len(members), "Extracting", Determinate=True)
    for member in members:
        progress.description(f"Extracting {member}")
        # extract the files
        tar.extract(member, path=path)
        # set the progress description of the progress bar
        progress.update(1)
        if progress.cancel:
            return False
    # or use this
    # tar.extractall(members=members, path=path)
    # close the file
    tar.close()
    return True

def encrypt(msg, key):
    return bbr.btwc(msg, key)

def decrypt(msg, key):
    return bbrd.decode(msg, key)

def efile(fpath, spath, key, corrupt=False):
    mode = 'rb'
    modew= 'wb'
    if corrupt:
        mode = 'r'
        modew= 'w'
    try:
        print(fpath)
        if len(fpath)==1:
            fpath = fpath[0]
            compressed = False
        elif len(fpath)>1:
            if not compresstree("Files.tar.gz", fpath):
                raise Exception("User Canceled")
            fpath = "Files.tar.gz"
            compressed = True
        with open(fpath, mode) as file:
            fl = file.readlines()
            file.close()

        fs = b''.join(fl)

        if compressed:
            #print(spath)
            if spath.endswith('.tar.gz.bbr'):
                spath = spath.replace(".tar.gz.bbr", '')
            if spath.endswith('.bbr'):
                spath = spath.replace(".bbr", '')
            with open(spath+".tar.gz.bbr", modew) as file:
                b = bbr.btwc(fs, key, True)
                print(b,type(b))
                if type(b)==Exception:
                    raise b
                file.write(b)
                file.close()
            os.remove("Files.tar.gz")
            shutil.rmtree("Files")
            return spath+".tar.gz.bbr"
        elif not compressed:
            if not spath.endswith(".bbr"):
                spath = spath + ".bbr"
            with open(spath, modew) as file:
                b = bbr.btwc(fs, key, True)
                print(b,type(b))
                if type(b)==Exception:
                    raise b
                file.write(b)
                file.close()
            return spath
    except Exception as e:
        print("User Interrupt")
        print("Removing Temporary files")
        try:
            os.remove("Files.tar.gz")
        except:
            pass
        try:
            os.remove(spath+".tar.gz.bbr")
        except:
            pass
        try:
            os.remove(spath)
        except:
            pass
        try:
            shutil.rmtree("Files")
        except:
            pass
        print(e)
        return e
def dfile(fpath, key, corrupt=False):
    mode = 'rb'
    modew = 'wb'
    if corrupt:
        mode = 'r'
        modew = 'w'
    try:
        if fpath.endswith(".tar.gz.bbr"):
            compressed = True
        elif not fpath.endswith(".tar.gz.bbr"):
            compressed = False
        with open(fpath, mode) as file:
            fl = file.readlines()
            file.close()
        fs = b''.join(fl)
        with open(fpath.replace(".bbr",''), modew) as file:
            file.write(bbrd.decode(fs, key, True))
            file.close()
        if compressed:
            decompress(fpath.replace('.bbr',''), f"{fpath.replace('.tar.gz.bbr','')}")
            os.remove(f"{fpath.replace('.bbr','')}")
            return f"Decompressed as {fpath.replace('.bbr','')}"
        elif not compressed:
            return f"Decrypted as {fpath.replace('.bbr','')}"
    except Exception as e:
        try:
            os.remove(fpath.replace('.bbr',''))
        except:
            pass
        try:
            shutil.rmtree(fpath.replace('tar.gz.bbr',''))
        except:
            pass
        print(e)
        easygui.msgbox(f"Error Decode failed Check below for error details\n\n{e}")

def main():
    running = True
    while running:
        c = easygui.buttonbox("Encrypt Or Decrypt?", choices=['Encrypt','Encrypt File','Decrypt','Decrypt File','fingerprint encrypt', 'fingerprint decrypt', 'Quit'])
        if c == "Quit":
            running = False

        if c == "Encrypt":
            a = encrypt(easygui.enterbox("Message to encrypt:"),easygui.enterbox("Passcode:"))
            print(type(a))
            easygui.msgbox(a)

        if c == "Encrypt File":
            easygui.msgbox(efile(easygui.fileopenbox(multiple=True), easygui.filesavebox(default='Encrypted.bbr'), easygui.enterbox("Passcode:")))

        if c == "Decrypt":
            easygui.msgbox(decrypt(easygui.enterbox("Message to decrypt:"),easygui.enterbox("Passcode:")))

        if c == "Decrypt File":
            easygui.msgbox(dfile(easygui.fileopenbox(multiple=False),easygui.enterbox("Passcode:")))

        if c == 'fingerprint encrypt':
            myfp = fingerprint.FingerPrint()
            try:
                myfp.open()
                print("Please touch the fingerprint sensor")
                try:
                    a = myfp.identify()
                except:
                    print("Error, Access denied or incorrect scan")
                    continue
                for i in range(len(a)):
                    a[i] = ''.join(str(a[i]))
                a = ''.join(a)
                file = easygui.fileopenbox(multiple=True)
                if len(file) >= 2:
                    save = file[0]+"tar.gz.bbr"
                elif len(file) < 2:
                    save = file[0]+".bbr"
                easygui.msgbox(efile(file, save, a))
            finally:
                myfp.close()
        if c == 'fingerprint decrypt':
            myfp = fingerprint.FingerPrint()
            try:
                myfp.open()
                print("Please touch the fingerprint sensor")
                try:
                    a = myfp.identify()
                except:
                    print("Error, Access denied or incorrect scan")
                    continue
                for i in range(len(a)):
                    a[i] = ''.join(str(a[i]))
                a = ''.join(a)
                file = easygui.fileopenbox(multiple=False)
                easygui.msgbox(dfile(file,a))
            finally:
                myfp.close()

if __name__ == '__main__':
    main()
