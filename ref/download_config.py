from tkinter import filedialog
from addons_base import *
from pathlib import Path

def url_config() -> dict:
    """ Configuration par l'user des données qu'il veut télécharger avec url """

    dic_download_config = {"data":"", "data_type":"", "qualite":"", "extension":"", "chemin":"", "url":""}

    main_fen = creer_fen("Youtube Downloader - Configuration", couleur_foncee)

    # Grande Frame pour les background
    div_main = Frame(main_fen, bg="black")
    div_main.pack(padx=20, pady=20)


    """ 
    Playlist ou vidéo
    """
    div_data = Frame(div_main, bg=couleur_foncee)
    div_data.grid(row=0, column=0, padx=20, pady=20)


    def get_data_video() -> None:
        btn_data_playlist.bouton_desappuye()
        label_url.configure(text="Url de la vidéo ?") # Change le label de l'url en f() du choix
        dic_download_config["data"] = "video"


    def get_data_playlist() -> None:
        btn_data_video.bouton_desappuye()
        label_url.configure(text="Url de la playlist ?")
        dic_download_config["data"] = "playlist"


    frame = Frame(div_data, bg=couleur_claire)
    frame.pack(side=LEFT, padx=10, pady=10)
    btn_data_video = Surlignage(frame, text="Vidéo", appuye=True, padx=20, pady=20, command=get_data_video)
    btn_data_video.pack(padx=1, pady=1)

    frame = Frame(div_data, bg=couleur_claire)
    frame.pack(side=LEFT, padx=10, pady=10)
    btn_data_playlist = Surlignage(frame, text="Playlist", appuye=True, padx=20, pady=20, command=get_data_playlist)
    btn_data_playlist.pack(padx=1, pady=1)


    """ 
    Image, Audio ou vidéo
    """
    div_data_type = Frame(div_main,  bg=couleur_foncee)
    div_data_type.grid(row=1, column=0, padx=20, pady=20)

    div_data_type_1 = Frame(div_data_type, bg=couleur_foncee)
    div_data_type_1.pack(side=TOP)

    div_data_type_2 = Frame(div_data_type, bg=couleur_foncee)
    div_data_type_2.pack(side=BOTTOM)


    def get_data_type_image() -> None:
        btn_data_type_audio.bouton_desappuye()
        btn_data_type_video.bouton_desappuye()
        dic_download_config["data_type"] = "image"
        combo_extension.configure(values=[".mp4", ".avi", ".mkv", ".webm", ".mov",
                                       ".mp3", ".m4a", ".flac", ".wav", ".wma", ".aac"]) # ouais je sais ça marche pas comme ça
        combo_extension.set(combo_extension["values"][0])


    def get_data_type_audio() -> None:
        btn_data_type_image.bouton_desappuye()
        btn_data_type_video.bouton_desappuye()
        dic_download_config["data_type"] = "audio"
        combo_extension.configure(values=[".mp3", ".m4a", ".flac", ".wav", ".wma", ".aac"])
        combo_extension.set(combo_extension["values"][0])


    def get_data_type_video() -> None:
        btn_data_type_image.bouton_desappuye()
        btn_data_type_audio.bouton_desappuye()
        dic_download_config["data_type"] = "video"
        combo_extension.configure(values=[".mp4", ".avi", ".mkv", ".webm", ".mov",
                                          ".mp3", ".m4a", ".flac", ".wav", ".wma", ".aac"])
        combo_extension.set(combo_extension["values"][0])


    frame = Frame(div_data_type_1, bg=couleur_claire)
    frame.pack(side=LEFT, padx=10, pady=10)
    btn_data_type_image = Surlignage(frame, text="Image", appuye=True, padx=20, pady=20, command=get_data_type_image)
    btn_data_type_image.pack(padx=1, pady=1)

    frame = Frame(div_data_type_1, bg=couleur_claire)
    frame.pack(side=LEFT, padx=10, pady=10)
    btn_data_type_audio = Surlignage(frame, text="Audio", appuye=True, padx=20, pady=20, command=get_data_type_audio)
    btn_data_type_audio.pack(padx=1, pady=1)

    frame = Frame(div_data_type_2, bg=couleur_claire)
    frame.pack(padx=10, pady=10)
    btn_data_type_video = Surlignage(frame, text="Vidéo", appuye=True, padx=20, pady=20, command=get_data_type_video)
    btn_data_type_video.pack(padx=1, pady=1)


    """ 
    Qualité
    """
    div_qualite = Frame(div_main, bg=couleur_foncee)
    div_qualite.grid(row=2, column=0, padx=20, pady=20)


    def get_bd() -> None:
        btn_hd.bouton_desappuye()
        dic_download_config["qualite"] = "bd"


    def get_hd() -> None:
        btn_bd.bouton_desappuye()
        dic_download_config["qualite"] = "hd"


    frame = Frame(div_qualite, bg=couleur_claire)
    frame.pack(side=LEFT, padx=10, pady=10)
    btn_bd = Surlignage(frame, text="BD", appuye=True, padx=20, pady=20, command=get_bd)
    btn_bd.pack(padx=1, pady=1)

    frame = Frame(div_qualite, bg=couleur_claire)
    frame.pack(side=LEFT, padx=10, pady=10)
    btn_hd = Surlignage(frame, text="HD", appuye=True, padx=20, pady=20, command=get_hd)
    btn_hd.pack(padx=1, pady=1)


    """ 
    Extension
    """
    div_extension = Frame(div_main, bg=couleur_foncee)
    div_extension.grid(row=0, column=1, padx=20, pady=20)

    label_extension = LabelStyle(div_extension, text="Extension ?")
    label_extension.pack(padx=10, pady=10)

    combo_extension = ttk.Combobox(div_extension, values=[".mp3", ".mp4"])
    combo_extension.pack(padx=10, pady=10)


    """ 
    Chemin de téléchargement
    """
    div_path = Frame(div_main, bg=couleur_foncee)
    div_path.grid(row=1, column=1, padx=20, pady=20)

    div_chemin_base = Frame(div_path, bg=couleur_foncee)
    div_chemin_base.pack(padx=10, pady=10)

    label_chemin_base_1 = LabelStyle(div_chemin_base, text="Chemin :")
    label_chemin_base_1.pack(side=LEFT)

    label_chemin_base_2 = LabelStyle(div_chemin_base, text=str(Path.home() / "Downloads"))
    label_chemin_base_2.pack(side=LEFT)


    def chercher_repertoire() -> None:
        text = filedialog.askdirectory()
        if text == "": # Parfois un bug où la recherche renvoie un string vide
            text = str(Path.home() / "Downloads")
        label_chemin_base_2.configure(text=text)


    frame = Frame(div_path, bg=couleur_claire)
    frame.pack(padx=10, pady=10)
    btn_chercher_chemin = Surlignage(frame, text="Chercher", command=chercher_repertoire)
    btn_chercher_chemin.pack(padx=1, pady=1)

    label_dossier_arrive = LabelStyle(div_path, text="Dossier d'arrivée :")
    label_dossier_arrive.pack(padx=10, pady=10)

    frame = Frame(div_path, bg=couleur_claire)
    frame.pack(padx=10, pady=10)
    entry_dossier_arrive = EntryStyle(frame)

    """
    Url
    """
    div_url = Frame(div_main, bg=couleur_foncee)
    div_url.grid(row=2, column=1, padx=20, pady=20)

    label_url = LabelStyle(div_url, text="Url de la vidéo / Playlist : ")
    label_url.pack(padx=10, pady=10)

    frame = Frame(div_url, bg=couleur_claire)
    frame.pack(padx=10, pady=10)
    entry_url = EntryStyle(frame)

    """
    Télécharger
    """
    div_telecharger = Frame(div_main, bg=couleur_foncee)
    div_telecharger.grid(row=1, column=2, padx=20, pady=20)


    def get_dic() -> None:
        """ Gère la relation entre le dictionnaire et les valeurs demandées par l'user """
        dic_download_config["extension"] = combo_extension.get()
        dic_download_config["chemin"] = label_chemin_base_2["text"] + "/" + entry_dossier_arrive.get()
        dic_download_config["url"] = entry_url.get()

        for key in list(dic_download_config.keys()):
            if dic_download_config[key] == "":
                label_erreur.configure(text=f"\"{key}\" non déclarée")
                return
        main_fen.destroy()


    frame = Frame(div_telecharger, bg=couleur_claire)
    frame.pack(padx=10, pady=10)
    btn_telecharger = Surlignage(frame, text="=> Télécharger", padx=20, pady=10, command=get_dic)
    btn_telecharger.pack(padx=1, pady=1)

    label_erreur = LabelStyle(div_telecharger)
    label_erreur.pack(pady=10)

    main_fen.mainloop()

    return dic_download_config



