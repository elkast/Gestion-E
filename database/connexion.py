"""
Module de gestion de la connexion à la base de données.
Supporte SQLite (portable) et MySQL (production).
"""
import sqlite3
import pymysql
from flask import g, current_app
from pathlib import Path

# Chemin de base du projet (pour chemins relatifs portables)
REPERTOIRE_BASE = Path(__file__).resolve().parent.parent
CHEMIN_DONNEES = REPERTOIRE_BASE / "data"

# Créer le dossier data s'il n'existe pas
CHEMIN_DONNEES.mkdir(exist_ok=True)


def fabrique_dictionnaire(curseur, ligne):
    """Convertit les résultats SQLite en dictionnaires."""
    d = {}
    for idx, col in enumerate(curseur.description):
        d[col[0]] = ligne[idx]
    return d


class CurseurSQLitePatch:
    """Wrapper pour le curseur SQLite qui convertit automatiquement les placeholders MySQL."""
    
    def __init__(self, curseur):
        self._curseur = curseur

    def execute(self, requete, parametres=None):
        # Convertir les placeholders MySQL vers SQLite
        if '%s' in requete:
            requete = requete.replace('%s', '?')
        if parametres:
            return self._curseur.execute(requete, parametres)
        else:
            return self._curseur.execute(requete)

    def fetchone(self):
        return self._curseur.fetchone()

    def fetchall(self):
        return self._curseur.fetchall()

    def close(self):
        return self._curseur.close()

    @property
    def lastrowid(self):
        return self._curseur.lastrowid

    @property
    def rowcount(self):
        return self._curseur.rowcount


class ConnexionSQLitePatch:
    """Wrapper pour la connexion SQLite qui retourne des curseurs patchés."""
    
    def __init__(self, connexion):
        self._connexion = connexion

    def cursor(self):
        curseur_original = self._connexion.cursor()
        return CurseurSQLitePatch(curseur_original)

    def __getattr__(self, nom):
        return getattr(self._connexion, nom)


def obtenir_db():
    """
    Crée une connexion à la base de données (SQLite ou MySQL selon la config).
    Utilise des chemins relatifs pour la portabilité.
    """
    if 'db' not in g:
        if current_app.config.get('UTILISER_SQLITE', True):
            # Utiliser SQLite pour le développement local et version portable
            nom_db = current_app.config.get('NOM_DB_SQLITE', 'gestion.db')
            chemin_db = CHEMIN_DONNEES / nom_db
            
            connexion = sqlite3.connect(str(chemin_db))
            connexion.row_factory = fabrique_dictionnaire
            g.db = ConnexionSQLitePatch(connexion)
            g.est_sqlite = True

            # Créer les tables si elles n'existent pas
            initialiser_db_sqlite(g.db)
        else:
            # Utiliser MySQL pour la production
            g.db = pymysql.connect(
                host=current_app.config['HOTE_MYSQL'],
                user=current_app.config['UTILISATEUR_MYSQL'],
                password=current_app.config['MOT_DE_PASSE_MYSQL'],
                database=current_app.config['NOM_DB_MYSQL'],
                port=current_app.config['PORT_MYSQL'],
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=False
            )
            g.est_sqlite = False

            # Initialiser la base de données MySQL si nécessaire
            initialiser_db_mysql(g.db)
    return g.db


