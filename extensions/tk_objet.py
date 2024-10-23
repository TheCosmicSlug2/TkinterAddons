"""
Simplifier l'ajout de nouvelles fonctionnalités dans des widjets tkinter ou ctkinter
"""

import tkinter as tk
import customtkinter as ctk


def set_color_managers_attributes(widget: ctk.CTkBaseClass, color_managers: dict):
    for color_manager_name, color_manager in color_managers.items():
        setattr(widget, color_manager_name, color_manager)
        color_manager.set_master(widget.master)
        color_manager.set_widget(widget)
    widget.color_managers = color_managers


class ButtonObjet(ctk.CTkButton):
    def __init__(self, master, need_toggling: bool = False, color_managers: dict = {}, **kw):
        super().__init__(master, **kw)
        self.clicked = False
        self.need_toggling = need_toggling
        self.bg_clicked = ""
        self.bg_not_clicked = ""

        # Initialisation des managers
        set_color_managers_attributes(self, color_managers)

    def set_bg_color(self, color_string):
        self.configure(bg=color_string)
    
    def click_on(self, event):
        self.clicked = True
        self.set_bg_color(self.bg_clicked)
        self.bind("<Button-1>", self.click_off)
    
    def click_off(self, event):
        self.clicked = False
        self.set_bg_color(self.bg_not_clicked)
        self.bind("<Button-1>", self.click_on)

class LabelObject(ctk.CTkLabel):
    def __init__(self, master, color_managers: dict = {}, **kw):
        super().__init__(master, **kw)
        self.master = master
        set_color_managers_attributes(self, color_managers)


class SliderObject(ctk.CTkSlider):
    def __init__(self, master, color_managers: dict = {}, **kw):
        super().__init__(master, **kw)
        self.master = master
        set_color_managers_attributes(self, color_managers)


class CheckboxObject(ctk.CTkCheckBox):
    def __init__(self, master, color_managers: dict = {}, **kw):
        super().__init__(master, **kw)
        set_color_managers_attributes(self, color_managers)


class FrameObject(ctk.CTkFrame):
    def __init__(self, master, color_managers: dict = {}, **kw):
        super().__init__(master, **kw)
        self.master = master
        set_color_managers_attributes(self, color_managers)
    

class ProgressbarObject(ctk.CTkProgressBar):
    def __init__(self, master, total: int, current: int = 0, color_managers: dict = {}, **kw):
        super().__init__(master, **kw)
        self.master = master
        self.current = current
        self.total = total
        set_color_managers_attributes(self, color_managers)
    
    def increment_current(self):
        self.current += 1
    
    def set_current(self, current):
        self.current = current
        self.update()
    
    def update(self):
        self.set(self.current/self.total)