def search_config() -> dict:
    """ Configuration par l'user des données qu'il veut télécharger avec recherche """

    dic_download_config = {"data_type":"", "qualite":"", "extension":"", "chemin":""}

    main_fen = creer_fen("Youtube Downloader - Configuration", couleur_foncee)

    # Grande Frame pour les background
    div_main = Frame(main_fen, bg="black")
    div_main.pack(padx=20, pady=20)

    """ 
    Image, Audio ou vidéo
    """
    div_data_type = Frame(div_main,  bg=couleur_foncee)
    div_data_type.grid(row=0, column=0, padx=20, pady=20)

    div_data_type_1 = Frame(div_data_type, bg=couleur_foncee)
    div_data_type_1.pack(side=TOP)

    div_data_type_2 = Frame(div_data_type, bg=couleur_foncee)
    div_data_type_2.pack(side=BOTTOM)


    def get_data_type_image():
        btn_data_type_audio.bouton_desappuye()
        btn_data_type_video.bouton_desappuye()
        dic_download_config["data_type"] = "image"
        combo_extension.configure(values=[".mp4", ".avi", ".mkv", ".webm", ".mov",
                                       ".mp3", ".m4a", ".flac", ".wav", ".wma", ".aac"]) # ouais je sais ça marche pas comme ça
        combo_extension.set(combo_extension["values"][0])


    def get_data_type_audio():
        btn_data_type_image.bouton_desappuye()
        btn_data_type_video.bouton_desappuye()
        dic_download_config["data_type"] = "audio"
        combo_extension.configure(values=[".mp3", ".m4a", ".flac", ".wav", ".wma", ".aac"])
        combo_extension.set(combo_extension["values"][0])


    def get_data_type_video():
        btn_data_type_image.bouton_desappuye()
        btn_data_type_audio.bouton_desappuye()
        dic_download_config["data_type"] = "video"
        combo_extension.configure(values=[".mp4", ".avi", ".mkv", ".webm", ".mov",
                                          ".mp3", ".m4a", ".flac", ".wav", ".wma", ".aac"])
        combo_extension.set(combo_extension["values"][0])


    frame = Frame(div_data_type_1, bg=couleur_claire)
    frame.pack(side=LEFT, padx=10, pady=10)
    btn_data_type_image = Surlignage(frame, text="Image", appuye=True, padx=20, pady=20, command=get_data_type_image)
    btn_data_type_image.pack(padx=1, pady=1)

    frame = Frame(div_data_type_1, bg=couleur_claire)
    frame.pack(side=LEFT, padx=10, pady=10)
    btn_data_type_audio = Surlignage(frame, text="Audio", appuye=True, padx=20, pady=20, command=get_data_type_audio)
    btn_data_type_audio.pack(padx=1, pady=1)

    frame = Frame(div_data_type_2, bg=couleur_claire)
    frame.pack(padx=10, pady=10)
    btn_data_type_video = Surlignage(frame, text="Vidéo", appuye=True, padx=20, pady=20, command=get_data_type_video)
    btn_data_type_video.pack(padx=1, pady=1)


    """ 
    Qualité
    """
    div_qualite = Frame(div_main, bg=couleur_foncee)
    div_qualite.grid(row=1, column=0, padx=20, pady=20)


    def get_bd():
        btn_hd.bouton_desappuye()
        dic_download_config["qualite"] = "bd"


    def get_hd():
        btn_bd.bouton_desappuye()
        dic_download_config["qualite"] = "hd"


    frame = Frame(div_qualite, bg=couleur_claire)
    frame.pack(side=LEFT, padx=10, pady=10)
    btn_bd = Surlignage(frame, text="BD", appuye=True, padx=20, pady=20, command=get_bd)
    btn_bd.pack(padx=1, pady=1)

    frame = Frame(div_qualite, bg=couleur_claire)
    frame.pack(side=LEFT, padx=10, pady=10)
    btn_hd = Surlignage(frame, text="HD", appuye=True, padx=20, pady=20, command=get_hd)
    btn_hd.pack(padx=1, pady=1)

    """ 
    Chemin de téléchargement
    """
    div_path = Frame(div_main, bg=couleur_foncee)
    div_path.grid(row=0, column=1, padx=20, pady=20)

    div_chemin_base = Frame(div_path, bg=couleur_foncee)
    div_chemin_base.pack(padx=10, pady=10)

    label_chemin_base_1 = LabelStyle(div_chemin_base, text="Chemin :")
    label_chemin_base_1.pack(side=LEFT)

    label_chemin_base_2 = LabelStyle(div_chemin_base, text=str(Path.home() / "Downloads"))
    label_chemin_base_2.pack(side=LEFT)


    def chercher_repertoire() -> None:
        """ Ouvre l'explorateur de fichier pour rechercher un chemin """
        text = filedialog.askdirectory()
        if text == "": # Parfois un bug où la recherche renvoie un string vide
            text = str(Path.home() / "Downloads")
        label_chemin_base_2.configure(text=text)


    frame = Frame(div_path, bg=couleur_claire)
    frame.pack(padx=10, pady=10)
    btn_chercher_chemin = Surlignage(frame, text="Chercher", command=chercher_repertoire)
    btn_chercher_chemin.pack(padx=1, pady=1)

    label_dossier_arrive = LabelStyle(div_path, text="Dossier d'arrivée :")
    label_dossier_arrive.pack(padx=10, pady=10)

    frame = Frame(div_path, bg=couleur_claire)
    frame.pack(padx=10, pady=10)
    entry_dossier_arrive = EntryStyle(frame)


    """ 
    Extension
    """
    div_extension = Frame(div_main, bg=couleur_foncee)
    div_extension.grid(row=1, column=1, padx=20, pady=20)

    label_extension = LabelStyle(div_extension, text="Extension ?")
    label_extension.pack(padx=10, pady=10)

    combo_extension = ttk.Combobox(div_extension, values=[".mp3", ".mp4"])
    combo_extension.pack(padx=10, pady=10)


    """
    Télécharger
    """
    div_telecharger = Frame(div_main, bg=couleur_foncee)
    div_telecharger.grid(row=0, column=2, padx=20, pady=20)


    def get_dic() -> None:
        """ Focntion qui gère la relation entre le contenu des boutons et le dictionnaire """
        dic_download_config["extension"] = combo_extension.get()
        dic_download_config["chemin"] = label_chemin_base_2["text"] + "/" + entry_dossier_arrive.get()

        for key in list(dic_download_config.keys()):
            if dic_download_config[key] == "":
                label_erreur.configure(text=f"\"{key}\" non déclarée")
                return
        main_fen.destroy()

    frame = Frame(div_telecharger, bg=couleur_claire)
    frame.pack(padx=10, pady=10)
    btn_telecharger = Surlignage(frame, text="=> Télécharger", padx=20, pady=10, command=get_dic)
    btn_telecharger.pack(padx=1, pady=1)

    label_erreur = LabelStyle(div_telecharger)
    label_erreur.pack(pady=10)


    main_fen.mainloop()

    return dic_download_config