def initialiser_db_mysql(db):
    """Initialise la base de données MySQL avec les tables nécessaires."""
    curseur = db.cursor()

    # Créer la base de données si elle n'existe pas
    curseur.execute("CREATE DATABASE IF NOT EXISTS gestion_enseignement CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")
    curseur.execute("USE gestion_enseignement")

    # Table ecoles
    curseur.execute("""
        CREATE TABLE IF NOT EXISTS ecoles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nom VARCHAR(255) NOT NULL,
            type_etablissement VARCHAR(100),
            ville VARCHAR(100),
            contact VARCHAR(100),
            telephone VARCHAR(50),
            email VARCHAR(150),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB
    """)

    # Table ecole_niveau_volumes
    curseur.execute("""
        CREATE TABLE IF NOT EXISTS ecole_niveau_volumes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            ecole_id INT,
            niveau VARCHAR(100),
            volume_cm DECIMAL(10,2) DEFAULT 0,
            volume_td DECIMAL(10,2) DEFAULT 0,
            volume_tp DECIMAL(10,2) DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE KEY unique_ecole_niveau (ecole_id, niveau),
            CONSTRAINT fk_ecole_niveau_ecole
                FOREIGN KEY (ecole_id)
                REFERENCES ecoles(id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        ) ENGINE=InnoDB
    """)

    # Table modules
    curseur.execute("""
        CREATE TABLE IF NOT EXISTS modules (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nom_module VARCHAR(255) NOT NULL,
            ecole_id INT,
            niveau VARCHAR(100),
            volume_cm DECIMAL(10,2) DEFAULT 0,
            volume_td DECIMAL(10,2) DEFAULT 0,
            volume_tp DECIMAL(10,2) DEFAULT 0,
            volume_total DECIMAL(10,2) DEFAULT 0,
            tarif_cm DECIMAL(10,2) DEFAULT 0,
            tarif_td DECIMAL(10,2) DEFAULT 0,
            tarif_tp DECIMAL(10,2) DEFAULT 0,
            montant_heure DECIMAL(10,2) DEFAULT 0,
            montant_total DECIMAL(10,2) DEFAULT 0,
            annee_universitaire VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_module_ecole
                FOREIGN KEY (ecole_id)
                REFERENCES ecoles(id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        ) ENGINE=InnoDB
    """)

    # Table paiements
    curseur.execute("""
        CREATE TABLE IF NOT EXISTS paiements (
            id INT AUTO_INCREMENT PRIMARY KEY,
            module_id INT,
            montant DECIMAL(10,2) NOT NULL,
            date_paiement DATE NOT NULL,
            type_paiement VARCHAR(100),
            mode_paiement VARCHAR(100),
            reference VARCHAR(100),
            statut VARCHAR(50) DEFAULT 'partiel',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_paiement_module
                FOREIGN KEY (module_id)
                REFERENCES modules(id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        ) ENGINE=InnoDB
    """)

    # Table taux_horaire
    curseur.execute("""
        CREATE TABLE IF NOT EXISTS taux_horaire (
            id INT AUTO_INCREMENT PRIMARY KEY,
            ecole_id INT,
            niveau VARCHAR(100),
            tarif_cm DECIMAL(10,2) DEFAULT 0,
            tarif_td DECIMAL(10,2) DEFAULT 0,
            tarif_tp DECIMAL(10,2) DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE KEY unique_taux (ecole_id, niveau),
            CONSTRAINT fk_taux_ecole
                FOREIGN KEY (ecole_id)
                REFERENCES ecoles(id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        ) ENGINE=InnoDB
    """)

    db.commit()


def initialiser_db_sqlite(db):
    """Initialise la base de données SQLite avec les tables nécessaires."""
    curseur = db.cursor()

    # Table ecoles
    curseur.execute("""
        CREATE TABLE IF NOT EXISTS ecoles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            type_etablissement TEXT,
            ville TEXT,
            contact TEXT,
            telephone TEXT,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Table modules
    curseur.execute("""
        CREATE TABLE IF NOT EXISTS modules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_module TEXT NOT NULL,
            ecole_id INTEGER,
            niveau TEXT,
            volume_cm REAL DEFAULT 0,
            volume_td REAL DEFAULT 0,
            volume_tp REAL DEFAULT 0,
            volume_total REAL DEFAULT 0,
            tarif_cm REAL DEFAULT 0,
            tarif_td REAL DEFAULT 0,
            tarif_tp REAL DEFAULT 0,
            montant_heure REAL DEFAULT 0,
            montant_total REAL DEFAULT 0,
            annee_universitaire TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ecole_id) REFERENCES ecoles(id)
        )
    """)

    # Table paiements
    curseur.execute("""
        CREATE TABLE IF NOT EXISTS paiements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            module_id INTEGER,
            montant REAL NOT NULL,
            date_paiement DATE NOT NULL,
            type_paiement TEXT,
            mode_paiement TEXT,
            reference TEXT,
            statut TEXT DEFAULT 'partiel',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (module_id) REFERENCES modules(id)
        )
    """)

    # Table ecole_niveau_volumes
    curseur.execute("""
        CREATE TABLE IF NOT EXISTS ecole_niveau_volumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ecole_id INTEGER,
            niveau TEXT,
            volume_cm REAL DEFAULT 0,
            volume_td REAL DEFAULT 0,
            volume_tp REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ecole_id) REFERENCES ecoles(id),
            UNIQUE(ecole_id, niveau)
        )
    """)

    db.commit()


def fermer_db(erreur=None):
    """Ferme la connexion à la base de données."""
    db = g.pop('db', None)
    if db is not None:
        db.close()


def initialiser_app(app):
    """Initialise l'application avec les gestionnaires de DB."""
    app.teardown_appcontext(fermer_db)