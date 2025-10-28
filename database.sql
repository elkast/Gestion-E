-- Table des établissements
CREATE TABLE ecoles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    type_etablissement VARCHAR(100),
    ville VARCHAR(100),
    contact VARCHAR(255),
    telephone VARCHAR(20),
    telephone DECIMAL(8,2) DEFAULT 0,
    volume_td DECIMAL(8,2) DEFAULT 0,
    volume_tp DECIMAL(8,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des volumes par niveau pour chaque école
CREATE TABLE ecole_niveau_volumes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ecole_id INT,
    niveau VARCHAR(100),
    volume_cm DECIMAL(8,2) DEFAULT 0,
    volume_td DECIMAL(8,2) DEFAULT 0,
    volume_tp DECIMAL(8,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ecole_id) REFERENCES ecoles(id),
    UNIQUE KEY unique_ecole_niveau (ecole_id, niveau)
);

-- Table des modules
CREATE TABLE modules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom_module VARCHAR(255) NOT NULL,
    ecole_id INT,
    niveau VARCHAR(100),
    volume_cm DECIMAL(8,2) DEFAULT 0,
    volume_td DECIMAL(8,2) DEFAULT 0,
    volume_tp DECIMAL(8,2) DEFAULT 0,
    volume_total DECIMAL(8,2) DEFAULT 0,
    montant_heure DECIMAL(10,2) DEFAULT 0,
    montant_total DECIMAL(12,2) DEFAULT 0,
    annee_universitaire VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ecole_id) REFERENCES ecoles(id)
);

-- Table des paiements
CREATE TABLE paiements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    module_id INT,
    montant DECIMAL(12,2) NOT NULL,
    type_paiement VARCHAR(50),
    reference VARCHAR(100),
    date_paiement DATE NOT NULL,
    statut ENUM('complet', 'partiel', 'excédent') DEFAULT 'complet',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (module_id) REFERENCES modules(id)
);


