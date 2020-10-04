import os
from tkinter import *
#from tkinter.ttk import *
import tkinter.messagebox
import subprocess

addentry = "C:\\Users\\"

root = Tk()
root.resizable(width=FALSE, height=FALSE)
root.title("EXT")
root.geometry('{}x{}'.format(200, 235))

frame = Frame(root)
frame.pack()

frameend = Frame(root)


def trouble():
    print("TROUBLE :D!")


def inital():
    global addentry
    output = subprocess.check_output("echo %username%", shell=True)

    output = str(output)
    output = output[2:]
    output = output[:-5]

    addentry = str(addentry + output)
    dirinput.delete(0, END)
    dirinput.insert(0, addentry)

    frameend.pack_forget()
    frame.pack()


types = []


def calcu():
    global types
    gobuttons()
    directory1 = dirinput.get()
    checks = []
    types = [txtvar.get(), exevar.get(), pyvar.get(), zipvar.get(), rarvar.get(), pdfvar.get()]
    print(types)
    for n in range(0, 6):
        if types[n] == 1:
            print(n)
            checks.append(n)
            fork(n, directory1)
            continue
        elif types == [0, 0, 0, 0, 0, 0]:
            # tkinter.messagebox.showinfo("Invalid Entry", "Choose an extension!"), print("Entry Failed.")
            for file in os.listdir(directory1):
                print(os.path.join(file))
            break

    print(checks)
    listcheck()


def fork(n, directory1):
    if n == 0:
        for file in os.listdir(directory1):
            if file.endswith(".txt"):
                print(os.path.join(file))
    elif n == 1:
        for file in os.listdir(directory1):
            if file.endswith(".exe"):
                print(os.path.join(file))
    elif n == 2:
        for file in os.listdir(directory1):
            if file.endswith(".py"):
                print(os.path.join(file))
    elif n == 3:
        for file in os.listdir(directory1):
            if file.endswith(".zip"):
                print(os.path.join(file))
    elif n == 4:
        for file in os.listdir(directory1):
            if file.endswith(".rar"):
                print(os.path.join(file))
    elif n == 5:
        for file in os.listdir(directory1):
            if file.endswith(".pdf"):
                print(os.path.join(file))


def desk():
    deskurl = addentry + "\\Desktop\\"
    dirinput.delete(0, END)
    dirinput.insert(0, deskurl)


def down():
    downurl = addentry + "\\Downloads\\"
    dirinput.delete(0, END)
    dirinput.insert(0, downurl)


def docs():
    docsurl = addentry + "\\Documents\\"
    dirinput.delete(0, END)
    dirinput.insert(0, docsurl)


def gobuttons():
    frame.pack_forget()
    frameend.pack()


def reset():
    frame.pack()
    frameend.pack_forget()


def listcheck():
    # global opts
    optsuse = opts
    x = 0
    for y in range(0, 6):
        if types[y] == 0:
            del opts[y - x]
            print(y)
            print(str(optsuse) + " opts")
            x = x + 1
    upopt = optsuse
    update_options(upopt)


def update_options(optsuse):
    choices.set(optsuse[0])

    menu = comboend['menu']
    menu.delete(0, 'end')

    for opt in optsuse:
        menu.add_command(label=opt, command=lambda n=opt: choices.set(opt))


choices = StringVar()

oc = StringVar(root)
oc.set("All")


def comboans(x):
            print(optentry)
            if x == "txt":
                print("txt")
            elif x == "exe":
                print("exe")
            elif x == "py":
                print("py")
            elif x == "zip":
                print("zip")
            elif x == "rar":
                print("rar")
            elif x == "pdf":
                print("pdf")


# Making Widgets
v = StringVar(frame, value=addentry)

labelstart = Label(frame, text="Configure")
dirlabel = Label(frame, text="Directory:")
dirinput = Entry(frame, textvariable=v)

##Checkboxes
txtvar = IntVar()
exevar = IntVar()
pyvar = IntVar()
zipvar = IntVar()
rarvar = IntVar()
pdfvar = IntVar()
subcha = IntVar()

check1 = Checkbutton(frame, text="txt", variable=txtvar)
check2 = Checkbutton(frame, text="exe", variable=exevar)
check3 = Checkbutton(frame, text="py", variable=pyvar)
check4 = Checkbutton(frame, text="zip", variable=zipvar)
check5 = Checkbutton(frame, text="rar", variable=rarvar)
check6 = Checkbutton(frame, text="pdf", variable=pdfvar)
subcheck = Checkbutton(frame, text="Check Sub folders?", variable=subcha)

buttondesk = Button(frame, text="Desk", command=desk)
buttondown = Button(frame, text="Down", command=down)
buttondocs = Button(frame, text="Docs", command=docs)

quitbutton = Button(frame, text="Quit", command=root.destroy)
gobutton = Button(frame, text="GO", command=calcu)

configbut = Button(frame, text="CFG", command=trouble)

# Frame1
labelstart.grid(columnspan=3)
dirlabel.grid(row=1, columnspan=3)
dirinput.grid(row=2, columnspan=3)
check1.grid(row=3, sticky=W)
check2.grid(row=4, sticky=W)
check3.grid(row=5, sticky=W)
check4.grid(row=6, sticky=W)
check5.grid(row=7, sticky=W)
check6.grid(row=8, sticky=W)
subcheck.grid(row=9, sticky=W)

buttondesk.grid(row=3, column=2, sticky=E)
buttondown.grid(row=4, column=2, sticky=E)
buttondocs.grid(row=5, column=2, sticky=E)
quitbutton.grid(row=8, column=2, sticky=E)
configbut.grid(row=7, column=2, sticky=E)
gobutton.grid(row=9, column=2, sticky=E)

# frameend
quitf2 = Button(frameend, text="Quit", command=root.destroy)
restartf2 = Button(frameend, text="Retry", command=reset)
restartf2.pack()

optentry = StringVar()
optdefault = ["txt", "exe", "py", "zip", "rar", "pdf"]
opts = optdefault
comboend = OptionMenu(frameend, oc, *opts, command=comboans)
buttontest = Button(frameend, text="Print", command=lambda: print(optentry))

comboend.event_generate("<Down>", when="head")

comboend.pack()
buttontest.pack()

# FRAME 1 WIDGET CONFIGS
buttondesk.config(width="5")
buttondown.config(width="5")
buttondocs.config(width="5")
quitbutton.config(width="5")
gobutton.config(width="5")
configbut.config(width="5")

dirinput.config(width="30")

# STUFF
user = ""
# FUNCTION HERE.
inital()

##popup_user()

root.mainloop()