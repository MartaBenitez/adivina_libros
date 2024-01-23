from pydantic import BaseModel

class DailySentence(BaseModel):
    sentence: str
    title: str
    author: str