import tkinter as Tk

def get_info():
    print(e1.index(Tk.INSERT))

def make_menu(w):
    global the_menu
    the_menu = Tk.Menu(w, tearoff=0)

    the_menu.add_command(label="Cut")
    the_menu.add_command(label="Copy")
    the_menu.add_command(label="Paste")

def show_menu(e):
    w = e.widget
    the_menu.entryconfigure("Cut",
    command=lambda: w.event_generate("<<Cut>>"))
    the_menu.entryconfigure("Copy",
    command=lambda: w.event_generate("<<Copy>>"))
    the_menu.entryconfigure("Paste",
    command=lambda: w.event_generate("<<Paste>>"))
    the_menu.tk.call("tk_popup", the_menu, e.x_root, e.y_root)

t = Tk.Tk()
make_menu(t)

e1 = Tk.Text(); e1.pack()
#e2 = Tk.Entry(); e2.pack()
e1.bind_class("Text", "<Button-3>", show_menu)

btn = Tk.Button(t, text="get info", command=get_info).pack()

t.mainloop()