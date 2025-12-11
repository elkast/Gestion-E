"""
Configuration de l'application Flask.
Supporte différents modes : développement, portable, production.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

# Chemin de base du projet
REPERTOIRE_BASE = Path(__file__).resolve().parent


class ConfigurationBase:
    """Configuration de base commune à tous les environnements."""
    
    # Clé secrète Flask - DOIT être changée en production
    SECRET_KEY = os.environ.get('CLE_SECRETE', 'cle_dev_a_changer_en_production_12345')
    
    # Configuration Flask
    DEBUG = False
    TESTING = False
    
    # Configuration de sécurité
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Taille maximale des fichiers uploadés
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB


class ConfigurationDeveloppement(ConfigurationBase):
    """Configuration pour le développement local."""
    
    DEBUG = True
    UTILISER_SQLITE = True
    NOM_DB_SQLITE = 'gestion.db'


class ConfigurationPortable(ConfigurationBase):
    """Configuration pour la version portable (application desktop)."""
    
    DEBUG = True
    UTILISER_SQLITE = True
    NOM_DB_SQLITE = 'gestion.db'


class ConfigurationProduction(ConfigurationBase):
    """Configuration pour la production (PythonAnywhere, serveur)."""
    
    DEBUG = False
    UTILISER_SQLITE = os.environ.get('UTILISER_SQLITE', 'False').lower() == 'true'
    
    # Configuration SQLite (si utilisé en production)
    NOM_DB_SQLITE = os.environ.get('NOM_DB_SQLITE', 'gestion.db')
    
    # Configuration MySQL (production)
    HOTE_MYSQL = os.environ.get('HOTE_MYSQL', 'localhost')
    UTILISATEUR_MYSQL = os.environ.get('UTILISATEUR_MYSQL', 'root')
    MOT_DE_PASSE_MYSQL = os.environ.get('MOT_DE_PASSE_MYSQL', '')
    NOM_DB_MYSQL = os.environ.get('NOM_DB_MYSQL', 'gestion_enseignement')
    PORT_MYSQL = int(os.environ.get('PORT_MYSQL', 3306))
    
    # Sécurité renforcée en production
    SESSION_COOKIE_SECURE = True
    SECRET_KEY = os.environ.get('CLE_SECRETE', 'production_secret_key_change_this')


def obtenir_configuration():
    """
    Retourne la configuration appropriée selon l'environnement.
    Lit la variable ENVIRONNEMENT_FLASK depuis .env
    """
    environnement = os.environ.get('ENVIRONNEMENT_FLASK', 'developpement')
    
    configurations = {
        'developpement': ConfigurationDeveloppement,
        'portable': ConfigurationPortable,
        'production': ConfigurationProduction
    }
    
    return configurations.get(environnement, ConfigurationDeveloppement)