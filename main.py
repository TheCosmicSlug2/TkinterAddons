import cProfile
import customtkinter as ctk
from extensions.tk_object_config import ColorManager, ColorComponent, ColorIncrementNature
from extensions.color import Color
from random import randint
from tkinter import LEFT
from extensions.tk_objet import ButtonObjet


def main():
    # Initialisation de la fenêtre principale
    app = ctk.CTk()  # Utilisation de CTk au lieu de Tk pour une fenêtre stylisée
    app.geometry("400x300")
    app.title("Exemple CustomTkinter")

    # Choisir un thème (clair ou sombre)
    ctk.set_appearance_mode("dark")  # Options: "light" ou "dark"
    ctk.set_default_color_theme("blue")  # Autres options : "green", "dark-blue"

    def on_button_click():
        global clicked
        
        if not clicked:
            clicked = True
            btn_manager.toggle()
            btn_manager2.toggle()
            return
        
    color1 = Color("white")
    color2 = Color("black")
    

    btn_manager = ColorManager(
        color_class=color1,
        component=ColorComponent.FG_COLOR,
        increment_nature=ColorIncrementNature.RGB_ADD,
        rgb_increment=(0, -10, -10)
    )

    btn_manager2 = ColorManager(
        color_class=color2,
        component=ColorComponent.TEXT_COLOR,
        increment_nature=ColorIncrementNature.RAINBOW,
        rgb_increment=10,
        update_duration=10
    )

    button = ButtonObjet(
        master=app,
        color_managers={"fg_manager": btn_manager, "text_manager": btn_manager2}
    )
    button.pack(pady = 10)

    def highlight_start(event):
        button.fg_manager.set_component_color("white")
        button.text_manager.set_component_color("green")
        button.fg_manager.start()
        button.text_manager.start()
    
    def highlight_stop(event):
        button.fg_manager.set_component_color("white")
        button.text_manager.set_component_color("black")
        button.fg_manager.stop()
        button.text_manager.stop()

    button.bind("<Enter>", highlight_start)
    button.bind("<Leave>", highlight_stop)

    global clicked
    clicked = False

    # Ajout d'un slider stylisé
    slider = ctk.CTkSlider(app, from_=0, to=100)
    slider.pack(pady=20)

    # Démarrer la boucle principale
    app.mainloop()


# Utiliser cProfile pour profiler tout le script
if __name__ == "__main__":
    main()
    #cProfile.run('main()', 'basic.prof')

