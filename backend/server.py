from curl_cffi import Session
from fastapi import Depends, FastAPI, HTTPException, Request, Form, Body
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse, StreamingResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
#from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi import status
from fastapi import UploadFile, File
from datetime import datetime
import shutil
import sqlite3
import os
from init_db import init_db
from models import Note
from api_router import get_note, router as api_router
#from pathlib import Path
import json
import csv
import io
import logging

app = FastAPI(
    title="📘 Mon API Personnalisée: 📚 Mes Notes",
    description="API FastAPI pour gérer mes notes: créer, modifier et supprimer",
    version="1.0.0",
    openapi_tags=[
        {"name": "Notes", "description": "Endpoints pour gérer les notes (CRUD) formulaire html"},
        {"name": "API Notes", "description": "Accès JSON pour React ou Postman"},
        {"name": "Admin", "description": "Fonctions administratives (si il y as), docs personalisées"}
    ],
    contact={
        "name": "Micodnet",
        "email": "verminnenmichael@gmail.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    #docs_url=None,     # Désactive Swagger par défaut
    #redoc_url=None      # Désactive Redoc aussi
)

# Générer openapi.json à chaque lancement
# @app.on_event("startup")
# def write_openapi_json():
#     openapi_schema = get_openapi(
#         title=app.title,
#         version=app.version,
#         description=app.description,
#         routes=app.routes,
#     )
#     Path("openapi.json").write_text(json.dumps(openapi_schema, indent=2, ensure_ascii=False))

# --------------------------
# 📁 Dossiers templates/static
# --------------------------
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# --------------------------
# 🗃️ Initialisation de la base de données
# --------------------------
DB_PATH = "database.db"
init_db()

# Autoriser les requêtes depuis React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ou 5173 pour Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Une erreur est survenue. Vérifie les logs."}
    )

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Nouvelle requête : {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Réponse : {response.status_code}")
    return response

# status de l'api pour le frontend
@app.get("/status", tags=["Admin"])
def health_check():
    return {"status": "✅ API opérationnelle"}

@app.get("/export/csv", tags=["Admin"])
def export_csv():
    conn = get_db_connection()
    notes = conn.execute("SELECT * FROM notes").fetchall()
    conn.close()

    filename = f"export_notes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    filepath = os.path.join("exports", filename)

    os.makedirs("exports", exist_ok=True)
    with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["id", "titre", "contenu"])
        writer.writeheader()
        for note in notes:
            writer.writerow(dict(note))

    return FileResponse(path=filepath, filename=filename, media_type="text/csv")

