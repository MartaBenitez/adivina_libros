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
        encontrado=False
        lista_titulos = disponibles.copy()
        while encontrado is False:
            if len(lista_titulos)==0:
                raise FileNotFoundError("No se ha encontrado una frase")
            index = random.choice(range(len(lista_titulos)))
            titulo = lista_titulos[index]
            lista_titulos.pop(index)
            info, encontrado=self.get_book_info(titulo)
        self.title=titulo
        return info
    
    def check_response(self,rsp) -> bool:
        if(self.title == rsp.lower()):
            return True
        return False

    def search_title(self,rsp) -> List[str]:
        titulos = self.get_titles_available()
        respuesta=rsp.lower()
        return list(filter(lambda title: respuesta in title,titulos))
        
    def get_titles(self) -> BookTitles:
        with open("app/data/book_titles.json", 'r') as file:
            datos_json = json.load(file)
            libros = BookTitles(**datos_json)
            return libros
    
    def get_titles_available(self) -> List[str]:
        return self.titles.available
    
    def get_book_info(self, title):
        param=title.replace(" ","+")
        url=f'{url_api}search.json?q={param}'
        with urlopen(url) as response:
            if(response.status==200):
                body = response.read()
                datos_json = json.loads(body)
                if "docs" not in datos_json:
                    return [None,False]
                libro = datos_json["docs"][0]
                if "first_sentence" not in libro:
                    return [None,False]
                frase=libro["first_sentence"][0]
                if "author_name" not in libro:
                    return [None,False]
                autor=libro["author_name"][0]
                daily_sentence=DailySentence(sentence=frase,title=title,author=autor)     
                return [daily_sentence,True]
            elif(response.status==404):
                return [None,False]
            else:
                 raise ConnectionError("Error en la peticion")