from typing import List
from pydantic import BaseModel
class CookieData(BaseModel):
    today_game: bool
    date: str
    try_number: int
    played: int
    games_win: int

    @classmethod
    def get_object_from_string(cls, string):
        lista=string.split(" ")
        today_game = bool(lista[0].split("=")[1])
        date = lista[1].split("=")[1]
        try_number = int(lista[2].split("=")[1])
        played = int(lista[3].split("=")[1])
        games_win = int(lista[4].split("=")[1])
        return CookieData(today_game=today_game,date=date,try_number=try_number,played=played,games_win=games_win)
    
    def __str__(self):
        return f"today_game={self.today_game} date={self.date} try_number={self.try_number} played={self.played} games_win={self.games_win}"