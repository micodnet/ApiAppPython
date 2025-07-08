@echo off
title 🚀 Lancement de l'API FastAPI

echo.
echo ▶️ Activation de l'environnement virtuel...
call venv\Scripts\activate

echo.
echo ⚙️ Initialisation de la base de données...
python init_db.py

echo.
echo 🚀 Lancement du serveur...
start http://localhost:8000
uvicorn server:app --reload

pause

