-- Schema de la base de données - Gestion Enseignement Mr Koffi Elise
-- Compatible SQLite et MySQL

-- Table des établissements scolaires
CREATE TABLE IF NOT EXISTS ecoles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    type_etablissement TEXT,
    ville TEXT,
    contact TEXT,
    telephone TEXT,
    email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des modules d'enseignement
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
    FOREIGN KEY (ecole_id) REFERENCES ecoles(id) ON DELETE CASCADE
);

-- Table des paiements
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
    FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE
);

-- Table des volumes par niveau (optionnel)
CREATE TABLE IF NOT EXISTS ecole_niveau_volumes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ecole_id INTEGER,
    niveau TEXT,
    volume_cm REAL DEFAULT 0,
    volume_td REAL DEFAULT 0,
    volume_tp REAL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ecole_id) REFERENCES ecoles(id) ON DELETE CASCADE,
    UNIQUE(ecole_id, niveau)
);

-- Index pour améliorer les performances
CREATE INDEX IF NOT EXISTS idx_modules_ecole ON modules(ecole_id);
CREATE INDEX IF NOT EXISTS idx_paiements_module ON paiements(module_id);
CREATE INDEX IF NOT EXISTS idx_ecole_niveau_volumes_ecole ON ecole_niveau_volumes(ecole_id);