from addons_base import *
from requests import get
from requests.exceptions import ConnectionError


def connexion_check() -> bool:
    """ Checke la connextion internet de l'utilisateur """

    dummy_dic = {"connexion": False}


    def internet_connexion() -> bool:
        """ Ici se passe le check : renvoie True ou False """
        try:
            get("https://youtube.com", timeout=5)
            dummy_dic["connexion"] = True
            fen_connexion_check.destroy()
            return True
        except ConnectionError:
            print("Non connecté à Internet")
            return False


    fen_connexion_check = creer_fen("Youtube Downloader - Vérification de la connexion")

    label_connexion_check = LabelStyle(fen_connexion_check,
                                       text="Vérification de la connexion internet\n...",
                                       padx=30, pady=30)
    label_connexion_check.grid(row=0, column=0)

    # Ne pas montrer le bouton dès sa création (on checke la connexion d'abord)
    frame = Frame(fen_connexion_check, bg=couleur_claire)
    bouton_connection_erreur = Surlignage(frame,
                                          text="Revérifier",
                                          command=internet_connexion, padx=30, pady=10)
    bouton_connection_erreur.pack(padx=1, pady=1)
    fen_connexion_check.update()


    def connexion_erreur() -> None:
        """ Fenêtre quand la connexion est pas suffisante """
        fen_connexion_check.title("Yt Downloader - Erreur connection")
        label_connexion_check.configure(text=f"Erreur : pas ou peu assez de connection internet \n"
                                             f"veuillez la revérifier")

        frame.grid(row=1, column=0, pady=20) # Ici on montre la frame

        fen_connexion_check.mainloop()

    if not internet_connexion():
        connexion_erreur() # Boucle jusqu'à la bonne connexion

    print("Connecté à Internet")

    return dummy_dic["connexion"]



def url_or_search() -> str:
    """ Permet à l'user de choisir entre téléchargement par url ou par recherche directe """

    fen_url_or_search = creer_fen("Url ou recherche")

    dummy_dic = {"url_or_search": ""} # On peut pas utiliser de variable...

    def return_url() -> None:
        fen_url_or_search.destroy()
        dummy_dic["url_or_search"] = "URL"


    def return_search() -> None:
        fen_url_or_search.destroy()
        dummy_dic["url_or_search"] = "SEARCH"


    frame = Frame(fen_url_or_search, bg=couleur_claire)
    frame.grid(row=0, column=0, padx=20, pady=20)
    btn_url = Surlignage(frame, text="URL", command=return_url, padx=35, pady=20)
    btn_url.pack(padx=1, pady=1)

    frame = Frame(fen_url_or_search, bg=couleur_claire)
    frame.grid(row=0, column=1, padx=20, pady=20)
    btn_search = Surlignage(frame, text="Recherche", command=return_search, padx=20, pady=20)
    btn_search.pack(padx=1, pady=1)


    fen_url_or_search.mainloop()
    return dummy_dic["url_or_search"]
