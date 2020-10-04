from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import datetime
# pip install tkfontchooser
from tkfontchooser import askfont

class Menubar():
    def __init__(self, parent):
        # important stuffs ...
        font_style = ('arial',10)
        menubar = Menu(parent.root,font=font_style)
        parent.root.config(menu=menubar)

        # file menu -------------------------------------------
        file_menu = Menu(menubar,font=font_style,tearoff = 0)
        file_menu.add_command(label = "New File",command=parent.new_file , accelerator='Ctrl+N')
        file_menu.add_command(label = "Open File" , command = parent.open_file, accelerator='Ctrl+O')
        file_menu.add_command(label = "Save " , command = parent.save_file, accelerator='Ctrl+S')
        file_menu.add_command(label = "Save As" , command =parent.save_as_file, accelerator='Ctrl+Shift+S')
        file_menu.add_separator()
        file_menu.add_command(label = "Exit App." , command = parent.close_App, accelerator='Ctrl+Q')

        # tool menu -----------------------------
        tool_menu = Menu(menubar, font=font_style, tearoff=0)
        tool_menu.add_command(label="Find ", command=parent.find_word_window)
        tool_menu.add_command(label="Find and Replace ", command=parent.find_replace_window)
        tool_menu.add_command(label="Refresh ", command= parent.refresh)
        tool_menu.add_command(label="Font ", command=parent.select_font)
        tool_menu.add_command(label="Add Time ", command=parent.add_time)
        tool_menu.add_command(label="Add Date ", command=parent.add_date)
        tool_menu.add_command(label="Add Time/Date ", command=parent.add_time_date)

        # About menu -----------------------------
        about_menu = Menu(menubar, font=font_style, tearoff=0)
        about_menu.add_command(label="About PyNote", command=parent.about_us)
        about_menu.add_command(label=" Version ", command=parent.about_pynote)

        # configure menubars ....
        menubar.add_cascade(label = 'File', menu = file_menu)
        menubar.add_cascade(label = 'Tools' , menu = tool_menu)
        menubar.add_cascade(label='About', menu=about_menu)





