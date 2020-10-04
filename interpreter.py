import os
from tkinter import *
from subprocess import *


class PythonShell:

    def __init__(self):
        self.master = Tk()

        self.mem_cache = open("idle.txt", "w+")
        self.body = None
        self.entry = None
        self.button = None
        self.entry_content = None

    @staticmethod
    def welcome_note():
        """
        To show welcome note on tkinter window
        :return:
        """
        Label(text="Welcome To My Python Program [Version 1.0]", font='Arial 12', background="#272626",
              foreground="white").pack()

        Label(text=">> Insert Python Commands <<", font='Arial 12', background="#272626",
              foreground="white").pack()

    def get_text(self):
        """
        This method will perform following operations;
        1- Get text from body
        2- Implies python compilation (treat text as command)
        3- Set Output in Output-Entry

        :return: get and set text in body of text box
        """
        content = self.body.get(1.0, "end-1c")
        out_put = self.run_commands(content)
        self.entry_content.set(out_put)

    def store_commands(self, command=None):

        try:
            self.mem_cache.write(command + ';')
            self.mem_cache.close()

        except Exception as e:
            print(e)

    def get_stored_commands(self):
        try:
            with open("idle.txt", "r") as self.mem_cache:
                self.mem_cache.seek(0)
                val = self.mem_cache.read()
                self.mem_cache.close()
                return val

        except Exception as e:
            print(e)

    @staticmethod
    def check_if_file_empty():
        size = os.stat("idle.txt").st_size

        if size != 0:
            return True
        else:
            return False

    def run_commands(self, command):
        """

        This method would return output of every command place in text box
        :param command: python command from text box
        :return: output of command
        """

        print("Running command: {}".format(command))
        value = None
        new_line_char = command.find('\n')
        semi_colons_char = command.find(';')
        double_quote = command.find('"')

        try:
            if new_line_char != -1:

                if semi_colons_char != -1 & double_quote == -1:

                    new_cmd = command.replace("\n", "")
                    cmd_value = '"' + new_cmd + '"'
                    self.store_commands(command)

                    value = check_output("python -c " + cmd_value, shell=True).decode()
                elif semi_colons_char == -1 & double_quote == -1:

                    new_cmd = command.replace("\n", ";")
                    cmd_value = '"' + new_cmd + '"'
                    self.store_commands(command)
                    value = check_output("python -c " + cmd_value, shell=True).decode()

                elif double_quote != -1:

                    cmd_1 = command.replace('"', "'")
                    new_cmd = cmd_1.replace('\n', ';')

                    cmd_value = '"' + new_cmd + '"'
                    self.store_commands(command)

                    value = check_output("python -c " + cmd_value, shell=True).decode()

                elif self.body.compare("end-1c", "==", "1.0"):
                    self.entry_content.set("the widget is empty")

            elif self.body.compare("end-1c", "==", "1.0"):
                value = "The widget is empty. Please Enter Something."

            else:
                variable_analyzer = command.find('=')
                file_size = PythonShell.check_if_file_empty()

                if file_size:
                    new_cmd = command.replace('"', "'")
                    cmd_value = '"' + new_cmd + '"'
                    stored_value = self.get_stored_commands()
                    cmd = stored_value + cmd_value
                    cmd.replace('"', '')

                    value = check_output("python -c " + cmd, shell=True).decode()
                elif variable_analyzer != -1:
                    new_cmd = command.replace('"', "'")
                    cmd_value = '"' + new_cmd + '"'
                    self.store_commands(cmd_value)

                    value = 'Waiting for input...'
                    pass
                else:
                    new_cmd = command.replace('"', "'")
                    cmd_value = '"' + new_cmd + '"'
                    value = check_output("python -c " + cmd_value, shell=True).decode()

        except Exception as ex:
            print('>>>', ex)
            self.entry_content.set('Invalid Command. Try again!!!')

        print('>>', value)
        # To Clear Text body After Button Click
        # self.body.delete('1.0', END)

        return value

    def start_terminal(self):
        """
        Initiate tkinter session to place and run commands
        :return:
        """
        self.master.propagate(0)
        self.master.geometry('750x350')
        self.master.title('Python IDLE')
        self.master.configure(background='#272626')

        terminal.welcome_note()

        self.body = Text(self.master, height='10', width='75', font='Consolas 12', background="#272626",
                         foreground="white",
                         insertbackground='white')
        # self.body.propagate(0)
        self.body.pack(expand=True)

        Label(text=">> Command Output <<", font='Arial 12', background="#272626",
              foreground="white").pack()

        self.entry_content = StringVar()
        self.entry = Entry(self.master, textvariable=self.entry_content, width=50, font='Consolas 16',
                           background="white",
                           foreground="black")
        self.entry.pack()
        # self.entry.propagate(0)

        self.button = Button(self.master, text="Run Command", command=self.get_text, background="white",
                             foreground="black",
                             font='Helvetica 12').pack()

        self.master.mainloop()


if __name__ == '__main__':
    terminal = PythonShell()
    terminal.start_terminal()
