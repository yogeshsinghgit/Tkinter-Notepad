from tkinter import *
from tkinter import ttk
import win32api
import win32print
import tempfile



def installed_printer():
    printers = win32print.EnumPrinters(2)
    for p in printers:
        return(p)

printerdef = ''

def locprinter():
    pt = Toplevel()
    pt.geometry("250x250")
    pt.title("choose printer")
    var1 = StringVar()
    LABEL = Label(pt, text="select Printer").pack()
    PRCOMBO = ttk.Combobox(pt, width=35,textvariable=var1)
    print_list = []
    printers = list(win32print.EnumPrinters(2))
    for i in printers:
        print_list.append(i[2])
    print(print_list)
    # Put printers in combobox
    PRCOMBO['values'] = print_list
    PRCOMBO.pack()
    def select():
        global printerdef
        printerdef = PRCOMBO.get()
        pt.destroy()
    BUTTON = ttk.Button(pt, text="Done",command=select).pack()

root = Tk()
root.title("printer selection in tkinter")
root.geometry("400x400")


menubar = Menu(root)
root.config(menu=menubar)

file_menu = Menu(menubar)
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="printer", command=locprinter)


LAB = Label(root, text="Comment")
T2 = Text(root, width=40, height=10, wrap=WORD)


def INFO():
    printText = T2.get("1.0", END)
    print(printText)
    print(printerdef)
    filename = tempfile.mktemp(".txt")
    open(filename, "w").write(printText)
    # Bellow is call to print text from T2 textbox
    win32api.ShellExecute(
        0,
        "printto",
        filename,
        '"%s"' % win32print.GetDefaultPrinter(),
        ".",
        0
    )


Print_Button = Button(root, text ="Print", command=INFO).place(x=180,y=250)

LAB.pack()
T2.pack()

root.mainloop()