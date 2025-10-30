-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : mar. 28 oct. 2025 à 09:43
-- Version du serveur : 9.1.0
-- Version de PHP : 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `gestion_enseignement`
--

-- --------------------------------------------------------

--
-- Structure de la table `ecoles`
--

DROP TABLE IF EXISTS `ecoles`;
CREATE TABLE IF NOT EXISTS `ecoles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(255) NOT NULL,
  `type_etablissement` varchar(100) DEFAULT NULL,
  `adresse` text,
  `ville` varchar(100) DEFAULT NULL,
  `contact` varchar(255) DEFAULT NULL,
  `telephone` varchar(20) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `volume_cm` decimal(8,2) DEFAULT '0.00',
  `volume_td` decimal(8,2) DEFAULT '0.00',
  `volume_tp` decimal(8,2) DEFAULT '0.00',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `ecoles`
--

INSERT INTO `ecoles` (`id`, `nom`, `type_etablissement`, `adresse`, `ville`, `contact`, `telephone`, `created_at`, `volume_cm`, `volume_td`, `volume_tp`) VALUES
(1, 'UIST', '', NULL, '', '', NULL, '2025-10-06 10:00:32', 0.00, 0.00, 0.00),
(2, 'UPB', 'Université', NULL, 'Abidjan', '', '', '2025-10-06 10:40:19', 0.00, 0.00, 0.00);

-- --------------------------------------------------------

--
-- Structure de la table `ecole_niveau_volumes`
--

DROP TABLE IF EXISTS `ecole_niveau_volumes`;
CREATE TABLE IF NOT EXISTS `ecole_niveau_volumes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ecole_id` int DEFAULT NULL,
  `niveau` varchar(100) DEFAULT NULL,
  `volume_cm` decimal(8,2) DEFAULT '0.00',
  `volume_td` decimal(8,2) DEFAULT '0.00',
  `volume_tp` decimal(8,2) DEFAULT '0.00',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_ecole_niveau` (`ecole_id`,`niveau`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `ecole_niveau_volumes`
--

INSERT INTO `ecole_niveau_volumes` (`id`, `ecole_id`, `niveau`, `volume_cm`, `volume_td`, `volume_tp`, `created_at`) VALUES
(1, 1, 'Licence 1', 30.00, 50.00, 102.00, '2025-10-06 10:01:10'),
(2, 1, 'Licence 2', 0.00, 0.00, 0.00, '2025-10-06 10:01:10'),
(3, 1, 'Licence 3', 0.00, 0.00, 0.00, '2025-10-06 10:01:10'),
(4, 1, 'Master 1', 0.00, 0.00, 0.00, '2025-10-06 10:01:10'),
(5, 1, 'Master 2', 0.00, 0.00, 0.00, '2025-10-06 10:01:10'),
(6, 1, 'Doctorat', 0.00, 0.00, 0.00, '2025-10-06 10:01:10');

-- --------------------------------------------------------

--
-- Structure de la table `modules`
--

DROP TABLE IF EXISTS `modules`;
CREATE TABLE IF NOT EXISTS `modules` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nom_module` varchar(255) NOT NULL,
  `ecole_id` int DEFAULT NULL,
  `niveau` varchar(100) DEFAULT NULL,
  `volume_cm` decimal(8,2) DEFAULT '0.00',
  `volume_td` decimal(8,2) DEFAULT '0.00',
  `volume_tp` decimal(8,2) DEFAULT '0.00',
  `volume_total` decimal(8,2) DEFAULT '0.00',
  `montant_heure` decimal(10,2) DEFAULT '0.00',
  `montant_total` decimal(12,2) DEFAULT '0.00',
  `montant_applique` decimal(12,2) DEFAULT '0.00',
  `montant_mensuel` decimal(10,2) DEFAULT '0.00',
  `taux` decimal(5,2) DEFAULT '0.00',
  `annee_universitaire` varchar(20) DEFAULT NULL,
  `statut` enum('actif','termine','annule') DEFAULT 'actif',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `ecole_id` (`ecole_id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `modules`
--

INSERT INTO `modules` (`id`, `nom_module`, `ecole_id`, `niveau`, `volume_cm`, `volume_td`, `volume_tp`, `volume_total`, `montant_heure`, `montant_total`, `montant_applique`, `montant_mensuel`, `taux`, `annee_universitaire`, `statut`, `created_at`) VALUES
(1, 'MATH', 1, 'Licence 1', 10.00, 10.00, 12.00, 32.00, 5000.00, 160000.00, 0.00, 0.00, 0.00, '2024-2025', 'actif', '2025-10-06 10:00:32'),
(2, 'SVT', 1, 'Licence 1', 20.00, 40.00, 90.00, 150.00, 50000.00, 7500000.00, 0.00, 0.00, 0.00, '2024-2025', 'actif', '2025-10-06 10:30:17'),
(3, 'RO', 2, 'Licence 1', 340.00, 55.00, 190.00, 585.00, 1000.00, 585000.00, 0.00, 0.00, 0.00, '2024-2025', 'actif', '2025-10-06 10:42:43'),
(4, 'RTT', 2, 'Licence 2', 20.00, 10.00, 20.00, 50.00, 25000.00, 1250000.00, 0.00, 0.00, 0.00, '2024-2025', 'actif', '2025-10-07 10:58:12'),
(5, 'LARAVEL', 1, 'Master 2', 30.00, 10.00, 0.00, 40.00, 15000.00, 600000.00, 0.00, 0.00, 0.00, '2024-2025', 'actif', '2025-10-08 11:54:58');

-- --------------------------------------------------------

--
-- Structure de la table `paiements`
--

DROP TABLE IF EXISTS `paiements`;
CREATE TABLE IF NOT EXISTS `paiements` (
  `id` int NOT NULL AUTO_INCREMENT,
  `module_id` int DEFAULT NULL,
  `date_paiement` date NOT NULL,
  `montant` decimal(12,2) NOT NULL,
  `type_paiement` enum('avance','solde','total') DEFAULT NULL,
  `reference` varchar(100) DEFAULT NULL,
  `mode_paiement` varchar(50) DEFAULT NULL,
  `statut` enum('complet','partiel','attente') DEFAULT 'complet',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `module_id` (`module_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `paiements`
--

INSERT INTO `paiements` (`id`, `module_id`, `date_paiement`, `montant`, `type_paiement`, `reference`, `mode_paiement`, `statut`, `created_at`) VALUES
(1, 2, '2025-10-06', 6000000.00, 'avance', '', NULL, 'partiel', '2025-10-06 10:31:07'),
(2, 2, '2025-10-06', 7000.00, 'avance', '', NULL, 'partiel', '2025-10-06 10:33:21'),
(3, 5, '2025-10-08', 10000.00, 'avance', '', NULL, 'partiel', '2025-10-08 11:57:02');

-- --------------------------------------------------------

--
-- Structure de la table `taux_horaires`
--

DROP TABLE IF EXISTS `taux_horaires`;
CREATE TABLE IF NOT EXISTS `taux_horaires` (
  `id` int NOT NULL AUTO_INCREMENT,
  `niveau` varchar(100) NOT NULL,
  `taux_min` decimal(10,2) DEFAULT NULL,
  `taux_max` decimal(10,2) DEFAULT NULL,
  `taux_defaut` decimal(10,2) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
