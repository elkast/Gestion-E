import os

class Config:
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'port')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'gestion_enseignement')
    SECRET_KEY = os.environ.get('SECRET_KEY', 'votre_cle_secrete_ici')
