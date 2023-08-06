from customtkinter import CTk, ThemeManager, CTkFrame


class CTkCustomBorder(CTk):
    def __init__(self, advanced: bool = True, client_edge: bool = False, window_edge: bool = False, **kwargs):
        super().__init__(**kwargs)
        from sys import platform
        if advanced:
            if platform == "win32":
                if "CTkCustom" in ThemeManager.theme:
                    self.__transparent_color = ThemeManager.theme["CTkCustom"]["transparent_color"]
                else:
                    self.__transparent_color = "#101010"
                self.attributes("-transparentcolor", self.__transparent_color)
                self.configure(fg_color=self.__transparent_color)
            elif platform == "darwin":
                self.__transparent_color = 'systemTransparent'
                self.attributes("-transparent", True)
                self.configure(fg_color=self.__transparent_color)
            else:
                self.__transparent_color = '#000001'

        self.wm_overrideredirect(True)

        if advanced:
            if platform == "win32":
                from ctypes import windll
                windll.uxtheme
                GWL_EXSTYLE = -20
                WS_EX_APPWINDOW = 0x00040000
                WS_EX_TOOLWINDOW = 0x00000080
                WS_EX_CLIENTEDGE = 0x00000200
                WS_EX_WINDOWEDGE = 0x00000100
                hwnd = windll.user32.GetParent(self.winfo_id())
                style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
                style = style & ~WS_EX_TOOLWINDOW
                style = style | WS_EX_APPWINDOW
                if client_edge:
                    style = style | WS_EX_CLIENTEDGE
                if window_edge:
                    style = style | WS_EX_WINDOWEDGE
                res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
                self.style32 = style
            else:
                try:
                    self.wm_attributes("-topmost", True)
                except:
                    pass

        self.minsize(150, 180)

        self.__frame_border = CTkFrame(self, border_width=1,
                                       background_corner_colors=(
                                           self.__transparent_color,
                                           self.__transparent_color,
                                           self.__transparent_color,
                                           self.__transparent_color
                                       )
                                       )
        self.__frame_border.pack(fill="both", expand=True, padx=0, pady=0)

    @property
    def mainframe(self):
        return self.__frame_border


if __name__ == '__main__':
    CTkCustomBorder().mainloop()