from tkinter import Tk, Button, Label, Entry, Frame, LEFT, RIGHT, TOP, BOTTOM, messagebox, PhotoImage, ttk, Toplevel, Canvas
from sys import exit as sysexit
from os import startfile


couleur_claire = "green2"
couleur_surlignage = "darkgreen"
couleur_foncee = "black"
bouton_background_couleur = "#001000"


def fermeture_fenetre():
    if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter ?"):
        sysexit()


def creer_fen(nom: str = "Nom à changer", background_color: str = couleur_foncee, fen_toplevel=False) -> Tk:
    """
    Créer et stylise une fenêtre tkinter

    :param nom: "Titre" de la fenêtre
    :param background_color: Couleur de fond
    :param fen_toplevel: Si la fenêtre doit être au-dessus d'une fenêtre déjà présente
    :return: Objet fenêtre tkinter
    """
    if fen_toplevel:
        fen = Toplevel(fen_toplevel)
    else:
        fen = Tk()
    fen.title(nom)
    fen.configure(bg=background_color)
    fen.protocol("WM_DELETE_WINDOW", fermeture_fenetre)
    """
    try:
        fen.iconphoto(True, PhotoImage(r"C:/Users\Eleve\Youtube_Downlader\yt.png"))
    except Exception as e:
        print(e, type(e))
    """
    return fen


class Surlignage(Button):
    def __init__(self, master=None, appuye=False, **kw):
        super().__init__(master, **kw)  # Initialisation de la classe parente

        # Configuration des couleurs du bouton
        self.configure(bg=bouton_background_couleur,
                       fg=couleur_claire,
                       activebackground=couleur_claire,
                       activeforeground=couleur_foncee
                       )

        # activebackground et foreground uniquement quand le bouton est pressé

        if appuye:
            # permet de relier le cliquage du bouton à un changement de couleur permanent
            # + pas de surlignage
            self.bouton_desappuye()
        else:
            # si paramètre "appuye" pas défini, on se comporte normalement (pas de changement de couleur quand cliqué)

            # <- "event" créé "erreur minime" dans Pycharm
            # Donc on utilise "lambda event", bien que - visibilité
            self.bind("<Enter>", lambda event: self.curseur_entree())
            self.bind("<Leave>", lambda event: self.curseur_sortie())
        #self.pack(padx=1, pady=1) # laisser de la marge pour la bordure (frame)


    def curseur_entree(self):
        self.configure(bg=couleur_surlignage)

    def curseur_sortie(self):
        self.configure(bg=bouton_background_couleur)

    def bouton_desappuye(self):
        self.bind("<Enter>", lambda event: self.curseur_entree())
        self.bind("<Leave>", lambda event: self.curseur_sortie())
        # remettre le bouton à sa couleur d'origine
        self.configure(bg=bouton_background_couleur, fg=couleur_claire)
        self.bind("<Button-1>", lambda event: self.bouton_appuye()) # ou lambda event: self.bouton_appuye()

    def bouton_appuye(self):
        self.unbind("<Enter>")
        self.unbind("<Leave>")
        self.configure(bg=couleur_claire, fg=couleur_foncee) # Couleurs qui "flashent"
        self.bind("<Button-1>", lambda event: self.bouton_desappuye())


class LabelStyle(Label):
    def __init__(self, master, **kw):
        Label.__init__(self, master=master, **kw)
        self.configure(bg=couleur_foncee, fg=couleur_claire, borderwidth=2)

class EntryStyle(Entry):
    def __init__(self, master, **kw):
        Entry.__init__(self, master, **kw)
        self.configure(bg=couleur_foncee, fg=couleur_claire, insertbackground=couleur_claire)
        self.pack(padx=1, pady=1)  # laisser de la marge pour la bordure (frame)

class ProgressbarStyle(ttk.Progressbar):
    def __init__(self, master, **kw):
        ttk.Progressbar.__init__(self, master=master, **kw)

        style_barre_de_chargement = ttk.Style()
        style_barre_de_chargement.theme_use("clam")  # Configure la barre horizontale avec le style "clam"
        style_barre_de_chargement.configure("Horizontal.TProgressbar",
                                            background=couleur_claire,
                                            troughcolor=couleur_foncee,
                                            bordercolor="green",
                                            lightcolor="lightgreen",
                                            darkcolor="darkgreen")

        self.configure(orient="horizontal", length=200, mode="determinate", maximum=100)


def fen_erreur(message) -> None:
    """ Fenêtre multitâche quand une erreur apparaît """

    fen = creer_fen("Yt Downloader - Erreur")

    div = Frame(fen, bg=couleur_foncee)
    div.pack(padx=60, pady=30)

    label_erreur = LabelStyle(div, text=message)
    label_erreur.pack(pady=20)

    frame = Frame(div, bg=couleur_claire)
    frame.pack(padx=10, pady=10)
    btn_erreur = Surlignage(frame, text="Quitter", command=sysexit, padx=40, pady=20)
    btn_erreur.pack(padx=1, pady=1)

    fen.mainloop()


def fen_fin(path, error) -> None:
    """ Fenêtre à la fin du téléchargement """
    global loc_chemin_dossier
    loc_chemin_dossier = path

    fen = creer_fen("Yt Downloader - Terminé")

    main_div = Frame(fen, bg=couleur_foncee)
    main_div.pack(padx=20, pady=20)

    label_termine = LabelStyle(main_div, text=f"Téléchargement terminé !\n"
                                              f"Nombre d'erreurs : {error}")
    label_termine.grid(row=0, column=0)

    def quitter():
        sysexit()

    def refaire():
        import main_file
        fen.destroy()
        main_file.main()

    def explore_files():
        startfile(loc_chemin_dossier)

    div = Frame(main_div, bg=couleur_foncee)
    div.grid(row=1, column=0)

    frame = Frame(div, bg=couleur_claire)
    frame.pack(side=LEFT, padx=10, pady=10)
    btn_refaire = Surlignage(frame, text="Quitter", padx=20, pady=20, command=quitter)
    btn_refaire.pack(padx=1, pady=1)

    frame = Frame(div, bg=couleur_claire)
    frame.pack(side=LEFT, padx=10, pady=10)
    btn_quitter = Surlignage(frame, text="Refaire", padx=20, pady=20, command=refaire)
    btn_quitter.pack(padx=1, pady=1)

    frame = Frame(main_div, bg=couleur_claire)
    frame.grid(row=2, column=0)
    btn_fichiers = Surlignage(frame, text="Fichiers", padx=40, pady=5, command=explore_files)
    btn_fichiers.grid(padx=1, pady=1)

    fen.mainloop()

def print_dims(fen):
    print(f"{fen.winfo_toplevel().title()}: {fen.winfo_width()}x{fen.winfo_height()}\n")
