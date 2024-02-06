import datetime
from typing import List
import json
import os
from urllib.request import urlopen

from domain.cookie_data import CookieData
from domain.book_info import BookInfo
from domain.book_titles import BookTitles

url_api=os.environ.get("URL_OPENLIBRARY_API")

class InMemorySentencesRepository():
    def __init__(self):
        self.titles=self.get_titles()
        self.title=""

    def get_sentence(self) -> BookInfo:
        disponibles = self.get_titles_available()
        lista_titulos = disponibles.copy()
        hoy = datetime.datetime.now()
        indice = (hoy.year + hoy.month + hoy.day) % len(lista_titulos)
        titulo = lista_titulos[indice]
        # Escribir titulo en el fichero como usado
        info=self.get_book_info(titulo)
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
    
    def get_book_info(self, titulo):
        param=titulo.replace(" ","+")
        url=f'{url_api}search.json?title={param}'
        with urlopen(url) as response:
            if(response.status==200):
                body = response.read()
                datos_json = json.loads(body)
                if "docs" not in datos_json:
                    return None
                libro = datos_json["docs"][0]
                frase = self.get_first_sentence(libro)
                autor = self.get_author(libro)
                lugar = self.get_place(libro)
                personaje = self.get_character(libro)
                anho = self.get_publish_year(libro)
                daily_sentence=BookInfo(sentence=frase,title=titulo,author=autor,publish_year=anho,character=personaje,place=lugar)
                return daily_sentence
            else:
                 raise ConnectionError("Error en la peticion")
    def get_first_sentence(self,libro) -> str:
        if "first_sentence" not in libro:
            return ""
        return libro["first_sentence"][0]
            
    def get_author(self,libro) -> str:
        if "author_name" not in libro:
            return ""
        return libro["author_name"][0]
    
    def get_place(self,libro) -> str:
        if "place" not in libro:
            return ""
        return libro["place"][0]
        
    def get_character(self, libro) -> str:
        if "person" not in libro:
            return ""
        return libro["person"][0]
    
    def get_publish_year(self, libro) -> int:
        if "first_publish_year" not in libro:
            return 0
        return int(libro["first_publish_year"])
    
    def check_cookie(self, request) -> bool:
        if 'adivina_libros' in request.cookies:
            return True
        return False

    def update_cookie_correct(self, request) -> str:
        if self.check_cookie(request):
            cookie=request.cookies["adivina_libros"]
            obj_cookie=CookieData.get_object_from_string(cookie)
            obj_cookie.played+=1
            obj_cookie.today_game=True
            obj_cookie.games_win+=1
            obj_cookie.try_number=1
            return str(obj_cookie)
        else:
            return self.generate_cookie()

    def update_cookie_incorrect(self, request) -> str:
        if self.check_cookie(request):
            cookie=request.cookies["adivina_libros"]
            obj_cookie=CookieData.get_object_from_string(cookie)
            obj_cookie.try_number+=1
            if obj_cookie.try_number>5:
                obj_cookie.today_game=True
                obj_cookie.played+=1
                obj_cookie.try_number=1
            return str(obj_cookie)
        else:
            return self.generate_cookie()

                
    def generate_cookie(self) -> str:
        obj_cookie=CookieData(today_game=False,try_number=1,played=0,games_win=0)
        return str(obj_cookie)


    


