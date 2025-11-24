import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

class Config:
    # Configuration de la base de données
    # Par défaut, utilise MySQL pour la production
    USE_SQLITE = os.environ.get('USE_SQLITE', 'False').lower() == 'true'
    
    # Configuration SQLite (développement local uniquement)
    SQLITE_DB = os.environ.get('SQLITE_DB', 'gestion_enseignement.db')
    
    # Configuration MySQL (production - PythonAnywhere recommandé)
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'gestion_enseignement')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
    
    # Clé secrète Flask - DOIT être changée en production
    SECRET_KEY = os.environ.get('SECRET_KEY', 'CHANGE_THIS_IN_PRODUCTION')
    
    # Configuration Flask
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    TESTING = os.environ.get('FLASK_TESTING', 'False').lower() == 'true'
    
    # Configuration de sécurité pour la production
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Autres configurations
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file upload
    