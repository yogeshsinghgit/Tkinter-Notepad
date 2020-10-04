import re
import tkinter as tk
import keyword

CODE = """#include <test.h>
#include "test.h"

for (int i = 0; i< 10;i++ ) {
    if (i < 3){
       int hello;
    }
}"""


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
        r"(?P<include>#include\s+[\"<]\S+)" + "|"
        r"(?P<int>int)"  # variable
        r"[\s\(]+)"
    )
    for idx, line in enumerate(lines):
        int_tag = f"int_{idx}"
        for_tag = f"for_{idx}"
        if_tag = f"if_{idx}"
        include_tag = f"include_{idx}"
        tags = {
            int_tag: "blue",
            for_tag: "green",
            if_tag: "purple",
            include_tag: "green",
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

    text = tk.Text(root)
    text.grid()

    text.bind("<KeyRelease>", lambda event: on_key_release(text))
    text.bind("<Enter>", lambda event: on_key_release(text))

    text.insert(tk.END, CODE)

    root.mainloop()


if __name__ == "__main__":
    main()