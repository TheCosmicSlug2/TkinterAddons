import os
from pathlib import Path
import re

class LocalHost:
    def __init__(self):
        pass

    def convert_to_path(path):
        return Path(path)

    @staticmethod
    def folder_path_exist(folder_path: Path):
        if not isinstance(folder_path, Path):
            print("Argument is not of Path Class")
            return
        if not folder_path.exists:
            return False
        return True
        
    @staticmethod
    def check_filename_validity(filemame: str):
        forbidden_chars = r'[<>:"/\\|?*]'
        if re.search(forbidden_chars, filemame):
            return False
        
        if len(filemame) > 255:
            return False
        
        return True
    
    def check_music_filename_validity(self, filename: str):
        if not self.check_filename_validity(filename):
            return False
        
        # Checker les extensions
