import tkinter
from tkinter import ttk
import tkinter.filedialog
from pathlib import Path
from random import randint
from enum import Enum
from extensions.color import Color, extract_rgb_color

def config_progressbar(progressbar: ttk.Progressbar, current: int, total: int) -> None:
    progressbar.configure(value=(current/total) * 100)
    progressbar.update()

def search_directory() -> str:
    directory = tkinter.filedialog.askdirectory()
    if directory == "":
        directory = str(Path.home() / "Downloads")
    return directory


class ColorComponent(Enum):
    TEXT_COLOR = "text_color"
    BG_COLOR = "bg_color"
    FG_COLOR = "fg_color"
    BORDER_COLOR = "border_color"


class ColorIncrementNature(Enum):
    RGB_ADD = "constant"
    RAINBOW = "rainbow"


"""
Une classe qui fait le lien entre une couleur et un widget
On peut définir et utiliser cette classe de 2 manières :
 - En la définissant "toute seule", c'est-à-dire la définir, puis la relier à un widget (elle n'appartiendra pas alors au widget)
 - En la définissant exclusivement pour le widget (c'est à dire en ne précisant pas le master et le widget dans __init__ (plus bas), puis une fois le widget définit, on met cette classe dans l'argument du widget). Elle appartient alors exclusivement au widget
"""

class ColorManager:
    def __init__(self, color_class: Color, component: ColorComponent, increment_nature: ColorIncrementNature, rgb_increment: int, master=None, widget=None, update_duration: int=100):
        self.master = master
        self.widget = widget
        self.color_class = color_class
        self.increment_nature = increment_nature
        self.rgb_increment = rgb_increment
        self.component = component
        self.update_duration = update_duration # Si la durée entre chaque mise à jour est trop petite, la fenêtre n'actualisera pas
        if self.update_duration < 2:
            print(f"[ColorManager][__init__.py] (Low Warning) : Too fast widget update (= 1 update / {self.update_duration} ms) could result in tkinter window freezing")
        self.is_running = False

    def update_widget_color(self):
        """ Update la couleur du widget à celle que possède la classe actuellement """
        hex_color = self.color_class.get_hex()
        self.widget.configure(**{self.component.value: hex_color})
    
    def toggle(self):
        if not self.is_running:
            self.start()
            return
        
        self.stop()
    
    def set_master(self, master_arg):
        self.master = master_arg
    
    def set_widget(self, widget_arg):
        self.widget = widget_arg
        
    def start(self):
        self.is_running = True
        self.color_change_loop()
    
    def stop(self):
        self.is_running = False
    
    def inverse_rgb_increment(self):
        r, g, b = self.rgb_increment
        self.rgb_increment = (-r, -g, -b)
    
    def set_rgb_increment(self, rgb_increment):
        self.rgb_increment = rgb_increment
    
    def set_class_color(self, color: tuple[int, int, int]):
        self.color_class.rgb = extract_rgb_color(color)
    
    def set_component_color(self, color):
        """ Update la couleur du widget arbitrairement """
        self.set_class_color(color)
        self.update_widget_color()
    
    def color_change_loop(self):
        if not self.is_running:
            return
        
        if self.increment_nature == ColorIncrementNature.RGB_ADD:
            self.color_class.rgb_increment(self.rgb_increment)
        if self.increment_nature == ColorIncrementNature.RAINBOW:
            self.color_class.rgb_rainbow_increment(self.rgb_increment)

        self.update_widget_color()
        self.master.after(self.update_duration, self.color_change_loop)