-- ==========================================
-- Script de création de la base de données MySQL
-- Pour phpMyAdmin - Exécutez ce script dans phpMyAdmin
-- ==========================================

-- Création de la base de données
CREATE DATABASE IF NOT EXISTS gestion_enseignement
CHARACTER SET utf8mb4
COLLATE utf8mb4_general_ci;

-- Utilisation de la base de données
USE gestion_enseignement;

-- ==========================================
-- Table : ecoles
-- ==========================================
CREATE TABLE IF NOT EXISTS ecoles (
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

-- ==========================================
-- Insertion de données d'exemple (optionnel)
-- ==========================================

-- Exemple d'écoles
INSERT INTO ecoles (nom, type_etablissement, ville, contact, telephone, email) VALUES
('Université de Yaoundé I', 'Université Publique', 'Yaoundé', 'Dr. Jean Dupont', '+237 222 22 22 22', 'contact@univ-yaounde1.cm'),
('Université de Douala', 'Université Publique', 'Douala', 'Dr. Marie Claire', '+237 233 33 33 33', 'info@univ-douala.cm'),
('Université Catholique d\'Afrique Centrale', 'Université Privée', 'Yaoundé', 'Père Michel', '+237 222 44 44 44', 'admission@ucac.cm');

-- Exemple de taux horaires
INSERT INTO taux_horaire (ecole_id, niveau, tarif_cm, tarif_td, tarif_tp) VALUES
(1, 'Licence 1', 15000, 12000, 10000),
(1, 'Licence 2', 16000, 13000, 11000),
(1, 'Licence 3', 17000, 14000, 12000),
(1, 'Master 1', 20000, 17000, 15000),
(1, 'Master 2', 22000, 19000, 17000),
(2, 'Licence 1', 14000, 11000, 9000),
(2, 'Licence 2', 15000, 12000, 10000),
(2, 'Licence 3', 16000, 13000, 11000),
(2, 'Master 1', 19000, 16000, 14000),
(2, 'Master 2', 21000, 18000, 16000),
(3, 'Licence 1', 18000, 15000, 13000),
(3, 'Licence 2', 19000, 16000, 14000),
(3, 'Licence 3', 20000, 17000, 15000),
(3, 'Master 1', 25000, 22000, 20000),
(3, 'Master 2', 27000, 24000, 22000);

-- Exemple de modules
INSERT INTO modules (nom_module, ecole_id, niveau, volume_cm, volume_td, volume_tp, volume_total, tarif_cm, tarif_td, tarif_tp, montant_heure, montant_total, annee_universitaire) VALUES
('Algorithmes et Programmation', 1, 'Licence 1', 30, 20, 15, 65, 15000, 12000, 10000, 0, 0, '2023-2024'),
('Base de Données', 1, 'Licence 2', 25, 25, 20, 70, 16000, 13000, 11000, 0, 0, '2023-2024'),
('Intelligence Artificielle', 1, 'Master 1', 20, 30, 25, 75, 20000, 17000, 15000, 0, 0, '2023-2024'),
('Mathématiques Appliquées', 2, 'Licence 1', 35, 15, 10, 60, 14000, 11000, 9000, 0, 0, '2023-2024'),
('Statistiques', 2, 'Licence 3', 20, 25, 15, 60, 16000, 13000, 11000, 0, 0, '2023-2024'),
('Économie', 3, 'Master 1', 25, 20, 15, 60, 25000, 22000, 20000, 0, 0, '2023-2024');

-- Calcul automatique des montants (sera fait par l'application)
-- Exemple de paiements
INSERT INTO paiements (module_id, montant, date_paiement, type_paiement, mode_paiement, reference, statut, notes) VALUES
(1, 500000, '2023-10-01', 'Paiement partiel', 'Virement bancaire', 'PAY-001', 'partiel', 'Premier paiement pour Algorithmes'),
(2, 750000, '2023-10-05', 'Paiement complet', 'Chèque', 'PAY-002', 'complet', 'Paiement complet pour Base de Données'),
(3, 300000, '2023-10-10', 'Paiement partiel', 'Espèces', 'PAY-003', 'partiel', 'Avance pour IA'),
(4, 400000, '2023-10-15', 'Paiement partiel', 'Virement bancaire', 'PAY-004', 'partiel', 'Paiement pour Mathématiques');

-- ==========================================
-- Création d'un utilisateur pour l'application (optionnel)
-- ==========================================
-- CREATE USER IF NOT EXISTS 'app_user'@'localhost' IDENTIFIED BY 'secure_password';
-- GRANT ALL PRIVILEGES ON gestion_enseignement.* TO 'app_user'@'localhost';
-- FLUSH PRIVILEGES;
