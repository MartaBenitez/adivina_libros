from typing import List
from pydantic import BaseModel


class BookTitles(BaseModel):
    available: List[str]
    used: List[str]