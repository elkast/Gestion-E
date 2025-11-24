#!/usr/bin/env python3
"""
Script de lancement pour le développement local
Usage: python run_local.py
"""
import os
import sys

# Définir les variables d'environnement pour le développement local
os.environ['USE_SQLITE'] = 'True'  # Utiliser SQLite en local
os.environ['FLASK_DEBUG'] = 'True'  # Activer le mode debug
os.environ['FLASK_ENV'] = 'development'

# Importer et lancer l'application
from app import app

if __name__ == '__main__':
    print("=" * 70)
    print("🚀 LANCEMENT DE L'APPLICATION EN MODE DÉVELOPPEMENT LOCAL")
    print("=" * 70)
    print(f"📊 Base de données : SQLite (gestion_enseignement.db)")
    print(f"🌐 URL locale : http://localhost:5000")
    print(f"🔍 Health check : http://localhost:5000/health")
    print("=" * 70)
    print("\n⚠️  Mode DEBUG activé - Ne pas utiliser en production!")
    print("⚠️  Pour la production, utilisez PythonAnywhere\n")
    print("💡 Appuyez sur Ctrl+C pour arrêter le serveur\n")
    
    try:
        app.run(host='127.0.0.1', port=5000, debug=True)
    except KeyboardInterrupt:
        print("\n\n✅ Serveur arrêté proprement")
        sys.exit(0)