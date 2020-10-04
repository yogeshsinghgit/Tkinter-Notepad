from cefpython3 import cefpython as cef
import ctypes
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk # for version 2
import sys
import platform
import logging as _logging

# Fix for PyCharm hints warnings
WindowUtils = cef.WindowUtils()

# Platforms
WINDOWS = (platform.system() == "Windows")
LINUX = (platform.system() == "Linux")
MAC = (platform.system() == "Darwin")

# Globals
logger = _logging.getLogger("tkinter_.py")

class MainFrame(tk.Frame):

    def __init__(self, root):
        self.browser_frame = None
        self.navigation_bar = None

        # Root
        root.geometry("900x640")
        tk.Grid.rowconfigure(root, 0, weight=1)
        tk.Grid.columnconfigure(root, 0, weight=1)

        # MainFrame
        tk.Frame.__init__(self, root)
        self.master.title("Web Browser @Dynamic Coding")
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        self.master.bind("<Configure>", self.on_root_configure)
        self.bind("<Configure>", self.on_configure)
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)

        # NavigationBar
        self.navigation_bar = NavigationBar(self)
        self.navigation_bar.grid(row=0, column=0,
                                 sticky=(tk.N + tk.S + tk.E + tk.W))
        tk.Grid.rowconfigure(self, 0, weight=0)
        tk.Grid.columnconfigure(self, 0, weight=0)

        # BrowserFrame
        self.browser_frame = BrowserFrame(self, self.navigation_bar)
        self.browser_frame.grid(row=1, column=0,
                                sticky=(tk.N + tk.S + tk.E + tk.W))
        tk.Grid.rowconfigure(self, 1, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)

        # Pack MainFrame
        self.pack(fill=tk.BOTH, expand=tk.YES)

    def on_root_configure(self, _):
        logger.debug("MainFrame.on_root_configure")
        if self.browser_frame:
            self.browser_frame.on_root_configure()

    def on_configure(self, event):
        logger.debug("MainFrame.on_configure")
        if self.browser_frame:
            width = event.width
            height = event.height
            if self.navigation_bar:
                height = height - self.navigation_bar.winfo_height()
            self.browser_frame.on_mainframe_configure(width, height)

    def on_focus_in(self, _):
        logger.debug("MainFrame.on_focus_in")

    def on_focus_out(self, _):
        logger.debug("MainFrame.on_focus_out")

    def on_close(self):
        if self.browser_frame:
            self.browser_frame.on_root_close()
        self.master.destroy()

    def get_browser(self):
        if self.browser_frame:
            return self.browser_frame.browser
        return None

    def get_browser_frame(self):
        if self.browser_frame:
            return self.browser_frame
        return None

class BrowserFrame(tk.Frame):

    def __init__(self, master, navigation_bar=None):
        self.navigation_bar = navigation_bar
        self.closing = False
        self.browser = None
        tk.Frame.__init__(self, master)
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)
        self.bind("<Configure>", self.on_configure)
        self.focus_set()

    def embed_browser(self):
        window_info = cef.WindowInfo()
        rect = [0, 0, self.winfo_width(), self.winfo_height()]
        window_info.SetAsChild(self.get_window_handle(), rect)
        self.browser = cef.CreateBrowserSync(window_info,
                                             url="http://www.google.com") #todo
        assert self.browser
        self.browser.SetClientHandler(LoadHandler(self))
        self.browser.SetClientHandler(FocusHandler(self))
        self.message_loop_work()

    def get_window_handle(self):
        if self.winfo_id() > 0:
            return self.winfo_id()
        elif MAC:
            from AppKit import NSApp
            import objc
            return objc.pyobjc_id(NSApp.windows()[-1].contentView())
        else:
            raise Exception("Couldn't obtain window handle")

    def message_loop_work(self):
        cef.MessageLoopWork()
        self.after(10, self.message_loop_work)

    def on_configure(self, _):
        if not self.browser:
            self.embed_browser()

    def on_root_configure(self):
        # Root <Configure> event will be called when top window is moved
        if self.browser:
            self.browser.NotifyMoveOrResizeStarted()

    def on_mainframe_configure(self, width, height):
        if self.browser:
            if WINDOWS:
                ctypes.windll.user32.SetWindowPos(
                    self.browser.GetWindowHandle(), 0,
                    0, 0, width, height, 0x0002)
            elif LINUX:
                self.browser.SetBounds(0, 0, width, height)
            self.browser.NotifyMoveOrResizeStarted()

    def on_focus_in(self, _):
        logger.debug("BrowserFrame.on_focus_in")
        if self.browser:
            self.browser.SetFocus(True)

    def on_focus_out(self, _):
        logger.debug("BrowserFrame.on_focus_out")
        if self.browser:
            self.browser.SetFocus(False)

    def on_root_close(self):
        if self.browser:
            self.browser.CloseBrowser(True)
            self.clear_browser_references()
        self.destroy()

    def clear_browser_references(self):
        self.browser = None

