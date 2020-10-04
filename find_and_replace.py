from tkinter import *

# to create a window
root = Tk()
root.title('Dynamic Coding')
# root window is the parent window
frame = Frame(root)

# Creating Label, Entry Box, Button
# and packing them adding label to
# search box
Label(frame, text='Find').pack(side=LEFT)

# adding of single line text box
edit = Entry(frame)
# positioning of text box
edit.pack(side=LEFT, fill=BOTH, expand=1)
# setting focus
edit.focus_set()

# adding of search button
Find = Button(frame, text='Find')
Find.pack(side=LEFT)

Label(frame, text="Replace With ").pack(side=LEFT)

edit2 = Entry(frame)
edit2.pack(side=LEFT, fill=BOTH, expand=1)
edit2.focus_set()

replace = Button(frame, text='FindNReplace')
replace.pack(side=LEFT)

refresh = Button(frame, text='Refresh')
refresh.pack(side=LEFT)

frame.pack(side=TOP)

# text box in root window
text = Text(root)

# text input area at index 1 in text window
text.insert('1.0', '''Hello World !   :D''')
text.pack(side=BOTTOM)


# function to search string in text
def find(*args):
    # remove tag 'found' from index 1 to END
    text.tag_remove('found', '1.0', END)

    # returns to widget currently in focus
    s = edit.get()

    if (s):
        idx = '1.0'
        while 1:
            # searches for desried string from index 1
            idx = text.search(s, idx, nocase=1,
                              stopindex=END)

            if not idx: break
            # last index sum of current index and
            # length of text
            lastidx = '% s+% dc' % (idx, len(s))
            print(lastidx)
            print(idx)
            # overwrite 'Found' at idx
            text.tag_add('found', idx, lastidx)
            idx = lastidx

        # mark located string as green and bg = ''yellow
        text.tag_config('found', foreground='green', background='yellow')
    edit.focus_set()


def findNreplace(*args):
    # remove tag 'found' from index 1 to END
    text.tag_remove('found', '1.0', END)

    # returns to widget currently in focus
    s = edit.get()
    r = edit2.get()

    if (s and r):
        idx = '1.0'
        while 1:
            # searches for desried string from index 1
            idx = text.search(s, idx, nocase=1,
                              stopindex=END)
            print(idx)
            if not idx: break

            # last index sum of current index and
            # length of text
            lastidx = '% s+% dc' % (idx, len(s))

            text.delete(idx, lastidx)
            text.insert(idx, r)

            lastidx = '% s+% dc' % (idx, len(r))

            # overwrite 'Found' at idx
            text.tag_add('found', idx, lastidx)
            idx = lastidx

        # mark located string as green and bg = ''yellow
        text.tag_config('found', foreground='green', background='yellow')
    edit.focus_set()

def refresh_func():
    text.tag_delete('found')

# add commands to button
Find.config(command=find)
replace.config(command=findNreplace)
refresh.config(command=refresh_func)
# binding entry boxes ...
edit.bind('<Return>',find)
edit2.bind('<Return>',findNreplace)

# mainloop function calls the endless
# loop of the window, so the window will
# wait for any user interaction till we
# close it
root.mainloop()
