import os

class Config:
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'gestion_enseignement')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
    SECRET_KEY = os.environ.get('SECRET_KEY', 'votre_cle_secrete_ici')