class LoadHandler(object):

    def __init__(self, browser_frame):
        self.browser_frame = browser_frame

    def OnLoadStart(self, browser, **_):
        if self.browser_frame.master.navigation_bar:
            self.browser_frame.master.navigation_bar.set_url(browser.GetUrl())

class FocusHandler(object):

    def __init__(self, browser_frame):
        self.browser_frame = browser_frame

    def OnTakeFocus(self, next_component, **_):
        logger.debug("FocusHandler.OnTakeFocus, next={next}"
                     .format(next=next_component))

    def OnSetFocus(self, source, **_):
        logger.debug("FocusHandler.OnSetFocus, source={source}"
                     .format(source=source))
        return False

    def OnGotFocus(self, **_):
        """Fix CEF focus issues (#255). Call browser frame's focus_set
           to get rid of type cursor in url entry widget."""
        logger.debug("FocusHandler.OnGotFocus")
        self.browser_frame.focus_set()

class NavigationBar(tk.Frame):
    def __init__(self, master):
        self.back_state = tk.NONE
        self.forward_state = tk.NONE
        self.back_image = None
        self.forward_image = None
        self.reload_image = None
        tk.Frame.__init__(self, master)

        # Back button
        back = b'iVBORw0KGgoAAAANSUhEUgAAAGAAAABgBAMAAAAQtmoLAAAAKlBMVEUAAAAyMjIzMzMzMzMyMjIzMzMxMTEzMzMtLS0zMzMkJCQyMjIrKysxMTExeYOJAAAADnRSTlMAgH3/cGlU1BHPDsoMWDQYbKYAAACNSURBVHgB7deBBYBAAIXha4YWaIdXJYlGaJwAzRFojhMarQnO+eWg3g9AvijnXXDZnKuawKpbCEgLA6QOAtLKAKmHgDYIDLuBDDBS4KDA+TsgQmC6IXAZyADpEkA6CogC/AH+SpQIlIAf7v2vYSIGfJBR4ihFmNjx+KHE8AliLjlD6dAFUxqMdX4dcM49/KeCIizV7gUAAAAASUVORK5CYII='
        self.back_image = tk.PhotoImage(data=back)
        self.back_image = self.back_image.zoom(25).subsample(100)
        self.back_button = tk.Button(self, image=self.back_image,command=self.go_back)
        self.back_button.grid(row=0, column=0)

        # Forward button
        forward = b'iVBORw0KGgoAAAANSUhEUgAAAGAAAABgCAYAAADimHc4AAAA1UlEQVR4Ae3cAQbCYBzG4Q6QiI4wYIbtPU1HCAgQSOcLgtBtamHQAb5/43noAu8Pmu37NgAAAAAAAAAAAC0luU7TdNuUMP4lyfv7E6GxefDzMr4IheOL0FiS0zK2CI2N43hcRhahQJJDkqcIhYZh2IsgAiKIgAgi8BPhURiBrut2IoiACCIgggj8WQQR5mHvhRHo+35bEAERBMD4xl8V4/v7iQcw42N842N8L+XxWYrxMb7xMb5TMsZ/GX+Nh/RwTNVBbVxV4LIOXFcDAAAAAAAAAADwAephJFWvaMW3AAAAAElFTkSuQmCC'
        self.forward_image = tk.PhotoImage(data=forward)
        self.forward_image = self.forward_image.zoom(25).subsample(100)
        self.forward_button = tk.Button(self, image=self.forward_image,command=self.go_forward)
        self.forward_button.grid(row=0, column=1)

