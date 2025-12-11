"""
Lanceur d'Application Desktop - Gestion Enseignement Mr Koffi Elise
Lance l'application Flask et ouvre automatiquement le navigateur.
"""
import os
import sys
import webbrowser
import time
from threading import Timer
from pathlib import Path

# Ajouter le répertoire courant au path Python
sys.path.insert(0, str(Path(__file__).parent))

def ouvrir_navigateur():
    """Ouvre le navigateur après un court délai."""
    time.sleep(1.5)
    webbrowser.open('http://127.0.0.1:5000')

def main():
    """Lance l'application."""
    # Définir les variables d'environnement pour le mode portable
    os.environ['ENVIRONNEMENT_FLASK'] = 'portable'
    os.environ['UTILISER_SQLITE'] = 'true'
    
    print("=" * 60)
    print("  GESTION ENSEIGNEMENT - MR KOFFI ELISE")
    print("  Application Desktop - Version Portable")
    print("=" * 60)
    print()
    print("Démarrage de l'application...")
    print("L'application s'ouvrira automatiquement dans votre navigateur.")
    print()
    print("Pour arrêter l'application, fermez cette fenêtre ou appuyez sur Ctrl+C")
    print()
    
    # Ouvrir le navigateur après un délai
    Timer(1.0, ouvrir_navigateur).start()
    
    # Importer et lancer Flask
    from app import app
    app.run(host='127.0.0.1', port=5000, debug=False)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nApplication arrêtée.")
        sys.exit(0)