from customtkinter import CTkFrame
from tkinter import Widget


class CTkStack(CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self._pages = {}

    def add(self, page: Widget, id: int = 0):
        self._pages[id] = page

    def show(self, id: int, *args, **kwargs):
        self._pages[id].pack(fill="both", expand="yes")
        self._pages[id].pack(*args, **kwargs)
        for item in self._pages.keys():
            if not item == id:
                self.hide(item)

    def hide(self, id: int):
        self._pages[id].pack_forget()

    @property
    def page(self, id: int):
        return self._pages[id]

    @property
    def pages(self):
        return self._pages