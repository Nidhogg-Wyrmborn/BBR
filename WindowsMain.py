#!/usr/bin/env python3
import B64B64RotcipherDECODE as bbrd
import B64B64Rotcipher as bbr
import tarfile
import os
import sys
from tqdm import tqdm
from tkinter import *
from tkinter.ttk import *
import easygui

class tkProgressbar():
    def __init__(self, total=int, Title=str, Orientation=HORIZONTAL, Determinate=False):
        self.total = total
        self.p2jmp = total/100
        self.tdone = float(0)
        self.nctdn = 0
        self.isDet = Determinate
        self.root = Tk()
        self.root.title(Title)
        self.root.geometry('400x250+1000+300')
        if not self.isDet:
            self.pb1 = Progressbar(self.root, orient=Orientation, length=100, mode='indeterminate')
        if self.isDet:
            self.pb1 = Progressbar(self.root, orient=Orientation, length=100, mode='determinate')
        self.pb1.pack(expand=True)
        

    def update(self, amount):
        self.tdone += amount
        self.nctdn += amount
        while self.tdone >= self.p2jmp:
            if self.tdone >= self.p2jmp*2:
                self.tdone -= self.p2jmp*2
                self.pb1['value'] += 2
                continue
            self.tdone -= self.p2jmp
            self.pb1['value'] += 1
        if self.nctdn >= self.total:
            self.root.destroy()
        
        

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
    compress(tar_file,members)


def compress(tar_file, members):
    """
    Adds files (`members`) to a tar_file and compresses it
    """
    # open file for gzip compressed writing
    tar = tarfile.open(tar_file, mode="w:gz")
    # with progress bar
    # set the progress bar
    progress = tkProgressbar(len(members), "Compressing", Determinate=True)
    for member in members:
        # add file/folder/link to the tar file (Compress)
        tar.add(member)
        # set the progress description of the progress bar to the file being compressed
        progress.update(1)
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

def encrypt(msg, key):
    return bbr.btwc(msg, key)

def decrypt(msg, key):
    return bbrd.decode(msg, key)

def efile(fpath, spath, key):
    try:
        print(fpath)
        if len(fpath)==1:
            fpath = fpath[0]
            compressed = False
        elif len(fpath)>1:
            compresstree("CompressedTree.tar.gz", fpath)
            fpath = "CompressedTree.tar.gz"
            compressed = True
        with open(fpath, 'rb') as file:
            fl = file.readlines()

        fs = b''.join(fl)

        if compressed:
            print(spath)
            if spath.endswith('.bbr'):
                spath = spath.replace(".bbr", '')
            with open(spath+".tar.gz.bbr", 'wb') as file:
                file.write(bbr.btwc(fs, key, True))
        elif not compressed:
            if not spath.endswith(".bbr"):
                spath = spath + ".bbr"
            with open(spath, 'wb') as file:
                file.write(bbr.btwc(fs, key, True))
    except KeyboardInterrupt:
        print("User Interrupt")
        print("Removing Temporary files")
        try:
            os.remove("CompressedTree.tar.gz")
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
            shutil.rmtree("CompressedTree")
        except:
            pass

def dfile(fpath, key):
    try:
        pass
    except Exception as e:
        print(e)
        easygui.msgbox(f"Error Decode failed Check below for error details\n\n{e}")

def main():
    running = True
    while running:
        c = easygui.buttonbox("Encrypt Or Decrypt?", choices=['Encrypt','Encrypt File','Decrypt','Decrypt File','Quit'])
        if c == "Quit":
            running = False

        if c == "Encrypt":
            easygui.msgbox(encrypt(easygui.enterbox("Message to encrypt:"),easygui.enterbox("Passcode:")))

        if c == "Encrypt File":
            efile(easygui.fileopenbox(multiple=True), easygui.filesavebox(default='Encrypted.bbr'), easygui.enterbox("Passcode:"))

        if c == "Decrypt":
            easygui.msgbox(decrypt(easygui.enterbox("Message to decrypt:"),easygui.enterbox("Passcode:")))

        if c == "Decrypt File":
            dfile(easygui.fileopenbox(multiple=False),easygui.enterbox("Passcode:"))

if __name__ == '__main__':
    main()
