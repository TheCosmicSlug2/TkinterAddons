"""
Simplifier l'ajout de nouvelles fonctionnalités dans des widjets tkinter ou ctkinter
"""

import tkinter as tk
import customtkinter as ctk


class ButtonObjet(ctk.CTkButton):
    def __init__(self, master, need_toggling: bool = False, color_managers: dict = {}, **kw):
        super().__init__(master, **kw)
        self.clicked = False
        self.need_toggling = need_toggling
        self.bg_clicked = ""
        self.bg_not_clicked = ""

        # Initialisation des managers
        for color_manager_name, color_manager in color_managers.items():
            setattr(self, color_manager_name, color_manager)
            color_manager.set_master(self.master)
            color_manager.set_widget(self)
        self.color_managers = color_managers


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



    
     

