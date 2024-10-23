from pathlib import Path
import re


def get_path_object(path: str):
    return Path(path)

def folder_path_exist(folder_path: Path):
    if not isinstance(folder_path, Path):
        print("Argument is not of Path Class")
        return
    if not folder_path.exists:
        return False
    return True

def check_filename_validity(filemame: str):
    forbidden_chars = r'[<>:"/\\|?*]'
    if re.search(forbidden_chars, filemame):
        return False
    
    if len(filemame) > 255:
        return False
    
    return True

def get_yt_view(views: int) -> str:
    """ Transforme les vues de la vidéo YouTube en format abrégé (k, M, Md). """
    suffixes = [(1_000_000_000, "Md"), (1_000_000, "M"), (1_000, "k")]
    
    if views < 1_000:
        return str(views)

    for threshold, suffix in suffixes:
        if views >= threshold:
            vues_changees = round(views / threshold, 1)
            vues_changees = str(int(vues_changees) if vues_changees.is_integer() else vues_changees)
            return vues_changees + " " + suffix

    return str(views)
