from addons_base import *
from PIL import ImageTk
import largeur_caracteres
from calculs import trouve_longueur, change_longueur, charger_images_depuis_url, process_vues
from pytube import Search


def ask_search_fen() -> str:
    """ Fenêtre pour obtenir le terme de recherche de l'user """
    global search_term  # obligé
    search_term = ""

    fen = creer_fen("Yt Downloader - Rechercher 1")

    div_main = Frame(fen, bg=couleur_foncee)
    div_main.pack(padx=20, pady=20)

    label = LabelStyle(div_main, text="Saisissez une recherche")
    label.pack(pady=5)


    def get_terme_recherche() -> None:
        """ Retourne la valeur présente dans l'entry """
        global search_term  # obligé
        entry_value = entry.get()
        if not (entry_value.isspace() or entry_value == ""):
            search_term = entry_value
            fen.destroy()


    frame = Frame(div_main, bg=couleur_claire)
    frame.pack(pady=5)
    entry = EntryStyle(frame)
    entry.pack()

    entry.bind("<Return>", lambda event: get_terme_recherche())

    fen.mainloop()

    return search_term



def display_miniatures(terme_recherche) -> list:
    """ Fenêtre où les miniatures sont crées """

    dic_char_largeur = largeur_caracteres.chars_largeur

    fen_display_miniatures = creer_fen("Yt Downloader - Résultats de la recherche")
    fen_display_miniatures.geometry("1000x500")

    fen_progress_miniatures = creer_fen("Yt Downloader - Recherche")
    fen_progress_miniatures.attributes('-topmost', 'true')

    div_main = Frame(fen_progress_miniatures, bg=couleur_foncee)
    div_main.pack(padx=20, pady=20)

    label_recherche = LabelStyle(div_main, text="Recherche des résultats\n"
                                                             "-------------------"
                                                             "\nVeuillez patienter")
    label_recherche.pack()

    fen_progress_miniatures.update()


    def get_youtube_results(recherche) -> list:
        """ Obtenir les résulats yt (API) avec un terme de recherche """
        get_result = Search(recherche)
        resultats_recherche = get_result.results
        return resultats_recherche


    liste_resultats_recherche = get_youtube_results(recherche=terme_recherche)

    label_recherche.configure(text="Décodage des urls / Formatage des résultats\n"
                                     "-------------------\n"
                                     "Veuillez patienter")

    barre_chargement_resultats = ProgressbarStyle(div_main)
    barre_chargement_resultats.pack(pady=5)


    def creer_scrollable_frame(master) -> Frame:
        """ Créer une frame scrollable """

        loc_canvas = Canvas(master,
                        borderwidth=0, highlightbackground=couleur_foncee, background=couleur_foncee)
        loc_frame = Frame(loc_canvas,
                      background=couleur_foncee)
        style = ttk.Style()
        style.theme_use('classic')
        style.configure("Vertical.TScrollbar", troughcolor=couleur_claire, background=couleur_foncee)

        scrollbar = ttk.Scrollbar(master,
                                  orient="vertical", command=loc_canvas.yview, style="Vertical.TScrollbar")
        loc_canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill="y")
        loc_canvas.pack(side=LEFT, fill="both", expand=True)
        loc_canvas.create_window((0, 0), window=loc_frame, anchor="nw")

        loc_frame.bind("<Configure>", lambda event, canvas=loc_canvas: on_frame_configure(loc_canvas))

        return loc_frame


    def on_frame_configure(canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))


    # Créer un cadre ("frame") scrollable
    scrollable_frame = creer_scrollable_frame(fen_display_miniatures)

    liste_yt_objets = []


    def ajouter_ou_supprimer_a_liste(texte_bouton) -> None:
        """ Ajoute ou retire des yt-object de la liste à télécharger """
        if texte_bouton in liste_yt_objets:
            liste_yt_objets.remove(texte_bouton)
        else:
            liste_yt_objets.append(texte_bouton)


    def update_avancement_miniatures(avancement_actuel, nb_total) -> None:
        """ Update la barre de chargement des miniatures """
        barre_chargement_resultats.configure(value=(avancement_actuel/nb_total)*100)
        barre_chargement_resultats.update() # <- ça update aussi la main window, malheureusement


    dimensions_constante = 10 # constante pour la taille des miniatures
    print(f"Caractères non reconnus :", end=" ")

    for videoID in liste_resultats_recherche:
        # Titre_video est le "nom" du bouton
        titre_video = videoID.title

        len_titre_affiche = trouve_longueur(titre_video, dic_char_largeur)

        titre_video = change_longueur(titre_video, len_titre_affiche)

        # Les vues sont changées ici
        nb_vues_video = process_vues(videoID)

        # Auteur de la vidéo
        auteur = videoID.author

        # Retrouve l'url de l'image à partir de l'ID de la vidéo
        url_image = videoID.thumbnail_url
        image = charger_images_depuis_url(url_image)

        # Change les dimensions de l'image
        image = image.resize((16 * dimensions_constante, 9 * dimensions_constante))  # Adjust size as needed

        # Convertit image PIl en image Tkinter
        tk_image = ImageTk.PhotoImage(image)

        # Créer la Frame dans laquelle sera comprise le bouton
        button_frame = Frame(scrollable_frame,
                             highlightbackground=couleur_claire, background=couleur_foncee,
                             highlightthickness=1)
        button_frame.pack(side=TOP, fill="x", pady=3)



        # Créer le bouton avec tous les éléments dedans (l'image n'est pas encore mise)
        bouton_miniature = Surlignage(button_frame,
                                             appuye=1,  # si appuye : changer de couleur
                                             text=f"   {titre_video}"
                                                  f"   {nb_vues_video} vues\n\n"
                                                  f"   ~ {auteur} ~",
                                             image=tk_image, compound=LEFT, anchor="w",
                                             command=lambda txt=videoID: ajouter_ou_supprimer_a_liste(txt), width=750)
        # Ici l'image est mise
        bouton_miniature.image = tk_image
        bouton_miniature.pack(pady=5)

        # Update les valeurs que prendra la barre de chargement
        avancement_res = liste_resultats_recherche.index(videoID) + 1 # index de la vidéo dans la liste + 1
        nb_total_res = len(liste_resultats_recherche)
        # Update la barre de chargement des miniatures avec les nouvelles valeurs
        update_avancement_miniatures(avancement_res, nb_total_res)


    div_droite = Frame(fen_display_miniatures, bg=couleur_foncee)
    div_droite.pack(side=RIGHT)

    frame = Frame(div_droite, bg=couleur_claire)
    frame.pack(side=TOP, pady=20, padx=10)
    bouton_nouvelle_recherche = Surlignage(frame,
                                                  text="Relancer \n une recherche ?",
                                                  padx=20,
                                                  command=lambda: [fen_display_miniatures.destroy(),
                                                            ask_search_fen()])
    bouton_nouvelle_recherche.pack(padx=1, pady=1)


    def telecharger() -> None:
        """ Quand le bouton "télécharger" est cliqué """
        if len(liste_yt_objets) != 0:
            fen_display_miniatures.destroy()
            print(f"liste des ID : {liste_yt_objets}")


    frame = Frame(div_droite, bg=couleur_claire)
    frame.pack(side=TOP, pady=20, padx=10)
    bouton_telecharger = Surlignage(frame,
                                           text="Téléchargement ==>",
                                           padx= 16,
                                           command=telecharger)
    bouton_telecharger.pack(padx=1, pady=1)

    fen_progress_miniatures.destroy()

    fen_display_miniatures.mainloop()

    return liste_yt_objets
