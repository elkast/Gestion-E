import sqlite3
import pymysql
from flask import g, current_app
import os

def dict_factory(cursor, row):
    """Convertit les résultats SQLite en dictionnaires"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class PatchedSQLiteCursor:
    """Wrapper for SQLite cursor that auto-converts MySQL placeholders"""
    def __init__(self, cursor):
        self._cursor = cursor

    def execute(self, query, params=None):
        # Convert MySQL placeholders to SQLite
        if '%s' in query:
            query = query.replace('%s', '?')
        if params:
            return self._cursor.execute(query, params)
        else:
            return self._cursor.execute(query)

    def fetchone(self):
        return self._cursor.fetchone()

    def fetchall(self):
        return self._cursor.fetchall()

    def close(self):
        return self._cursor.close()

    @property
    def lastrowid(self):
        return self._cursor.lastrowid

    @property
    def rowcount(self):
        return self._cursor.rowcount

class PatchedSQLiteConnection:
    """Wrapper for SQLite connection that returns patched cursors"""
    def __init__(self, conn):
        self._conn = conn

    def cursor(self, factory=None):
        original_cursor = self._conn.cursor(factory)
        return PatchedSQLiteCursor(original_cursor)

    def __getattr__(self, name):
        return getattr(self._conn, name)

def get_db():
    """Crée une connexion à la base de données (SQLite ou MySQL selon la config)"""
    if 'db' not in g:
        if current_app.config.get('USE_SQLITE', True):
            # Utiliser SQLite pour le développement local
            db_path = current_app.config.get('SQLITE_DB', 'gestion_enseignement.db')
            conn = sqlite3.connect(db_path)
            conn.row_factory = dict_factory
            g.db = PatchedSQLiteConnection(conn)
            g.is_sqlite = True

            # Créer les tables si elles n'existent pas
            init_sqlite_db(g.db)
        else:
            # Utiliser MySQL pour la production
            g.db = pymysql.connect(
                host=current_app.config['MYSQL_HOST'],
                user=current_app.config['MYSQL_USER'],
                password=current_app.config['MYSQL_PASSWORD'],
                database=current_app.config['MYSQL_DB'],
                port=current_app.config['MYSQL_PORT'],
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=False
            )
            g.is_sqlite = False
    return g.db

def init_sqlite_db(db):
    """Initialise la base de données SQLite avec les tables nécessaires"""
    cursor = db.cursor()
    
    # Table ecoles
    cursor.execute("""
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
    cursor.execute("""
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
    cursor.execute("""
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
    cursor.execute("""
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

def close_db(error=None):
    """Ferme la connexion à la base de données"""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    """Initialise l'application avec les gestionnaires de DB"""
    app.teardown_appcontext(close_db)