from pydantic import BaseModel

class BookInfo(BaseModel):
    sentence: str
    title: str
    author: str
    publish_year: int
    character: str
    place: str
    