import sqlite3

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY,
        titre CHAR NOT NULL,
        contenu CHAR NOT NULL
    )
    """)
    cursor.executemany("INSERT INTO notes (titre, contenu) VALUES (?, ?)", [
        ("Note 1", "Contenu de la note 1"),
        ("Note 2", "Encore du contenu ici."),
    ])
    conn.commit()
    conn.close()
    print("Base initialisée !")

if __name__ == "__main__":
    init_db()
