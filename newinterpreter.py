import tkinter as tk
import sys, io
import subprocess as subp
from contextlib import redirect_stdout

class Shell(tk.Text):
  def __init__(self, parent, **kwargs):
    tk.Text.__init__(self, parent, **kwargs)
    self.bind('<Key>', self.on_key) # setup handler to process pressed keys
    self.cmd = None        # hold the last command issued
    self.show_prompt()

  # to append given text at the end of Text box
  def insert_text(self, txt='', end='\n'):
    self.insert(tk.END, txt+end)
    self.see(tk.END) # make sure it is visible

  def show_prompt(self):
    self.insert_text('>> ', end='')
    self.mark_set(tk.INSERT, tk.END) # make sure the input cursor is at the end
    self.cursor = self.index(tk.INSERT) # save the input position

  # handler to process keyboard input
  def on_key(self, event):
    #print(event)
    if event.keysym == 'Up':
      if self.cmd:
        # show the last command
        self.delete(self.cursor, tk.END)
        self.insert(self.cursor, self.cmd)
      return "break" # disable the default handling of up key
    if event.keysym == 'Down':
      return "break" # disable the default handling of down key
    if event.keysym in ('Left', 'BackSpace'):
      current = self.index(tk.INSERT) # get the current position of the input cursor
      if self.compare(current, '==', self.cursor):
        # if input cursor is at the beginning of input (after the prompt), do nothing
        return "break"
    if event.keysym == 'Return':
      # extract the command input
      cmd = self.get(self.cursor, tk.END).strip()
      self.insert_text() # advance to next line
      if cmd.startswith('`'):
        # it is an external command
        self.system(cmd)
      else:
        # it is python statement
        self.execute(cmd)
      self.show_prompt()
      return "break" # disable the default handling of Enter key
    if event.keysym == 'Escape':
      self.master.destroy() # quit the shell

  # function to handle python statement input
  def execute(self, cmd):
    self.cmd = cmd  # save the command
    # use redirect_stdout() to capture the output of exec() to a string
    f = io.StringIO()
    with redirect_stdout(f):
      try:
        exec(self.cmd, globals())
      except Exception as e:
        print(e)
    # then append the output of exec() in the Text box
    self.insert_text(f.getvalue(), end='')

  # function to handle external command input
  def system(self, cmd):
    self.cmd = cmd  # save the command
    try:
      # extract the actual command
      cmd = cmd[cmd.index('`')+1:cmd.rindex('`')]
      proc = subp.Popen(cmd, stdout=subp.PIPE, stderr=subp.PIPE, text=True)
      stdout, stderr = proc.communicate(5) # get the command output
      # append the command output to Text box
      self.insert_text(stdout)
    except Exception as e:
      self.insert_text(str(e))

root = tk.Tk()
root.title('Simple Python Shell')

shell = Shell(root, width=100, height=50, font=('Consolas', 10))
shell.pack(fill=tk.BOTH, expand=1)
shell.focus_set()

root.mainloop()
