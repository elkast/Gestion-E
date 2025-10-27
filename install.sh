#!/bin/bash
echo "Installation du système de gestion pédagogique..."
echo

echo "Création de l'environnement virtuel..."
python3 -m venv venv
source venv/bin/activate

echo "Installation des dépendances..."
pip install -r requirements.txt

echo
echo "✅ Installation terminée !"
echo
echo "Pour démarrer l'application :"
echo "1. Activer l'environnement : source venv/bin/activate"
echo "2. Lancer : python app.py"
echo "3. Ouvrir : http://localhost:5000"
