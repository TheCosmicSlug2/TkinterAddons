import addons_base
import search
import startup
import download_config
from sys import exit as sysexit
import calculs
import download_process


if not startup.connexion_check():
    sysexit()


def main() -> None:
    """ Fonction principale du programme """

    url_or_search = startup.url_or_search()

    if url_or_search == "URL":
        dic_config = download_config.url_config()
        liste_yt_objets = calculs.return_liste_yt_object(dic_config["data"], dic_config["url"])

    else:
        terme_recherche = search.ask_search_fen()
        liste_yt_objets = search.display_miniatures(terme_recherche)
        dic_config = download_config.search_config()

    erreurs = download_process.main_download_process(liste_yt_objets, dic_config)

    addons_base.fen_fin(dic_config["chemin"], erreurs)


if __name__ == "__main__":
    main()



# Ajouter fenêtre qui s'affiche au milieu de l'écran