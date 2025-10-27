@echo off
echo Installation du système de gestion pédagogique...
echo.

echo Création de l'environnement virtuel...
python -m venv venv
call venv\Scripts\activate

echo Installation des dépendances...
pip install -r requirements.txt

echo.
echo ✅ Installation terminée !
echo.
echo Pour démarrer l'application :
echo 1. Activer l'environnement : venv\Scripts\activate
echo 2. Lancer : python app.py
echo 3. Ouvrir : http://localhost:5000
echo.
pause
