📘 README — Projet FastAPI + SQLAlchemy + React + HTML
🛠️ Prérequis
✅ Python 3.10+ recommandé

✅ pip installé

✅ Node.js (si tu veux lancer le frontend React)

📦 Installation (backend)
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS

pip install -r requirements.txt
Exemple de requirements.txt :

txt
Copier
Modifier
fastapi
uvicorn
jinja2
sqlalchemy
aiofiles
python-multipart

🧱 Structure du projet
/backend
│
├── server.py               # API FastAPI principale
├── api_router.py           # Routes REST JSON
├── models.py               # Modèle Note avec SQLAlchemy
├── database.py             # Connexion DB
├── init_db.py              # Création automatique de la base
├── /templates              # HTML (home, affichage, modifier)
├── /static                 # CSS, images, etc.
├── database.db             # Fichier SQLite généré automatiquement
├── run.bat                 # Script de démarrage auto (Windows)

🚀 Lancer le projet avec le script .bat
Double-clique sur le fichier run.bat ou exécute-le depuis le terminal :

.\run.bat
Il va :

Initialiser la base de données

Lancer le serveur FastAPI sur http://localhost:8000

🌐 Accès à l'application
🏠 http://localhost:8000/ — Page d’accueil HTML

📄 http://localhost:8000/affichage — Liste des notes

➕ Ajout / modification via formulaires HTML

📚 http://localhost:8000/docs — Swagger (API)

🧾 http://localhost:8000/redoc — ReDoc

🧪 Tester l'API (en JSON)
Exemples d'appels API :

GET    /api/notes         → Liste toutes les notes (format JSON)
POST   /api/notes         → Ajoute une note
PUT    /api/notes/{id}    → Modifie une note
DELETE /api/notes/{id}    → Supprime une note

⚙️ Lancer le frontend React

cd frontend
npm install
npm start

🧼 Réinitialiser la base de données (optionnel)

del backend\database.db
python backend\init_db.py
