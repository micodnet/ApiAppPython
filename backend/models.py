from pydantic import BaseModel

class Note(BaseModel):
    titre: str
    contenu: str
