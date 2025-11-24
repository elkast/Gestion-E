-- ==========================================
-- Base de données : gestion_enseignement
-- Schéma SQL complet - Compatible MySQL
-- ==========================================

-- Création de la base
CREATE DATABASE IF NOT EXISTS gestion_enseignement
CHARACTER SET utf8mb4
COLLATE utf8mb4_general_ci;

USE gestion_enseignement;

-- ==========================================
-- Table : ecoles
-- ==========================================CREATE TABLE IF NOT EXISTS ecoles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    type_etablissement VARCHAR(100),
    ville VARCHAR(100),
    contact VARCHAR(100),
    telephone VARCHAR(50),
    email VARCHAR(150),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ==========================================
-- Table : ecole_niveau_volumes
-- ==========================================
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
) ENGINE=InnoDB;

-- ==========================================
-- Table : modules
-- ==========================================
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
) ENGINE=InnoDB;

-- ==========================================
-- Table : paiements
-- ==========================================
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
) ENGINE=InnoDB;

-- ==========================================
-- Table : taux_horaire
-- ==========================================
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
) ENGINE=InnoDB;
