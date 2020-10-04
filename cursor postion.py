import tkinter as tk

def check_pos(event):
    print(t.index(tk.INSERT))

root = tk.Tk()

t = tk.Text(root)
t.pack()
t.bindtags(('Text','post-class-bindings', '.', 'all'))

t.bind_class("post-class-bindings", "<KeyPress>", check_pos)
t.bind_class("post-class-bindings", "<Button-1>", check_pos)


root.mainloop()