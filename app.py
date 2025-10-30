import os
import sys
import threading
from flask import Flask
from config import Config
from blueprints.principal import principal_bp
from blueprints.ecoles import schools_bp
from blueprints.paiements import payments_bp
from blueprints.db import init_app
import webview

# --- Fonction pour gérer les chemins de PyInstaller ---
def get_resource_path(relative_path):
    """Détermine le chemin correct des ressources après la compilation par PyInstaller."""
    try:
        # Chemin lorsque l'application est compilée dans un exécutable
        base_path = sys._MEIPASS
    except Exception:
        # Chemin lorsque l'application est exécutée normalement
        base_path = os.path.abspath(os.path.dirname(__file__))
    
    return os.path.join(base_path, relative_path)

# --- Initialisation de Flask et de la DB ---
# Assurez-vous que vos dossiers sont nommés 'templates' et 'static'
TEMPLATE_DIR = get_resource_path('templates')
STATIC_DIR = get_resource_path('static')

# Modifiez l'initialisation de Flask
app = Flask(__name__, 
            template_folder=TEMPLATE_DIR, 
            static_folder=STATIC_DIR)
app.config.from_object(Config)

# GESTION DE VOTRE BASE DE DONNÉES (SQLite)
DB_FILE = "gestion_enseignement.db"
DB_PATH = get_resource_path(DB_FILE)
app.config['SQLITE_DB'] = DB_PATH

# Initialiser la gestion de la DB
init_app(app)

# Enregistrer les blueprints
app.register_blueprint(principal_bp)
app.register_blueprint(schools_bp)
app.register_blueprint(payments_bp)

# Health check endpoint
@app.route('/health')
def health_check():
    """Endpoint de santé pour vérifier que l'application fonctionne"""
    try:
        from blueprints.db import get_db
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        return {
            "status": "healthy",
            "database": "connected",
            "message": "Application is running correctly"
        }, 200
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "message": "Database connection failed. Check MYSQL_* environment variables in Railway."
        }, 503

if __name__ == '__main__':
    # Le serveur Flask doit être lancé en premier dans un thread
    threading.Thread(target=app.run, kwargs={'host': '127.0.0.1', 'port': 5000}).start()
    
    # Lance la fenêtre pywebview qui pointe vers le serveur local
    webview.create_window('Zen Faskk', 'http://127.0.0.1:5000', width=1000, height=700)
    webview.start()