@app.get("/export/json", tags=["Admin"])
def export_json():
    conn = get_db_connection()
    notes = conn.execute("SELECT * FROM notes").fetchall()
    conn.close()

    filename = f"export_notes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = os.path.join("exports", filename)

    os.makedirs("exports", exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as jsonfile:
        json.dump([dict(note) for note in notes], jsonfile, ensure_ascii=False, indent=2)

    return FileResponse(path=filepath, filename=filename, media_type="application/json")

# 📤 Import CSV
@app.post("/import/csv", tags=["Admin"])
async def import_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        return {"error": "Le fichier doit être un CSV"}

    contents = await file.read()
    decoded = contents.decode("utf-8").splitlines()
    
    reader = csv.DictReader(decoded)
    notes = [row for row in reader if row.get("titre") and row.get("contenu")]

    conn = get_db_connection()
    for note in notes:
        conn.execute("INSERT INTO notes (titre, contenu) VALUES (?, ?)", (note["titre"], note["contenu"]))
    conn.commit()
    conn.close()

    return {"message": f"{len(notes)} notes importées depuis CSV ✅ avec succès."}


# 📤 Import JSON
@app.post("/import/json", tags=["Admin"])
async def import_json(file: UploadFile = File(...)):
    if not file.filename.endswith(".json"):
        return {"error": "Le fichier doit être un JSON"}

    contents = await file.read()
    try:
        data = json.loads(contents)
    except Exception as e:
        return {"error": f"Erreur JSON : {str(e)}"}

    if not isinstance(data, list):
        return {"error": "Le fichier JSON doit contenir une liste de notes."}

    notes = [note for note in data if note.get("titre") and note.get("contenu")]

    conn = get_db_connection()
    for note in notes:
        conn.execute("INSERT INTO notes (titre, contenu) VALUES (?, ?)", (note["titre"], note["contenu"]))
    conn.commit()
    conn.close()

    return {"message": f"{len(notes)} notes importées avec succès."}
    
# 🆕 Route HTML
# --------------------------
# 🏠 Page d'accueil HTML
# --------------------------
@app.get("/", response_class=HTMLResponse, tags=["Notes"])
def read_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/notes", tags=["Notes"])
def read_notes():
    conn = get_db_connection()
    notes = conn.execute("SELECT * FROM notes").fetchall()
    conn.close()
    return [dict(note) for note in notes]

# --------------------------
# 📄 Affichage des notes
# --------------------------
@app.get("/affichage", response_class=HTMLResponse, tags=["Notes"])
def affichage_notes(request: Request):
    conn = get_db_connection()
    notes = conn.execute("SELECT * FROM notes").fetchall()
    conn.close()
    return templates.TemplateResponse("affichage_server.html", {"request": request, "notes": notes})

# --------------------------
# ➕ Ajouter une note (form HTML)
# --------------------------
# 🆕 Route POST pour ajouter une note
@app.post("/ajouter-note", tags=["Notes"])
def ajouter_note(titre: str = Form(...), contenu: str = Form(...)):
    conn = get_db_connection()
    conn.execute("INSERT INTO notes (titre, contenu) VALUES (?, ?)", (titre, contenu))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/affichage", status_code=303)

# --------------------------
# 🗑️ Supprimer une note
# --------------------------
@app.post("/supprimer-note", tags=["Notes"])
def supprimer_note(note_id: int = Form(...)):
    conn = get_db_connection()
    conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/affichage", status_code=303)


@app.get("/modifier-note/{note_id}", response_class=HTMLResponse, tags=["Notes"])
def formulaire_modifier(request: Request, note_id: int):
    conn = get_db_connection()
    note = conn.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
    conn.close()
    return templates.TemplateResponse("modifier.html", {"request": request, "note": note})

@app.post("/modifier-note", tags=["Notes"])
def modifier_note(note_id: int = Form(...), titre: str = Form(...), contenu: str = Form(...)):
    conn = get_db_connection()
    conn.execute("UPDATE notes SET titre = ?, contenu = ? WHERE id = ?", (titre, contenu, note_id))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/affichage", status_code=303)

@app.get("/importer", response_class=HTMLResponse, tags=["Admin"])
def page_import(request: Request):
    return templates.TemplateResponse("import.html", {"request": request})

@app.get("/redoc", include_in_schema=False, tags=["Admin"])
async def custom_redoc():
    return get_redoc_html(
        openapi_url="/openapi.json",
        title="🧾 Documentation ReDoc",
        redoc_favicon_url="/static/logo.png"
    )

# Route custom /docs
@app.get("/docs", include_in_schema=False, tags=["Admin"])
async def custom_docs():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="📘 Documentation Personnalisée",
        swagger_favicon_url="/static/logo.png",
        #swagger_css_url="/static/swagger-overrides.css", # css personnalisée
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css"
    )

# route api pour requetes js les autres pour les formulaires
@app.post("/api/notes", tags=["Notes"])
def create_note(note: Note):
    try:
        conn = get_db_connection()
        conn.execute("INSERT INTO notes (titre, contenu) VALUES (?, ?)", (note.titre, note.contenu))
        conn.commit()
        conn.close()
        return {"message": "Note créée avec succès"}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

# Pour des notes paginées
@app.get("/api/notes", tags=["Notes"])
def get_notes(skip: int = 0, limit: int = 10):
    conn = get_db_connection()
    notes = conn.execute("SELECT * FROM notes LIMIT ? OFFSET ?", (limit, skip)).fetchall()
    conn.close()
    return [dict(note) for note in notes]

@app.post("/api/modifier-note", tags=["API"])
def modifier_note_api(data: dict = Body(...)):
    note_id = data.get("note_id")
    titre = data.get("titre")
    contenu = data.get("contenu")
    conn = get_db_connection()
    conn.execute("UPDATE notes SET titre = ?, contenu = ? WHERE id = ?", (titre, contenu, note_id))
    conn.commit()
    conn.close()
    return {"message": "Note modifiée avec succès"}

# Cacher une route
@app.get("/secret", include_in_schema=False)
def route_cachee():
    return {"msg": "Tu ne devrais pas voir ça dans la doc 😄"}

# Inclure API JSON
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)



# cd backend
# python init_db.py
# uvicorn main:app --reload
# L’API est disponible sur http://localhost:8000/notes