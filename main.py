from tkinter import *
import os
#import ctypes   #<-----------lib that enable high DPI, to result smoother graphics
import pathlib
import customtkinter as ctk
from customtkinter import *


#ctypes.windll.shcore.SetProcessDpiAwarness(True)            #increase dots per inch for sharper look

#root cfg
root = Tk()
root.title="Pseudo Commander"
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(1, weight=1)


def pathChange(*event):
    
    directory = os.listdir(currentPath.get())   #Get all files in the current dir
    list.delete(0, END)                         #clear the list... then insert

    for file in directory:
        list.insert(0, file)


def changePathByClicking(event=None):

    picked = list.get(list.curselection()[0])       #Get clicked item

    path = os.path.join(currentPath.get(), picked)  #get full path

    if os.path.isfile(path):                        #if file -> open
        
        print("Opening: " + path)
        os.startfile(path)
    
    else:                                           #if dir -> proceed further and change new path
        
        currentPath.set(path)


def goBack(event=None):

    newPath = pathlib.Path(currentPath.get()).parent #get new path and the change it
    currentPath.set(newPath)
    print("going up")


def open_popup():

    global top

    top = Toplevel(root)

    top.geometry('250x150')
    top.resizable(False, False)
    top.title('child window')
    top.columnconfigure(0,weight=1)
    
    Label(top, text='Enter File or Folder name').grid()
    Entry(top, textvariable=newFileName).grid(column=0, pady=10, sticky='NSEW')
    Button(top, text="Create", command=newFileOrFolder).grid(pady=10, sticky='NSEW')

def newFileOrFolder():

    if len(newFileName.get().split('.')) !=1:                                           #check if file/dir
        open(os.path.join(currentPath.get(), newFileName.get()), 'w').close()
    
    else:
        os.mkdir(os.path.join(currentPath.get(), newFileName.get))

    top.destroy()
    pathChange()

top = ''

#string variables

newFileName = StringVar(root, "File.dot", 'new_name')
currentPath = StringVar(

    root,
    name='currentPath',
    value=pathlib.Path.cwd()

)

currentPath.trace('w', pathChange)              #bind changes in this var for pathChange func.

Button(root, text='Folder Up', command=goBack).grid(sticky='NSEW', column=0, row=0)

#root.bind("<Alt+Up>", goBack)                   #key-shortcut for goBack

Entry(root, textvariable=currentPath).grid(sticky='NSEW', column=1, row=0, ipadx=10, ipady=10)

list = Listbox(root)
list.grid(sticky="NSEW", column=1, row=1, ipadx=10, ipady=10)

list.bind('<Double-1>', changePathByClicking)
list.bind('<Return>', changePathByClicking)


#Menu


menubar= Menu(root)
menubar.add_command(label="Add File or Folder", command=open_popup)
menubar.add_command(label='Quit', command=root.quit)
root.config(menu=menubar)

pathChange('')

root.mainloop()
