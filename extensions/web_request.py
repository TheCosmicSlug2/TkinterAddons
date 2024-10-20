import PIL.Image
import requests
import pytube
import PIL
import io

class InternetRequests:
    def __init__(self):
        self.website_url = "https://youtube.com"
        self.max_timeout = 5

    def test_connexion(self) -> bool:
        """ Teste la connexion de l'utilisateur à un site Internet """
        try:
            requests.get(
                url=self.website_url, 
                timeout=self.max_timeout
            )
            return True
        except ConnectionError:
            return False
    
    def is_user_connected(self) -> bool:
        return self.test_connexion()
    
    @staticmethod
    def get_search_results(search_term: str) -> list:
        result_object = pytube.Search(search_term)
        results = result_object.results
        return results
    
    @staticmethod
    def get_image_from_url(image_url: str) -> PIL.Image:
        reponse_object = requests.get()
        if reponse_object.status_code != 200:
            print(f"Échec du chargement de l'image depuis l'URL {image_url}. Code d'état HTTP : {reponse_object.status_code}")
        image_data = io.BytesIO(reponse_object.content)
        image = PIL.Image.open(image_data)
        return image
    
    @staticmethod
    def get_yt_object(yt_url: str) -> pytube.YouTube:
        return pytube.YouTube(yt_url)
    
    @staticmethod
    def get_playlist_object(playlist_url: str) -> pytube.Playlist:
        return pytube.Playlist(playlist_url)
    
    @staticmethod
    def get_lowest_resolution(yt_object: pytube.YouTube):
        return yt_object.stream.get_lowest_resolution()

    @staticmethod
    def get_highest_resolution(yt_object: pytube.YouTube):
        return yt_object.stream.get_highest_resolution()

    def get_video_stream(self, yt_object: pytube.YouTube, quality: str):
        if quality == "low":
            return self.get_lowest_resolution(yt_object)
        return self.get_highest_resolution(yt_object)

    def download_stream(yt_stream: pytube.YouTube, path: str):
        return yt_stream.download(path)