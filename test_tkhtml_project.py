import tkinter as tk
from tkhtmlview import HTMLLabel

root = tk.Tk()
root.title("Test Html on Tkinter")
root.configure(bg='black')

data = """<!-- Dynamic Coding output code  -->
<p style="border: 2px solid rgb(51, 103, 214); font-size: 15px; padding: 0.2em 0.6em;"><font face="arial">
<kbd style="border-radius: 0px; border: 1px solid rgb(51, 103, 214); padding: 3px;color:#3367d6;"><b>&nbsp;  Output &nbsp;</b></kbd>
<br />
<code style="color:#ff0000">
deque(['A', 'B', 'C', 'D'])


</code>
</font></p>
<br />


"""
html_label = HTMLLabel(root, html=data)
html_label.pack(fill="both", expand=True)
html_label.fit_height()
root.mainloop()