#        Reload button
        refresh = b'iVBORw0KGgoAAAANSUhEUgAAAGAAAABgCAQAAABIkb+zAAADwklEQVR4Ae2aY5jGVhCFZ+3a9iK7+XLPqW23v2rbtm3btm3btm3bbWpN8i0nt83z3Hd+Z+ac6GokEAgEAoFAIBAIBKyIGjkr1sJBuIoP8zV8w6/4Oh/GVTgIayWzRI0yJLiT+COZGjvzZnzLtJ/4Grdg+3gcGRTchqn4oG90bsvHmQ46vsPZycyDke/BgJsUR/IrpkMP3M0lpVaqgE2YFm+ghusNUbyOp9081eQXbqAyIW5hahBXurGz8gs3wOX4KVOjeBuUv+C6TIs2UMfjmVoGvnXLKPnFGWArru9Xzgs8kxu5mX7/53d2xJ2cCytwW57Jl/qx8BO3VfKLMTBVE++tfh9xUtwp/cA+nMbvq15/A9PCDfC8KsW/4IG948og6J0Yh/Pr/CyFG3Bb55b5EvtGY8gQiCfitfRvAAvgp5wiz7hJh/cfw8deDVSmwefZArg8bpNhEo2HW/wZqMGjOQWOkloZAWzgeZ4MuNVz0p9gcFtO8mIgauf72SmA1MoIUfKLM4Dts59u1C4jhEd5+oijdn6iPt1v2GUl34MBbKrTYhdD+R4MPKLSvj5Vk5V8DwZcTybt5jIicDBTjwawh3p9Pu/sMJTvwcD9evCyk+/BQDKanv9UnJ18DwawmEr5gQwb7s3Uv4Gt1BdwgaV8DwZ4gkq5haV8DwZw678TuoWkXOAp9QpNJeWCr6uHOpaUC719NVGLlAu9bo0aS/4KdY0p5YJPl/wjxm3/NpAsLOUCJ6onsKWUC26jfqPnSblwi2cmc+UiatfTaVeRcoH71FdwpBQETlNP+3YRD0tKK9wE/L6QH0Yl0lNct5kUAA7SdfqmEBvwqPW2Su5O9Reqyh1iBTbR9wY7izE8S9dwq4sVE7XoKR2+iTvFkGTm7NGr6bQR25lu7iriNj6Tyb+u9Wjwni6Bq6RWLKjLObZ90Xza7lYzO+BQ8JRsZjePmFPDh+2PmKQWh+RkvViKIO7MO+TjFXHbCHb9bszJ+KlqiLLDLWR5zOqmxStMs+GWEU3RB934AvtyrCH+mPfDj7m5DpJiwTnVWw04/uDEc2V179WfrVCmasL9w232YEMyH07ml0yryWeDGGDSboMZf/+TT9bM8dGdzMKNeIWSruM8qRdP1OmVskEcJTXiEyzFT8zEf+1WE//0TmzU9PdgMrX8R9Rg/RG2Xb7lVjN6dfw3vvJTt4PBVrFZ6/FjQxL/KrY32GX11PytpR+ZzCe1/+P2+2SWP9rvH/qt/f73lsoXcSF3xGLxRGJEIBAIBAKBQCAQCPwM9/tgs3UybYkAAAAASUVORK5CYII='
        self.reload_image = tk.PhotoImage(data=refresh)
        self.reload_image = self.reload_image.zoom(25).subsample(100)
        self.reload_button = tk.Button(self, image=self.reload_image,command=self.reload)
        self.reload_button.grid(row=0, column=2)

        # Url entry
        self.url_entry = tk.Entry(self)
        tk.Grid.rowconfigure(self, 0, weight=100)
        tk.Grid.columnconfigure(self, 3, weight=100)

        # Update state of buttons
        self.update_state()

    def go_back(self):
        if self.master.get_browser():
            self.master.get_browser().GoBack()

    def go_forward(self):
        if self.master.get_browser():
            self.master.get_browser().GoForward()

    def reload(self):
        if self.master.get_browser():
            self.master.get_browser().Reload()

    def set_url(self, url):
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, url)

    def on_url_focus_in(self, _):
        logger.debug("NavigationBar.on_url_focus_in")

    def on_url_focus_out(self, _):
        logger.debug("NavigationBar.on_url_focus_out")

    def on_load_url(self, _):
        if self.master.get_browser():
            self.master.get_browser().StopLoad()
            self.master.get_browser().LoadUrl(self.url_entry.get())

    def on_button1(self, _):
        """Fix CEF focus issues (#255). See also FocusHandler.OnGotFocus."""
        logger.debug("NavigationBar.on_button1")
        self.master.master.focus_force()

    def update_state(self):
        browser = self.master.get_browser()
        if not browser:
            if self.back_state != tk.DISABLED:
                self.back_button.config(state=tk.DISABLED)
                self.back_state = tk.DISABLED
            if self.forward_state != tk.DISABLED:
                self.forward_button.config(state=tk.DISABLED)
                self.forward_state = tk.DISABLED
            self.after(100, self.update_state)
            return
        if browser.CanGoBack():
            if self.back_state != tk.NORMAL:
                self.back_button.config(state=tk.NORMAL)
                self.back_state = tk.NORMAL
        else:
            if self.back_state != tk.DISABLED:
                self.back_button.config(state=tk.DISABLED)
                self.back_state = tk.DISABLED
        if browser.CanGoForward():
            if self.forward_state != tk.NORMAL:
                self.forward_button.config(state=tk.NORMAL)
                self.forward_state = tk.NORMAL
        else:
            if self.forward_state != tk.DISABLED:
                self.forward_button.config(state=tk.DISABLED)
                self.forward_state = tk.DISABLED
        self.after(100, self.update_state)

if __name__ == '__main__':
    logger.setLevel(_logging.INFO)
    stream_handler = _logging.StreamHandler()
    formatter = _logging.Formatter("[%(filename)s] %(message)s")
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.info("CEF Python {ver}".format(ver=cef.__version__))
    logger.info("Python {ver} {arch}".format(
            ver=platform.python_version(), arch=platform.architecture()[0]))
    logger.info("Tk {ver}".format(ver=tk.Tcl().eval('info patchlevel')))
    assert cef.__version__ >= "55.3", "CEF Python v55.3+ required to run this"
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    root = tk.Tk()
    app = MainFrame(root)
    # Tk must be initialized before CEF otherwise fatal error (Issue #306)
    cef.Initialize()
    app.mainloop()
    cef.Shutdown()