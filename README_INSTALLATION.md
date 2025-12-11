# Guide d'Installation - Application Desktop

## Gestion Enseignement Mr Koffi Elise - Version Portable

### Prérequis

- **Python 3.8 ou supérieur** installé sur votre ordinateur
  - Télécharger depuis : https://www.python.org/downloads/
  - **IMPORTANT** : Cochez "Add Python to PATH" lors de l'installation

### Installation

1. **Extraire le dossier** contenant l'application sur votre ordinateur

2. **Installer les dépendances** (première utilisation uniquement)
   - Double-cliquez sur `lancer_application.bat`
   - Les dépendances s'installeront automatiquement

### Utilisation

#### Sur Windows
- Double-cliquez sur **`lancer_application.bat`**
- L'application s'ouvrira automatiquement dans votre navigateur

#### Sur Mac/Linux
```bash
python3 lancer_application.py
```

### Données

- Toutes les données sont stockées dans le fichier **`data/gestion.db`**
- Ce fichier SQLite contient toutes vos informations
- **Sauvegardez régulièrement ce fichier** pour ne pas perdre vos données

### Arrêt de l'Application

- Fermez la fenêtre du terminal/console
- Ou appuyez sur **Ctrl+C** dans le terminal

### Partage de l'Application

Pour partager l'application avec quelqu'un d'autre :

1. Copiez **tout le dossier** de l'application
2. La personne devra avoir Python installé
3. Elle pourra lancer l'application avec `lancer_application.bat`

### Support

Pour toute question ou problème, contactez l'administrateur.

---

## Structure des Fichiers

```
projet_mr_koffi/
├── lancer_application.bat    # Lanceur Windows
├── lancer_application.py      # Lanceur Python
├── app.py                     # Application principale
├── requirements.txt           # Dépendances
├── schema.sql                 # Schéma de la base de données
├── data/
│   └── gestion.db            # Base de données (créée automatiquement)
├── templates/                 # Pages HTML
├── static/                    # CSS et ressources
└── blueprints/               # Modules de l'application
```

## Fonctionnalités

✅ Gestion des établissements scolaires
✅ Gestion des modules d'enseignement  
✅ Suivi des paiements avec validation automatique
✅ Génération automatique des références de paiement
✅ Calcul automatique des montants restants
✅ Export Excel et PDF
✅ Interface simple et professionnelle
✅ Base de données SQLite portable