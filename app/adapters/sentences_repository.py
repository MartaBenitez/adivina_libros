from typing import List
import json
import random
import os
from urllib.request import urlopen

from domain.book_titles import BookTitles
from domain.daily_sentence import DailySentence

url_api=os.environ.get("URL_OPENLIBRARY_API")

class InMemorySentencesRepository():
    def __init__(self):
        self.titles=self.get_titles()
        self.title=""

    def get_sentence(self) -> DailySentence:
        disponibles = self.get_titles_available()
        index = random.choice(range(len(disponibles)))
        titulo = disponibles[index]
        info=self.get_book_info(titulo)
        self.title=titulo
        return info
    
    def check_response(self,rsp) -> bool:
        if(self.title == rsp.lower()):
            return True
        return False

    def get_titles(self) -> BookTitles:
        with open("app/data/book_titles.json", 'r') as file:
            datos_json = json.load(file)
            libros = BookTitles(**datos_json)
            return libros
    
    def get_titles_available(self) -> List[str]:
        return self.titles.available
    
    def get_book_info(self, title) -> DailySentence:
        param=title.replace(" ","+")
        url=f'{url_api}search.json?q={param}'
        with urlopen(url) as response:
            if(response.status==200):
                body = response.read()
                datos_json = json.loads(body)
                libro = datos_json["docs"][0]
                frase=libro["first_sentence"][0]
                autor=libro["author_name"][0]
                daily_sentence=DailySentence(sentence=frase,title=title,author=autor)     
                return daily_sentence
            else:
                 raise ConnectionError("Error en la peticion")