class PyNote:
    def __init__(self,root):
        self.root = root
        self.root.title('Untitled - PyNote')
        self.root.configure( bg='lightgray')
        self.root.geometry('950x600')
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.minsize(width=700, height=400)

        # important stuffs ...
        self.font_style = ('arial',14)
        self.filename = None
        self.file_saved = True
        self.index=0

        # widgets ,........
        self.textarea = ScrolledText(self.root,font=self.font_style,undo=True, wrap = WORD)
        #self.textarea.bindtags(('Text','post-class-bindings', '.', 'all'))
        self.textarea.pack(fill=BOTH,expand=True)
        self.shortcut_binding()

        self.status = StringVar()
        self.pos = StringVar()

        self.status.set('PyNote - ({})'.format('Untitled File'))
        # important stuffs ...
        font_style = ('arial', 13)
        self.label = Label(self.root, textvariable=self.status, fg='black', bg='lightgray', anchor=SW, font=font_style)
        self.label.pack(side=LEFT,fill=BOTH)


        # cursor postion label...
        self.cursor_pos_lbl = Label(self.root, textvariable=self.pos, fg='black', bg='lightgray', anchor=NW, font=font_style)
        self.cursor_pos_lbl.pack(side=RIGHT)

        # code for popup menu bar ....
        # creating menu-bar ...
        self.m = Menu(root, tearoff=0)
        self.m.add_command(label="Refresh", command=self.refresh)
        self.m.add_command(label = "Select All",command=self.select_all)
        self.m.add_command(label="Cut", command=lambda: self.textarea.event_generate("<<Cut>>"))
        self.m.add_command(label="Copy", command=lambda: self.textarea.event_generate("<<Copy>>"))
        self.m.add_command(label = "Paste", command=lambda: self.textarea.event_generate("<<Paste>>"))
        self.m.add_command(label="Delete", command=lambda: self.textarea.delete(SEL_FIRST, SEL_LAST))
        self.m.add_command(label="Add Date/Time", command=self.add_time_date)

        # Calling functions and other class methods or creating objects ......
        self.menubar = Menubar(self)


    # function definations .................

    def set_title(self,name= None):
        if name:
            self.root.title(name + " - PyNote")
        else:
            self.root.title('Untitled - PyNote')



    def new_file(self, event = None):
        self.textarea.delete(1.0, END)
        # call the save command if any text is written on text area ..
        self.filename = None
        self.set_title()
        self.update_status('PyNote - ({})'.format('Untitled File'))


    def open_file(self, *args):
        self.filename = filedialog.askopenfilename( defaultextension = ".txt",
                                                    filetypes = [("All Files" , "*.*"),
                                                                 ("Text Files" , "*.txt"),
                                                                 ("Python Scripts" , "*.py"),
                                                                 ('HTML Docs.' , "*.html"),
                                                                 ("CSS Docs.","*.css")])
        if self.filename:
            self.textarea.delete(1.0,END)
            with open(self.filename , "r") as f :
                self.textarea.insert(1.0,f.read())
            self.update_status('File is Opened /  ' + self.filename)
        self.set_title(self.filename)





    def save_file(self, *args):
        if self.filename:
            try:
                textarea_data = self.textarea.get(1.0,END)
                with open(self.filename, 'w') as f:
                    f.write(textarea_data)
                self.update_status('File is Saved Again ')
                self.file_saved = True

            except Exception as e:
                messagebox.showerror('PyNote -Says ','Error Occurs '+ str(e))
        else:
            self.save_as_file()


    def save_as_file(self, *args):
        try:
            new_file = filedialog.asksaveasfilename(initialfile = 'Untitled.txt',
                                                    defaultextension=".txt",
                                                    filetypes=[("All Files", "*.*"),
                                                               ("Text Files", "*.txt"),
                                                               ("Python Scripts", "*.py"),
                                                               ('HTML Docs.', "*.html"),
                                                               ("CSS Docs.", "*.css")]
                                                    )
            textarea_data =  self.textarea.get(1.0,END)
            with open(new_file , 'w') as f:
                f.write(textarea_data)
            self.filename = new_file
            self.set_title(self.filename)
            self.file_saved = True
            self.update_status('File is Saved As '+ self.filename)
        except Exception as e:
            messagebox.showerror('PyNote -Says ','Error Occurs '+ str(e))


    def about_us(self):
        messagebox.showinfo('About - Us','''
        PyNote is a Text Editor which is looks like a Notepad \n
        PyNote is Build as a Demo Project for those Who are \n
        interested in building Awesome GUI Projects using Tkinter\n
        _________________________________________________________\n
        PyNote Developer : Yogesh Singh \n
        Build For : Dynamic Coding \n''')

    def about_pynote(self):
        messagebox.showinfo('About - PyNote','''
        Current Version : 0.0 \n
        ''')


    def shortcut_binding(self):
        self.textarea.bind('<Control-n>',self.new_file)
        self.textarea.bind('<Control-Key-o>',self.open_file)
        self.textarea.bind('<Control-s>',self.save_file)
        self.textarea.bind('<Control-S>',self.save_as_file)
        self.textarea.bind('<Control-q>',self.close_App)
        self.textarea.bind('<Key>', self.text_area_cursor)
        #self.textarea.bind('<KeyPress>', self.cursor_pos)

        self.root.bind("<Button-3>", self.do_popup)

    def do_popup(self, event):
        try:
            self.m.tk_popup(event.x_root, event.y_root)
        finally:
            self.m.grab_release()

    def find_word_window(self):
        top = Toplevel(self.root)
        top.geometry('400x130')
        top.title('PyNote - Find Text ')
        top.resizable(0,0)

        # important stuffs ...........
        find_var = StringVar()
        self.total_var =StringVar()

        # --------------------------find window widgets ----------------------
        self.find_entry = ttk.Entry(top,width=20,font=('times',12), textvariable = find_var)
        self.find_entry.focus_set()
        self.find_entry.bind('<Return>',self.find)
        self.find_entry.place(x=10,y=25)

        find_btn = Button(top,text='Find',width=10,bd=2,relief=RIDGE,command=self.find)
        find_btn.place(x=200,y=25)

        clear_btn = Button(top, text='Clear', width=10, bd=2, relief=RIDGE,command=lambda:find_var.set(''))
        clear_btn.place(x=300, y=25)

        self.total_world_count = Label(top,font=('arial',13,'bold'))
        self.total_world_count.place(x=20,y=80)

        top.mainloop()


    def find(self, *args):
        # remove tag 'found' from index 1 to END
        self.textarea.tag_remove('found', '1.0', END)

        # returns to widget currently in focus
        s = self.find_entry.get()

        if (s):
            idx = '1.0'
            self.count=0
            while 1:
                # searches for desried string from index 1
                idx = self.textarea.search(s, idx, nocase=1,
                                  stopindex=END)
                self.count +=1

                if not idx: break

                # last index sum of current index and
                # length of text
                lastidx = '% s+% dc' % (idx, len(s))

                # overwrite 'Found' at idx
                self.textarea.tag_add('found', idx, lastidx)
                idx = lastidx

            # mark located string as red
            self.textarea.tag_config('found', foreground='green', background='yellow')
            #self.textarea.focus_set()
            self.total_world_count['text'] = 'Total Word Count is : ' + str(self.count -1 )



    def refresh(self):

        self.textarea.tag_delete("found")


    def find_replace_window(self):
        top = Toplevel(self.root)
        top.geometry('400x130')
        top.title('PyNote - Find Text ')
        top.focus_force()
        top.resizable(0, 0)

        # important stuffs ...........
        find_var = StringVar()
        replace_var = StringVar()

        # --------------------------find replace window widgets ----------------------
        self.find_entry = ttk.Entry(top, width=20, font=('times', 12), textvariable=find_var)
        self.find_entry.focus_set()
        self.find_entry.bind('<Return>', self.find)
        self.find_entry.place(x=10, y=25)

        self.replace_entry = ttk.Entry(top, width=20, font=('times', 12), textvariable=replace_var)
        #self.replace_entry.focus_set()
        self.replace_entry.bind('<Return>', self.find_replace)
        self.replace_entry.place(x=10, y=60)

        find_btn = Button(top, text='Find', width=10, bd=2, relief=RIDGE, command=self.find)
        find_btn.place(x=200, y=25)

        replace_btn = Button(top, text='Replace', width=10, bd=2, relief=RIDGE,
                             command=self.find_replace)
        replace_btn.place(x=200, y=60)

        clear_btn = Button(top, text='Clear All', width=10,height=3, bd=2, relief=RIDGE, command=lambda: [find_var.set(''),replace_var.set('')])
        clear_btn.place(x=300, y=26)

        self.total_world_count = Label(top, text='',font=('arial', 13, 'bold'))
        self.total_world_count.place(x=20, y=100)

        top.mainloop()


    def find_replace(self, *args):
        find = self.find_entry.get()
        replace = self.replace_entry.get()

        if(find and replace):
            idx = '1.0'
            while 1:
                # searches for desired string from index 1
                idx = self.textarea.search(find, idx, nocase=1,
                                  stopindex=END)
                print(idx)
                if not idx: break

                # last index sum of current index and
                # length of text
                lastidx = '% s+% dc' % (idx, len(find))

                self.textarea.delete(idx, lastidx)
                self.textarea.insert(idx, replace)

                lastidx = '% s+% dc' % (idx, len(replace))

                # overwrite 'Found' at idx
                self.textarea.tag_add('found', idx, lastidx)
                idx = lastidx

            self.total_world_count['text'] = '" {} " is replaced with " {} "'.format(find,replace)
        self.replace_entry.focus_set()

    def close_App(self, *args):
        print(self.textarea.get(1.0,END))
        if self.textarea.get(1.0,END) != '' and self.file_saved == True:
            if messagebox.askyesno('PyNote Says','Do you really want to exit'):
                self.root.quit()
        else:
            val = messagebox.askyesnocancel('PyNote - Says', 'Save File Before Exit App. ')
            if val:
                self.save_file()
                self.root.destroy()
            elif val == False:
                self.root.destroy()

    def text_area_cursor(self, *args):
        #print('inside function ')
        self.file_saved = False
        if self.filename:
            self.update_status('PyNote - Currently Working on : ({})'.format(self.filename))
        else:
            self.update_status('Untitled File')

        pos = self.textarea.index(INSERT)
        line , column = pos.split('.')
        column = int(column) + 1
        #print('Current line is : ',line)
        #print('Current Column is : ', column)
        self.pos.set('Line : {} Column : {}'.format(line,column))

    def cursor_pos(self, *args):
        pos = self.textarea.index(INSERT)
        line, column = pos.split('.')
        column = int(column) + 1
        self.pos.set('Line : {} Column : {}'.format(line, column))



    def update_status(self,data=''):
        self.status.set('PyNote - ({})'.format(data))


    def select_font(self):
        font= askfont()
        # font is "" if the user has cancelled
        if font:
            # spaces in the family name need to be escaped
            font['family'] = font['family'].replace(' ', '\ ')
            font_str = "%(family)s %(size)i %(weight)s %(slant)s" % font
            if font['underline']:
                font_str += ' underline'
            if font['overstrike']:
                font_str += ' overstrike'

            self.font_style = font_str
            self.textarea.configure(font=self.font_style)


    def add_time(self):
        now = datetime.datetime.now()
        now = now.strftime(' Time: %I:%M:%S:%p ')
        self.textarea.insert(END, now)


    def add_date(self):
        now = datetime.datetime.now()
        now = now.strftime(' %Y-%m-%d ')
        self.textarea.insert(END, now)


    def add_time_date(self):
        now = datetime.datetime.now()
        now = now.strftime(' Date: %Y-%m-%d Time: %I:%M:%S:%p ')
        self.textarea.insert(END,now)

    # Select all the text in textbox
    def select_all(self, *args):
        self.textarea.tag_add(SEL, "1.0", END)
        self.textarea.mark_set(INSERT, "1.0")
        self.textarea.see(INSERT)

    def callback(self):
        if(self.file_saved) and (self.textarea.get(1.0,END)) != '':
            if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
                self.root.destroy()
        else:
            val = messagebox.askyesnocancel('PyNote - Says','Save File Before Exit App. ')
            if val:
                self.save_file()
            elif val== False:
                self.root.destroy()





if __name__ == '__main__':
    root= Tk()
    py = PyNote(root)
    root.mainloop()
