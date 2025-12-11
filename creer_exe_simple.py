"""
Script Python pour créer l'exécutable
Alternative au fichier .bat pour les utilisateurs qui préfèrent Python
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def main():
    print("=" * 60)
    print("  CREATION DE L'EXECUTABLE")
    print("  Gestion Enseignement - Mr Koffi Elise")
    print("=" * 60)
    print()
    
    # Vérifier Python
    print("Vérification de Python...")
    if sys.version_info < (3, 8):
        print("ERREUR: Python 3.8 ou supérieur requis!")
        return 1
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} détecté")
    print()
    
    # Installer PyInstaller
    print("Étape 1/4: Installation de PyInstaller...")
    try:
        # Essayer d'installer normalement
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller", "--upgrade"], 
                      check=True, capture_output=True)
    except subprocess.CalledProcessError:
        # Si échec, essayer avec --user
        try:
            print("Installation avec --user...")
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller", "--user", "--upgrade"], 
                          check=True, capture_output=True)
        except subprocess.CalledProcessError:
            print("⚠️ PyInstaller déjà installé ou erreur de permissions")
            print("Tentative de continuation...")
    print("✓ PyInstaller prêt")
    print()
    
    # Nettoyage
    print("Étape 2/4: Nettoyage des anciens fichiers...")
    for folder in ["build", "dist"]:
        if Path(folder).exists():
            shutil.rmtree(folder)
    if Path("GestionEnseignement.spec").exists():
        Path("GestionEnseignement.spec").unlink()
    print("✓ Nettoyage terminé")
    print()
    
    # Créer l'exécutable
    print("Étape 3/4: Création de l'exécutable (cela peut prendre quelques minutes)...")
    cmd = [
        "pyinstaller",
        "--name=GestionEnseignement",
        "--onefile",
        "--windowed",
        "--add-data", "templates;templates",
        "--add-data", "static;static",
        "--add-data", ".env;.",
        "--hidden-import=flask",
        "--hidden-import=pymysql",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=xlsxwriter",
        "--hidden-import=reportlab",
        "--hidden-import=reportlab.pdfgen",
        "--hidden-import=reportlab.lib",
        "--hidden-import=reportlab.lib.pagesizes",
        "--hidden-import=openpyxl",
        "--hidden-import=jinja2",
        "--hidden-import=werkzeug",
        "--hidden-import=click",
        "--hidden-import=itsdangerous",
        "--hidden-import=blinker",
        "--collect-all=xlsxwriter",
        "--collect-all=reportlab",
        "lancer_application.py"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ Erreur lors de la création de l'exécutable:")
        print(result.stderr)
        raise Exception("Échec de la création de l'exécutable")
    print("✓ Exécutable créé")
    print()
    
    # Créer le package de distribution
    print("Étape 4/4: Création du package de distribution...")
    dist_folder = Path("Distribution")
    dist_folder.mkdir(exist_ok=True)
    (dist_folder / "data").mkdir(exist_ok=True)
    
    # Copier l'exécutable
    shutil.copy("dist/GestionEnseignement.exe", dist_folder)
    
    # Copier les fichiers optionnels (ignorer si manquants)
    fichiers_optionnels = [
        ("README_INSTALLATION.md", "README_INSTALLATION.md"),
        ("DEMARRAGE_RAPIDE.txt", "LIRE_MOI.txt"),
        ("schema.sql", "schema.sql"),
        ("GUIDE_COMPLET_DISTRIBUTION.md", "GUIDE_COMPLET_DISTRIBUTION.md")
    ]
    
    for source, dest in fichiers_optionnels:
        try:
            if Path(source).exists():
                shutil.copy(source, dist_folder / dest)
        except Exception as e:
            print(f"⚠️ Fichier {source} non copié: {e}")
    
    # Créer un fichier LIRE_MOI.txt minimal si absent
    lire_moi = dist_folder / "LIRE_MOI.txt"
    if not lire_moi.exists():
        with open(lire_moi, 'w', encoding='utf-8') as f:
            f.write("GESTION ENSEIGNEMENT - MR KOFFI ELISE\n\n")
            f.write("Double-cliquez sur GestionEnseignement.exe pour lancer l'application.\n\n")
            f.write("Vos données seront stockées dans le dossier data/gestion.db\n")
            f.write("Pensez à sauvegarder ce fichier régulièrement.\n")
    
    print("✓ Package créé")
    print()
    
    print("=" * 60)
    print("  CREATION TERMINEE AVEC SUCCES!")
    print("=" * 60)
    print()
    print(f"L'exécutable se trouve dans: {dist_folder / 'GestionEnseignement.exe'}")
    print()
    print("Pour distribuer l'application:")
    print("1. Compressez le dossier 'Distribution' en ZIP")
    print("2. Envoyez le ZIP à l'utilisateur")
    print("3. L'utilisateur n'a qu'à double-cliquer sur GestionEnseignement.exe")
    print()
    print("IMPORTANT: Le dossier 'data' sera créé automatiquement")
    print("           au premier lancement pour stocker la base de données.")
    print()
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"\nERREUR: {e}")
        input("\nAppuyez sur Entrée pour quitter...")
        sys.exit(1)