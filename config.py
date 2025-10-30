import os

class Config:
    # Configuration de la base de données
    # Utilise MySQL par défaut pour le développement local
    USE_SQLITE = os.environ.get('USE_SQLITE', 'False').lower() == 'true'
    
    # Configuration SQLite (local)
    SQLITE_DB = os.environ.get('SQLITE_DB', 'gestion_enseignement.db')
    
    # Configuration MySQL (pour production - PythonAnywhere/Railway)
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'gestion_enseignement')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
    
    SECRET_KEY = os.environ.get('SECRET_KEY', '7da03cbb130d8854d11d8daf4e0c73665673aa013c7fff24ae377e0a3c2b58fa6')

    # Configuration Flask
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    TESTING = os.environ.get('FLASK_TESTING', 'False').lower() == 'true'
    