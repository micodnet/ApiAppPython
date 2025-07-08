from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sqlite3

router = APIRouter(prefix="/api", tags=["API Notes"])

class Note(BaseModel):
    titre: str
    contenu: str

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@router.get("/notes")
def get_notes():
    conn = get_db()
    notes = conn.execute("SELECT * FROM notes").fetchall()
    conn.close()
    return [dict(note) for note in notes]

@router.get("/notes/{note_id}")
def get_note(note_id: int):
    conn = get_db()
    note = conn.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
    conn.close()
    if note is None:
        raise HTTPException(status_code=404, detail="Note non trouvée")
    return dict(note)

@router.post("/notes")
def create_note(note: Note):
    conn = get_db()
    conn.execute("INSERT INTO notes (titre, contenu) VALUES (?, ?)", (note.titre, note.contenu))
    conn.commit()
    conn.close()
    return {"message": "Note ajoutée"}

@router.put("/notes/{note_id}")
def update_note(note_id: int, note: Note):
    conn = get_db()
    conn.execute("UPDATE notes SET titre = ?, contenu = ? WHERE id = ?", (note.titre, note.contenu, note_id))
    conn.commit()
    conn.close()
    return {"message": "Note mise à jour"}

@router.delete("/notes/{note_id}")
def delete_note(note_id: int):
    conn = get_db()
    conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()
    return {"message": "Note supprimée"}
