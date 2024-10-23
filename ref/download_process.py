from time import process_time as cpu_clock_time
from os import path, rename
from pytube.exceptions import AgeRestrictedError, VideoUnavailable
from calculs import itag_data
from addons_base import *


def main_download_process(liste_objects, dic_config) -> int:
    """ Télécharge toutes les vidéos d'une liste """

    def download_yt_object(loc_yt_object, dic) -> int:
        """ Télécharge une vidéo """

        titre_video = loc_yt_object.title  # <- titre_video sert à configurer "xxxx" est en train d'être téléchargée
        label_extraction.configure(text=f"Extraction de : \"{titre_video}\"")
        loc_yt_object.register_on_progress_callback(download_callback)

        try:  # Au cas où téléchargement impossible
            if dic["data_type"] == "image" or dic["data_type"] == "son":  # extraire juste l'image ou le son
                print(yt_object, dic["data_type"], dic["qualite"])
                stream_a_telecharger = loc_yt_object.streams.get_by_itag(
                    itag_data(yt_object=loc_yt_object, data_type=dic["data_type"], qualite=dic["qualite"])
                )

            else:  # Data_type == "vidéo"
                if dic["qualite"] == "ld":
                    stream_a_telecharger = loc_yt_object.streams.get_lowest_resolution()
                else:  # Qualite == "hd"
                    stream_a_telecharger = loc_yt_object.streams.get_highest_resolution()

            fichier_sortie = stream_a_telecharger.download(output_path=dic["chemin"])
            base, ext = path.splitext(fichier_sortie)

            fichier_final = base + dic["extension"]  # Télécharge avec l'extension choisie

            rename(fichier_sortie, fichier_final)

        # Exceptions durant le téléchargement

        except AgeRestrictedError:
            label_erreur.configure(text=f"\"{titre_video}\"\n"
                                        f"n'est pas téléchargeable (âge restreint)")
            label_erreur.pack()
            print(f"Erreur : \"{titre_video}\" : âge restreint")

            return 1 # Retourne 1 erreur (ajouter le nombre d'erreurs)


        except VideoUnavailable:
            label_erreur.configure(text=f"\"{titre_video}\"\n"
                                        f"n'est pas trouvable (url fausse ou vidéo supprimée)")
            label_erreur.pack()
            print(f"Erreur : \"{titre_video}\" : vidéo non trouvable")

            return 1

        except Exception as exception_rencontree:
            label_erreur.configure(text=f"\"{titre_video}\" : \n"
                                        f"une erreur s'est produite durant le téléchargement\n"
                                        f"voir cmd pour précisions")
            label_erreur.pack()

            print(f"Erreur : {titre_video} : {exception_rencontree}")

            return 1

        print(f"\"{titre_video}\" a été téléchargé !")

        return 0



    len_yt_objects = len(liste_objects)

    fen_download = creer_fen("Téléchargement")

    div_main = Frame(fen_download, bg=couleur_foncee)
    div_main.pack(padx=50, pady=20)

    label_extraction = LabelStyle(div_main,
                                  text="Extraction de : ",
                                  pady=20)
    label_extraction.pack()

    # Barre de compléation (avancement des vidéos)

    div_completion = Frame(div_main, bg=couleur_foncee)
    div_completion.pack(pady=20)

    barre_de_completion = ProgressbarStyle(div_completion)
    barre_de_completion.pack(side=LEFT)

    label_completion = LabelStyle(div_completion, text=f"(0/{len_yt_objects})")
    label_completion.pack(side=LEFT, padx=10)

    # Barre de progression

    div_progress = Frame(div_main, bg=couleur_foncee)
    div_progress.pack(pady=20)

    barre_de_progression = ProgressbarStyle(div_progress)
    barre_de_progression.pack(side=LEFT)

    label_progression = LabelStyle(div_progress, text="0,0 %")
    label_progression.pack(side=LEFT, padx=10)


    # Label "temps restant : " + "vitesse : "
    label_temps_restant = LabelStyle(div_main, text="Temps restant : ")
    label_temps_restant.pack()

    label_erreur = LabelStyle(div_main)
    label_erreur.pack(pady=10)


    def montrer_details():
        label_infos.pack(side=RIGHT)
        bouton_montrer_ou_cacher_infos.configure(text="Cacher détails",
                                                 command=cacher_details)

    def cacher_details():
        label_infos.pack_forget()
        bouton_montrer_ou_cacher_infos.configure(text="Montrer détails",
                                                 command=montrer_details)

    div_infos = Frame(fen_download, bg=couleur_foncee)
    div_infos.pack(pady=30)

    frame = Frame(div_infos, bg=couleur_claire)
    frame.pack(side=LEFT, padx=20)
    bouton_montrer_ou_cacher_infos = Surlignage(frame)
    bouton_montrer_ou_cacher_infos.pack(padx=1, pady=1)

    label_infos = LabelStyle(div_infos)
    label_infos.pack(side=RIGHT)

    cacher_details()


    def download_callback(stream, chunk, bytes_remaining) -> None:
        """ Fonction appelée durant le téléchargement d'une vidéo """
        """ "Chunk" : paramètre obligatoire même si pas utilisé (par défaut : 9 MB) """
        seconds_since_download_start = cpu_clock_time() - start_time
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = round(bytes_downloaded / total_size * 100, 1)
        speed = round(((bytes_downloaded / 1024) / 1024) / seconds_since_download_start, 2) # en MB/s
        seconds_left = round(((bytes_remaining / 1024) / 1024) / float(speed))

        # Update les infos

        label_progression.configure(text=f"{percentage_of_completion} %")
        barre_de_progression.configure(value=percentage_of_completion)
        label_temps_restant.configure(text=f"temps restant : {seconds_left} secondes \n"
                                           f"({speed} Mo/s)")
        label_infos.configure(text=f"Total : {round(total_size / 1048576)} Mo \n"  # 1048576 = 1024 * 1024
                                   f"Téléchargé : {bytes_downloaded / 1048576} Mo \n"
                                   f"Restant : {round(bytes_remaining / 1048576)} Mo \n"
                                   f"Pourcentage : {percentage_of_completion} % \n"
                                   f"Secondes depuis début : {round(seconds_since_download_start)} secondes\n"
                                   f"Vitesse : {speed} Mo/s\n"
                                   f"Secondes restantes : {seconds_left} secondes")
        fen_download.update()


    def data_update(idx: int, total: int) -> None:
        """ Update les labels et la barre de progression à la fin de téléchargement d'une vidéo """

        barre_de_progression.configure(value=0)
        label_progression.configure(text=f"0.0%")

        barre_de_completion.configure(value=round(idx/total*100, 2))
        label_completion.configure(text=f"({idx}/{total})")

        fen_download.update()


    data_update(0, len_yt_objects)
    global start_time  # j'ai maaal
    start_time = cpu_clock_time()
    nb_erreurs = 0

    for idx_yt_objet, yt_object in enumerate(liste_objects):
        label_erreur.pack_forget()
        nb_erreurs += download_yt_object(loc_yt_object=yt_object, dic=dic_config)
        data_update(idx_yt_objet+1, len_yt_objects)

    fen_download.destroy()
    return nb_erreurs
