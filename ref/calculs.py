from pytube import YouTube, Playlist
from addons_base import fen_erreur
from requests import get
from io import BytesIO
from PIL import Image


def return_liste_yt_object(data: str, url: str) -> list:
    """ Transforme l'url d'une vidéo ou d'une playlist en liste d'objects Youtube """

    liste_yt_objects = []

    if data == "video": # Trouver l'ID de la vidéo
        try:
            yt_object = YouTube(url)
            liste_yt_objects.append(yt_object) # ici
        except Exception as exception_rencontree:
            print(f"{__file__} : L'erreur suivante s'est produite dans la conversion de la vidéo en objet YouTube : "
                  f"{exception_rencontree}")
            fen_erreur(f"Erreur lors de la conversion de l'url :\n\n"
                       f"Voir cmd pour précisions")

    if data == "playlist":  # Compter le nombre d'éléments, pour afficher la progression
        try:
            yt_object_playlist = Playlist(url) # Trouver l'ID de la playlist
            for yt_object in yt_object_playlist:
                liste_yt_objects.append((YouTube(yt_object))) # Créer une liste des objets yt de la playlist
        except Exception as exception_rencontree:
            print(f"{__file__} : L'erreur suivante s'est produite dans la conversion de la playlist en objet YouTube : "
                  f"{exception_rencontree}")
            fen_erreur(f"Erreur lors de la conversion de l'url :\n\n"
                       f"Voir cmd pour précisions")

    print(f"Liste des ID : {liste_yt_objects}\n"
          f"Nombre de vidéos : {len(liste_yt_objects)}")

    return liste_yt_objects


def itag_data(yt_object, data_type, qualite) -> int:
    """ Cherche les itags correspondant à la qualité demandé par l'user """

    def ajouter_itag_au_dictionnaire(loc_stream):  # juste pour les only_video et only_audio, pas pour les "vraies" vidéos

        stream_str = str(loc_stream)
        # exemple avec un stream :
        # <Stream: itag="136" mime_type="video/mp4" res="720p" fps="30fps" vcodec="avc1.4d401f" progressive="False"
        # type="video">

        stream_list = list(stream_str.split())
        # stream list : ['<Stream:', 'itag="136"', 'mime_type="video/mp4"', 'res="720p"', 'fps="30fps"',
        # 'vcodec="avc1.4d401f"', 'progressive="False"', 'type="video">']

        stream_itag_raw = stream_list[1]
        # stream itag str : itag="136"

        stream_itag_nb = int("".join([char for char in stream_itag_raw if char.isdigit()]))
        # stream itag_nb : 136

        stream_res_raw = stream_list[3]  # Que ce soit pour les sons ou les images,
        # le string où seront situées les infos de la résolution sonore et de l'image
        # sera toujours situé à l'index 3
        # stream data str : res="720p"

        stream_res_nb = int("".join([char for char in stream_res_raw if char.isdigit()]))
        # stream data nb : 720

        dict_itags[str(stream_itag_nb)] = stream_res_nb  # ajoute l'itag suivi de la résolution sonore ou visuelle
        # dict itags : {'136': 720}

        return dict_itags

    dict_itags = {}

    if data_type == "image":
        for stream in yt_object.streams.filter(adaptive=True, only_video=True):
            ajouter_itag_au_dictionnaire(stream)
    if data_type == "son":
        for stream in yt_object.streams.filter(adaptive=True, only_audio=True):
            ajouter_itag_au_dictionnaire(stream)

    sorted_itags = dict(sorted(dict_itags.items(), key=lambda item: item[1]))
    sorted_itags = [value for value in sorted_itags]

    if qualite == "bd":
        itag = sorted_itags[0]
    else: # qualite == "hd"
        itag = sorted_itags[-1]

    print(f"itag retenu {qualite}: {itag}")
    return itag



def trouve_longueur(mot: str, dic: dict) -> int:
    """ Renvoie la largeur "à l'écran" d'un mot en fonction d'un dictionnaire de référence """
    longueur = 0
    for char in mot:
        try:
            longueur += dic[char]
        except:
            print(end=f"\"{char}\" ")
            longueur += 10.0 # Longueur arbitraire (mais représente largeur moyenne, je crois)
    return longueur


def change_longueur(mot: str, longueur_initiale: int) -> str:
    """ Change la longueur d'un string """
    mot_change = mot
    if longueur_initiale > 700:  # si la largeur > 700 px
    # Enlever ce qu'il faut pour arriver à 50 caractères
        longueur_enlevee = len(mot_change) - (len(mot_change) - 50)
        mot_change = mot_change[:longueur_enlevee] + "..."
        longueur_initiale -= longueur_enlevee * 10 # enlève la longueur des caractères en trop + *10 (longueur caractère moyenne)

    while longueur_initiale <= 700:
        mot_change += " "
        longueur_initiale += 5.0
    return mot_change


def charger_images_depuis_url(url_image: str) -> Image:
    """ Retrouve l'image située à l'url """
    reponse = get(url_image)
    if reponse.status_code == 200:
        data_image = BytesIO(reponse.content)
        image = Image.open(data_image)
        return image
    else:
        print(
            f"Échec du chargement de l'image depuis l'URL {url_image}. Code d'état HTTP : {reponse.status_code}")
        return None


def process_vues(url: YouTube) -> int: # Prend le nombre de vues, et le convertit en k, M ou Md comme sur YouTube
    """ Transforme les vues de la vidéo yt en "format youtube" (k, M et B) """
    nb_vues = url.views
    if nb_vues < 1_000:
        vues_changees = nb_vues
    elif nb_vues < 10_000:
        vues_changees = round(nb_vues / 1_000, 1)
        if vues_changees - int(vues_changees) == 0: # checke s'il y a uniquement un 0 après la virgule (ex : 2.0 k)
            vues_changees = int(vues_changees) # Supprime ce 0
        vues_changees = str(vues_changees) + " k"
    elif nb_vues < 1_000_000:
        vues_changees = str(nb_vues // 1_000) + " k"
    elif nb_vues < 10_000_000:
        vues_changees = round(nb_vues / 1_000_000, 1)
        if vues_changees - int(vues_changees) == 0: # idem
            vues_changees = int(vues_changees) # idem
        vues_changees = str(vues_changees) + " M"
    elif nb_vues < 1_000_000_000:
        vues_changees = str(nb_vues // 1_000_000) + " M"
    else:
        vues_changees = str(nb_vues // 1_000_000_000) + " Md"

    return vues_changees
