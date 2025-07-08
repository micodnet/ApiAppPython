@echo off
title 🚀 Lancement du Frontend React

echo.
echo ▶️ Passage dans le dossier frontend...
cd frontend

echo.
echo 📦 Vérification des dépendances...
if not exist node_modules (
    echo 📥 Installation des modules NPM...
    npm install
)

echo.
echo 🚀 Lancement du serveur React...
start http://localhost:3000
npm start

pause
