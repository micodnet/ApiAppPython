import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY,
    titre TEXT,
    contenu TEXT
)
""")

cursor.executemany("INSERT INTO notes (titre, contenu) VALUES (?, ?)", [
    ("Note 1", "Contenu de la note 1"),
    ("Note 2", "Contenu de la note 2"),
])
conn.commit()
conn.close()


# ▶️ Lancer le backend
# bash
# uvicorn main:app --reload