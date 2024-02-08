import datetime
from domain.cookie_data import CookieData

class CookiesRepository():

    def check_cookie(self, request) -> bool:
        if 'adivina_libros' in request.cookies:
            return True
        return False

    def update_cookie_correct(self, request) -> str:
        if self.check_cookie(request):
            cookie=self.decrypt_cookie(request.cookies["adivina_libros"])
            obj_cookie=CookieData.get_object_from_string(cookie)
            obj_cookie.played+=1
            obj_cookie.today_game=True
            obj_cookie.games_win+=1
            obj_cookie.try_number=1
            return self.encrypt_cookie(str(obj_cookie))
        else:
            return self.generate_cookie()

    def update_cookie_incorrect(self, request) -> str:
        if self.check_cookie(request):
            cookie=self.decrypt_cookie(request.cookies["adivina_libros"])
            obj_cookie=CookieData.get_object_from_string(cookie)
            obj_cookie.try_number+=1
            if obj_cookie.try_number>5:
                obj_cookie.today_game=True
                obj_cookie.played+=1
            return self.encrypt_cookie(str(obj_cookie))
        else:
            return self.generate_cookie()

    def update_cookie_try_number(self, request) -> str:
        cookie=self.decrypt_cookie(request.cookies["adivina_libros"])
        obj_cookie=CookieData.get_object_from_string(cookie)
        obj_cookie.try_number=1
        return self.encrypt_cookie(str(obj_cookie))

    def generate_cookie(self) -> str:
        date = (datetime.datetime.now()).strftime("%d/%m/%Y")
        obj_cookie=CookieData(today_game=False,date=date,try_number=1,played=0,games_win=0)
        return self.encrypt_cookie(str(obj_cookie))
    
    def encrypt_cookie(self, cookie) -> str:
        result = ""
        s = 7
        for i in range(len(cookie)):
            char = cookie[i]
            if (char.isdigit() or char.isspace() or char == "'" or char == "_" or char == "=" or char == "/"):
                result += char
            elif (char.isupper()):
                result += chr((ord(char) + s - 65) % 26 + 65)
            else:
                result += chr((ord(char) + s - 97) % 26 + 97)
        return result

    def decrypt_cookie(self, cookie) -> str:
        result = ""
        s = 7
        for i in range(len(cookie)):
            char = cookie[i]
            if (char.isdigit() or char.isspace() or char == "'" or char == "_" or char == "=" or char == "/"):
                result += char
            elif (char.isupper()):
                result += chr((ord(char) - s - 65) % 26 + 65)
            else:
                result += chr((ord(char) - s - 97) % 26 + 97)
        return result
    
    def check_today_done(self,request) -> bool:
        cookie=self.decrypt_cookie(request.cookies["adivina_libros"])
        obj_cookie=CookieData.get_object_from_string(cookie)
        date = (datetime.datetime.now()).strftime("%d/%m/%Y")
        if (obj_cookie.today_game and obj_cookie.date == date):
            return True
        return False
    

    def check_try_number(self, request) -> bool:
        cookie=self.decrypt_cookie(request.cookies["adivina_libros"])
        obj_cookie=CookieData.get_object_from_string(cookie)
        if (obj_cookie.try_number > 5):
            return False
        return True
    
