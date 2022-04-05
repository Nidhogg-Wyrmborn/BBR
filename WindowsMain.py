#!/usr/bin/env python3
import B64B64RotcipherDECODE as bbrd
import B64B64Rotcipher as bbr
import tarfile
import os
import sys
from tqdm import tqdm
from tkinter import *
import easygui

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
            with open(spath+".tar.gz.bbr", 'wb') as file:
                file.write(bbr.btwc(fs, key))
        elif not compressed:
            with open(spath, 'wb') as file:
                file.write(bbr.btwc(fs, key))
    except KeyboardInterrupt:
        print("User Interrupt")
        print("Removing Temporary files")

def dfile(fpath, key):
    pass

def main():
    running = True
    while running:
        c = easygui.buttonbox("Encrypt Or Decrypt?", choices=['Encrypt','Encrypt File','Decrypt','Decrypt File','Quit'])
        if c == "Quit":
            running = False

        if c == "Encrypt":
            easygui.msgbox(encrypt(easygui.enterbox("Message to encrypt:"),easygui.enterbox("Passcode:")))

        if c == "Encrypt File":
            efile(easygui.fileopenbox(multiple=True), easygui.filesavebox(), easygui.enterbox("Passcode:"))

        if c == "Decrypt":
            easygui.msgbox(decrypt(easygui.enterbox("Message to decrypt:"),easygui.enterbox("Passcode:")))

        if c == "Decrypt File":
            dfile(easygui.fileopenbox(multiple=False),easygui.enterbox("Passcode:"))

if __name__ == '__main__':
    main()
