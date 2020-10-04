import re
import tkinter as tk

CODE = """
import os
if True:
    for in in range(10):
        print('hello world')
"""


def configure_tags(text_widget, tags):
    for tag, color in tags.items():
        text_widget.tag_delete(tag)
        text_widget.tag_config(tag, foreground=color)


def on_key_release(text_widget):
    lines = text_widget.get(1.0, tk.END).splitlines()
    regex = re.compile(
        r"(^\s*"
        r"(?P<if>if)" + "|"  # if condition
        r"(?P<for>for)" + "|"  # for loop
        r"(?P<import>import\s+[\"<]\S+)" + "|"
        r"(?P<while>while)" 
        r"(?P<print>print)" 
        r"(?P<else>else)"
        r"(?P<elif>elif)"# variable
        r"[\s\(]+)"
    )
    for idx, line in enumerate(lines):
        elif_tag = f"elif_{idx}"
        for_tag = f"for_{idx}"
        while_tag = f"while_{idx}"
        if_tag = f"if_{idx}"
        import_tag = f"import_{idx}"
        else_tag = f"else_{idx}"
        print_tag = f"print_{idx}"
        tags = {
            while_tag: "green",
            for_tag: "green",
            if_tag: "purple",
            else_tag:'purple',
            elif_tag: 'purple',
            import_tag: "red",
            print_tag: "red"
            # add new tag here
        }
        configure_tags(text_widget, tags)

        for match in regex.finditer(line):
            for tag in tags:
                group_name = tag.split("_")[0]
                if -1 != match.start(group_name):
                    text_widget.tag_add(
                        tag,
                        "{0}.{1}".format(idx+1, match.start(group_name)),
                        "{0}.{1}".format(idx+1, match.end(group_name))
                    )


def main():
    root = tk.Tk()

    text = tk.Text(root,font=('arial',12))
    text.grid()

    text.bind("<KeyRelease>", lambda event: on_key_release(text))
    text.bind("<Enter>", lambda event: on_key_release(text))

    text.insert(tk.END, CODE)

    root.mainloop()


if __name__ == "__main__":
    main()