from customtkinter import CTk, CTkToplevel, CTkFrame, CTkLabel, CTkButton, ThemeManager, get_appearance_mode
from customtkinterx.CTkCustomBorder import CTkCustomBorder
from tkinter import ttk


def bind_move(widget, root):
    def _click(event):
        global x, y
        x, y = event.x, event.y

    def _move(event):
        new_x = (event.x - x) + root.winfo_x()
        new_y = (event.y - y) + root.winfo_y()
        s = f"+{new_x}+{new_y}"
        root.geometry(s)

    widget.bind("<Button-1>", _click, add="+")
    widget.bind("<B1-Motion>", _move, add="+")


class CTkCustom(CTkCustomBorder):
    def __init__(self, title: str = "", advanced: bool = True, titlebar: bool = True,
                 client_edge: bool = False, window_edge: bool = False, titlebar_layout: str = "pack", **kwargs):
        try:
            super().__init__(**kwargs)
        except:
            pass
        if titlebar:
            self.create_titlebar(title)

    def minimize(self):
        try:
            from ctypes import windll
            hwnd = windll.user32.GetParent(self.winfo_id())
            windll.user32.ShowWindow(hwnd, 2)
        except:
            pass

    def bind_move(self, widget):
        bind_move(widget, self)

    from tkinter import Event

    def _sizegrip_click(self, event: Event):
        from ctypes import Structure, c_ulong, byref, windll

        class _PointAPI(Structure):
            _fields_ = [("x", c_ulong), ("y", c_ulong)]

        def getpos():
            # 调用API函数获取当前鼠标位置。返回值以(x,y)形式表示。
            po = _PointAPI()
            windll.user32.GetCursorPos(byref(po))
            return int(po.x), int(po.y)

        self.sg_cx, self.sg_cy = getpos()
        self.sg_x, self.sg_y = self.winfo_x(), self.winfo_y()
        self.sg_width = self.winfo_width()
        self.sg_height = self.winfo_height()

    def _sizegrip_move(self, event: Event):
        from pyautogui import position

        dx = position()[0] - self.sg_cx
        dy = position()[1] - self.sg_cy

        try:
            self.geometry(f"{self.sg_width + dx}x{self.sg_height + dy}+{self.sg_x}+{self.sg_y}")
        except TypeError:
            pass

    def create_sizegrip(self, custom: bool = False):
        from sys import platform
        if custom:
            self.sizegrip = CTkButton(self.__frame_border, width=32, height=32, text="⚪")
            self.sizegrip.configure(cursor="sizing")

            self.sizegrip.bind("<Button-1>", self._sizegrip_click)
            self.sizegrip.bind("<B1-Motion>", self._sizegrip_move)
            self.sizegrip._text_color = ThemeManager.theme["CTkLabel"]["text_color"]
            self.sizegrip._fg_color = self.sizegrip._hover_color = self.mainframe._fg_color
            self.sizegrip._draw()
            self.sizegrip.pack(side="bottom", anchor="se", padx=3, pady=3)
        else:
            if get_appearance_mode() == "Dark":
                ttk.Style().configure("CTkCustom.TSizegrip", background=ThemeManager.theme["CTkFrame"]["fg_color"][1])
            else:
                ttk.Style().configure("CTkCustom.TSizegrip", background=ThemeManager.theme["CTkFrame"]["fg_color"][0])
            self.sizegrip = ttk.Sizegrip(self.mainframe, style="CTkCustom.TSizegrip")
            self.sizegrip.pack(side="bottom", anchor="se", padx=5, pady=5, ipady=2)
        return self.sizegrip

    def create_titlebar(self, title: str, titlebar_layout: str = "pack"):

        self.__frame_title = CTkFrame(self.mainframe, border_width=0, corner_radius=ThemeManager.theme["CTkFrame"]["corner_radius"]/2+2)
        self.__frame_title.pack(fill="x", side="top", padx=2, pady=2)
        self.bind_move(self.__frame_title)

        self.title(title)

        self.maximized = False

        if "CTkCustom" in ThemeManager.theme:
            self.__frame_title._fg_color = ThemeManager.theme["CTkCustom"]["titlebar_color"]
            self.__frame_title._draw()

        self.__label_title = CTkLabel(self.__frame_title, text=title)
        self.__label_title.pack(side="left", anchor="w", padx=10, pady=5)
        self.bind_move(self.__label_title)

        self.__button_close = CTkButton(self.__frame_title, text="✕", width=30, height=30,
                                        command=lambda: self.destroy())
        self.__button_close.pack(side="right", anchor="e", padx=5, pady=5)

        self.__button_minimize = CTkButton(self.__frame_title, text="–", width=30, height=30,
                                           command=lambda: self.minimize())
        from sys import platform
        if platform == "win32":
            self.__button_minimize.pack(side="right", anchor="e", padx=5, pady=5)

        if "CTkCustom" in ThemeManager.theme:
            try:
                self.__label_title._text_color = ThemeManager.theme["CTkCustom"]["title_color"]
                self.__label_title._draw()

                self.__button_close._text_color = ThemeManager.theme["CTkCustom"]["closebutton_text_color"]
                self.__button_close._fg_color = ThemeManager.theme["CTkCustom"]["closebutton_color"]
                self.__button_close._hover_color = ThemeManager.theme["CTkCustom"]["closebutton_hover_color"]
                self.__button_close._border_width = ThemeManager.theme["CTkCustom"]["closebutton_border_width"]
                self.__button_close._draw()

                self.__button_minimize._text_color = ThemeManager.theme["CTkCustom"]["minimizebutton_text_color"]
                self.__button_minimize._fg_color = ThemeManager.theme["CTkCustom"]["minimizebutton_color"]
                self.__button_minimize._hover_color = ThemeManager.theme["CTkCustom"]["minimizebutton_hover_color"]
                self.__button_minimize._border_width = ThemeManager.theme["CTkCustom"]["minimizebutton_border_width"]
                self.__button_minimize._draw()
            except:
                pass

        if platform == "linux":
            self.__frame_border.configure(corner_radius=0)

        self.x, self.y = 0, 0

        self.sg_x = 0
        self.sg_y = 0
        self.sg_width = 0
        self.sg_height = 0

    def hide_titlebar(self):
        self.__frame_title.forget()

    @property
    def titlebar(self):
        return self.__frame_title

    @property
    def titlebar_title(self):
        return self.__label_title

    @property
    def titlebar_closebutton(self):
        return self.__button_close

    @property
    def titlebar_minimizebutton(self):
        return self.__button_minimize

    def _click(self, event):
        import warnings

        warnings.warn(
            '请不要使用此方法'
            '请使用bind_move',
            DeprecationWarning,
            stacklevel=2,
        )

        self.x, self.y = event.x, event.y

    def _move(self, event):
        import warnings

        warnings.warn(
            '请不要使用此方法'
            '请使用bind_move',
            DeprecationWarning,
            stacklevel=2,
        )

        new_x = (event.x - self.x) + self.winfo_x()
        new_y = (event.y - self.y) + self.winfo_y()
        if new_y <= -self.__frame_title.winfo_height()+5:
            new_y = -self.__frame_title.winfo_height()+5
        s = f"+{new_x}+{new_y}"
        self.geometry(s)


class CTkCustomToplevel(CTkCustom, CTkToplevel):
    pass


if __name__ == '__main__':
    root = CTkCustom()
    root.title("helloworld")
    root.titlebar_title.configure(text="helloworld")

    root.mainloop()
