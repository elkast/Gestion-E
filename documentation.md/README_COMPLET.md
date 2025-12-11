# 🎓 Gestion d'Enseignement - Mr Koffi Elise

[![Flask](https://img.shields.io/badge/Flask-3.1.2-blue.svg)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey.svg)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-Private-red.svg)]()

## 📋 Table des Matières

- [Vue d'ensemble](#-vue-densemble)
- [Architecture du Projet](#-architecture-du-projet)
- [Fonctionnalités](#-fonctionnalités)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Utilisation](#-utilisation)
- [Structure de la Base de Données](#-structure-de-la-base-de-données)
- [Guide du Développeur](#-guide-du-développeur)
- [Déploiement](#-déploiement)
- [FAQ](#-faq)

---

## 🎯 Vue d'ensemble

**Gestion d'Enseignement** est une application web moderne et professionnelle développée avec Flask pour la gestion complète des établissements scolaires, modules d'enseignement et suivi des paiements.

### ✨ Points Forts

- ✅ **Architecture Modulaire** : Code organisé en blueprints pour une maintenance facile
- ✅ **Portable** : Fonctionne sur n'importe quel PC avec SQLite (pas besoin de serveur MySQL)
- ✅ **Bilingue** : Code entièrement en français pour une meilleure compréhension
- ✅ **Responsive** : Interface adaptée aux mobiles, tablettes et ordinateurs
- ✅ **Professionnelle** : Design moderne avec Bootstrap 5
- ✅ **Exportable** : Export des données en Excel et PDF

---

## 🏗️ Architecture du Projet

### Structure des Dossiers

```
projet_mr_koffi/
│
├── app.py                          # Point d'entrée principal de l'application
├── configuration.py                # Configuration (dev, portable, production)
├── wsgi.py                        # Point d'entrée WSGI pour déploiement
├── requirements.txt               # Dépendances Python
├── .env                           # Variables d'environnement (à configurer)
├── README_COMPLET.md              # Ce fichier
│
├── database/                      # 📦 Module de gestion de la base de données
│   ├── __init__.py
│   └── connexion.py              # Gestion connexion SQLite/MySQL avec chemins relatifs
│
├── data/                          # 💾 Dossier des fichiers SQLite (portable)
│   └── gestion.db                # Base de données SQLite (créée automatiquement)
│
├── blueprints/                    # 🔷 Modules fonctionnels (Blueprints Flask)
│   ├── __init__.py
│   ├── principal.py              # Tableau de bord et gestion des modules
│   ├── ecoles.py                 # Gestion des établissements scolaires
│   └── paiements.py              # Gestion des paiements
│
├── templates/                     # 🎨 Templates HTML (organisés par module)
│   ├── principal/
│   │   ├── index.html            # Tableau de bord
│   │   └── export.html           # Page d'export
│   ├── ecoles/
│   │   ├── liste.html            # Liste des établissements
│   │   ├── ajouter.html          # Ajouter un établissement
│   │   ├── modifier.html         # Modifier un établissement
│   │   ├── finances.html         # États financiers par école
│   │   ├── volumes_niveau.html   # Gestion volumes par niveau
│   │   └── volumes_niveau_standalone.html
│   ├── modules/
│   │   ├── ajouter.html          # Ajouter un module
│   │   ├── modifier.html         # Modifier un module
│   │   └── details.html          # Détails d'un module
│   └── paiements/
│       ├── liste.html            # Liste des paiements
│       └── modifier.html         # Modifier un paiement
│
└── static/                        # 🎨 Fichiers statiques (CSS, JS, Images)
    ├── css/
    │   └── style.css             # Styles personnalisés
    ├── js/                       # Scripts JavaScript (si nécessaire)
    └── images/                   # Images et logos
```

### 🔄 Flux de Données

```
┌─────────────┐
│   Navigateur │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│   app.py        │  ← Point d'entrée Flask
└──────┬──────────┘
       │
       ▼
┌─────────────────────────────────┐
│   Blueprints (Routes)           │
│  - principal.py                 │
│  - ecoles.py                    │
│  - paiements.py                 │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│   database/connexion.py         │  ← Gestion DB (SQLite/MySQL)
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────┐
│   data/gestion.db│  ← Base de données SQLite
└─────────────────┘
```

---

## 🚀 Fonctionnalités

### 📚 Gestion des Modules d'Enseignement

- ✅ Créer, modifier, supprimer des modules
- ✅ Calcul automatique des volumes horaires (CM, TD, TP)
- ✅ Calcul automatique des montants (tarifs × volumes)
- ✅ Gestion par niveaux (Licence 1-3, Master 1-2, Doctorat)
- ✅ Association aux établissements

### 🏫 Gestion des Établissements

- ✅ Ajouter, modifier, supprimer des établissements
- ✅ Informations complètes (nom, type, ville, contact, téléphone, email)
- ✅ Vue des montants totaux par établissement
- ✅ Gestion des volumes par niveau et par établissement

### 💰 Gestion des Paiements

- ✅ Enregistrer les paiements par module
- ✅ Calcul automatique du statut (partiel, complet, excédent)
- ✅ Historique complet des transactions
- ✅ Validation automatique (empêche les surpaiements)

### 📊 Tableaux de Bord et Rapports

- ✅ Vue d'ensemble financière (gains totaux, perçus, reste à percevoir)
- ✅ États financiers détaillés par établissement
- ✅ Export Excel avec toutes les données
- ✅ Export PDF pour les rapports

### 🎨 Interface Utilisateur

- ✅ Design moderne et professionnel (Bootstrap 5)
- ✅ Responsive (mobile, tablette, desktop)
- ✅ Messages de feedback utilisateur
- ✅ Formulaires avec validation
- ✅ Calculs en temps réel (JavaScript)

---

## 💻 Installation

### Prérequis

- **Python** : Version 3.8 ou supérieure
- **pip** : Gestionnaire de paquets Python
- **Git** (optionnel) : Pour cloner le repository

### Étape 1 : Cloner ou Télécharger le Projet

```bash
# Option 1 : Cloner avec Git
git clone https://github.com/VOTRE_USERNAME/projet_mr_koffi.git
cd projet_mr_koffi

# Option 2 : Télécharger le ZIP et extraire
```

### Étape 2 : Créer un Environnement Virtuel

```bash
# Sur Windows
python -m venv venv
venv\Scripts\activate

# Sur Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Étape 3 : Installer les Dépendances

```bash
pip install -r requirements.txt
```

### Étape 4 : Configurer l'Application

Créez ou modifiez le fichier `.env` à la racine du projet :

```env
# Mode de l'application (developpement, portable, production)
ENVIRONNEMENT_FLASK=portable

# Clé secrète (CHANGEZ-LA !)
CLE_SECRETE=votre_cle_secrete_unique_a_changer

# Base de données (SQLite par défaut)
UTILISER_SQLITE=True
NOM_DB_SQLITE=gestion.db

# Debug (True pour développement, False pour production)
FLASK_DEBUG=True
```

### Étape 5 : Lancer l'Application

```bash
python app.py
```

L'application sera accessible sur : **http://localhost:5000**

---

## ⚙️ Configuration

### Modes de Configuration

L'application supporte 3 modes configurables via `ENVIRONNEMENT_FLASK` dans `.env` :

#### 1. Mode Développement (`developpement`)

```env
ENVIRONNEMENT_FLASK=developpement
FLASK_DEBUG=True
UTILISER_SQLITE=True
```

- ✅ Debug activé
- ✅ SQLite local
- ✅ Rechargement automatique du code

#### 2. Mode Portable (`portable`)

```env
ENVIRONNEMENT_FLASK=portable
UTILISER_SQLITE=True
NOM_DB_SQLITE=gestion.db
```

- ✅ Fonctionne sur n'importe quel PC
- ✅ Base de données dans le dossier `data/`
- ✅ Pas besoin de serveur MySQL
- ✅ Idéal pour une application desktop

#### 3. Mode Production (`production`)

```env
ENVIRONNEMENT_FLASK=production
UTILISER_SQLITE=False
HOTE_MYSQL=localhost
UTILISATEUR_MYSQL=root
MOT_DE_PASSE_MYSQL=votre_mot_de_passe
NOM_DB_MYSQL=gestion_enseignement
PORT_MYSQL=3306
CLE_SECRETE=cle_secrete_production_tres_longue
```

- ✅ MySQL pour performances
- ✅ Sécurité renforcée
- ✅ Cookies sécurisés (HTTPS)

---

## 📖 Utilisation

### Démarrage Rapide

1. **Lancer l'application**
   ```bash
   python app.py
   ```

2. **Ouvrir le navigateur**
   - Aller sur : `http://localhost:5000`

3. **Créer un établissement**
   - Menu : Établissements → Ajouter un établissement
   - Remplir les informations (nom, type, ville, contact)

4. **Créer un module**
   - Menu : Nouveau Module
   - Sélectionner l'établissement
   - Remplir les volumes horaires et tarifs
   - Les calculs se font automatiquement

5. **Enregistrer un paiement**
   - Depuis le tableau de bord, cliquer sur "💰 Paiements"
   - Ajouter un paiement avec montant et référence
   - Le statut est calculé automatiquement

### Fonctionnalités Avancées

#### Export des Données

- **Excel** : Menu Export → Télécharger Excel
- **PDF** : Menu Export → Télécharger PDF

#### États Financiers

- Menu : États Financiers
- Voir les montants dus, perçus et restants par établissement
- Filtrer et trier les résultats

#### Gestion des Volumes par Niveau

- Menu : Gestion Volumes
- Modifier les volumes horaires par niveau pour chaque établissement

---

## 🗄️ Structure de la Base de Données

### Tables Principales

#### Table `ecoles`

| Colonne             | Type          | Description                    |
|---------------------|---------------|--------------------------------|
| id                  | INTEGER (PK)  | Identifiant unique             |
| nom                 | TEXT          | Nom de l'établissement         |
| type_etablissement  | TEXT          | Type (Université, IUT, etc.)   |
| ville               | TEXT          | Ville                          |
| contact             | TEXT          | Personne de contact            |
| telephone           | TEXT          | Numéro de téléphone            |
| email               | TEXT          | Adresse email                  |
| created_at          | TIMESTAMP     | Date de création               |

#### Table `modules`

| Colonne             | Type          | Description                    |
|---------------------|---------------|--------------------------------|
| id                  | INTEGER (PK)  | Identifiant unique             |
| nom_module          | TEXT          | Nom du module                  |
| ecole_id            | INTEGER (FK)  | Référence à l'établissement    |
| niveau              | TEXT          | Niveau (L1, L2, M1, etc.)      |
| volume_cm           | REAL          | Volume CM (heures)             |
| volume_td           | REAL          | Volume TD (heures)             |
| volume_tp           | REAL          | Volume TP (heures)             |
| volume_total        | REAL          | Volume total (calculé)         |
| tarif_cm            | REAL          | Tarif horaire CM (FCFA)        |
| tarif_td            | REAL          | Tarif horaire TD (FCFA)        |
| tarif_tp            | REAL          | Tarif horaire TP (FCFA)        |
| montant_heure       | REAL          | Montant horaire moyen          |
| montant_total       | REAL          | Montant total (calculé)        |
| annee_universitaire | TEXT          | Année (ex: 2024-2025)          |
| created_at          | TIMESTAMP     | Date de création               |

#### Table `paiements`

| Colonne         | Type          | Description                    |
|-----------------|---------------|--------------------------------|
| id              | INTEGER (PK)  | Identifiant unique             |
| module_id       | INTEGER (FK)  | Référence au module            |
| montant         | REAL          | Montant du paiement (FCFA)     |
| date_paiement   | DATE          | Date du paiement               |
| type_paiement   | TEXT          | Type (Virement, Chèque, etc.)  |
| mode_paiement   | TEXT          | Mode de paiement               |
| reference       | TEXT          | Référence du paiement          |
| statut          | TEXT          | Statut (partiel, complet)      |
| notes           | TEXT          | Notes additionnelles           |
| created_at      | TIMESTAMP     | Date de création               |

#### Table `ecole_niveau_volumes`

| Colonne     | Type          | Description                    |
|-------------|---------------|--------------------------------|
| id          | INTEGER (PK)  | Identifiant unique             |
| ecole_id    | INTEGER (FK)  | Référence à l'établissement    |
| niveau      | TEXT          | Niveau                         |
| volume_cm   | REAL          | Volume CM total                |
| volume_td   | REAL          | Volume TD total                |
| volume_tp   | REAL          | Volume TP total                |
| created_at  | TIMESTAMP     | Date de création               |

### Relations

```
ecoles (1) ──────< (N) modules
modules (1) ──────< (N) paiements
ecoles (1) ──────< (N) ecole_niveau_volumes
```

---

## 👨‍💻 Guide du Développeur

### Structure du Code

#### 1. Blueprints (Modules Fonctionnels)

Les blueprints organisent le code par fonctionnalité :

- **`blueprints/principal.py`** : Tableau de bord, modules, exports
- **`blueprints/ecoles.py`** : Gestion des établissements
- **`blueprints/paiements.py`** : Gestion des paiements

#### 2. Base de Données (`database/connexion.py`)

- **`obtenir_db()`** : Obtient une connexion à la DB (SQLite ou MySQL)
- **`initialiser_db_sqlite()`** : Crée les tables SQLite
- **`initialiser_db_mysql()`** : Crée les tables MySQL
- **`fermer_db()`** : Ferme la connexion
- **Chemins relatifs** : Utilise `Path(__file__).resolve().parent.parent` pour la portabilité

#### 3. Configuration (`configuration.py`)

Classes de configuration pour chaque environnement :

```python
class ConfigurationDeveloppement(ConfigurationBase):
    DEBUG = True
    UTILISER_SQLITE = True

class ConfigurationPortable(ConfigurationBase):
    UTILISER_SQLITE = True

class ConfigurationProduction(ConfigurationBase):
    DEBUG = False
    # Configuration MySQL
```

### Ajouter une Nouvelle Fonctionnalité

#### Exemple : Ajouter une route pour les statistiques

1. **Créer la route dans le blueprint approprié**

```python
# Dans blueprints/principal.py
@bp_principal.route('/statistiques')
def statistiques():
    db = obtenir_db()
    curseur = db.cursor()
    
    # Votre logique ici
    curseur.execute("SELECT COUNT(*) as total FROM modules")
    stats = curseur.fetchone()
    
    curseur.close()
    return render_template('principal/statistiques.html', stats=stats)
```

2. **Créer le template**

```html
<!-- templates/principal/statistiques.html -->
<!DOCTYPE html>
<html lang="fr">
<head>
    <title>Statistiques</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <h1>Statistiques</h1>
    <p>Total modules : {{ stats.total }}</p>
</body>
</html>
```

3. **Ajouter le lien dans la navigation**

```html
<!-- Dans templates/principal/index.html -->
<a class="nav-link" href="/statistiques">Statistiques</a>
```

### Conventions de Code

#### Nommage en Français

```python
# ✅ Bon
def obtenir_liste_ecoles():
    pass

# ❌ Mauvais
def get_school_list():
    pass
```

#### Variables et Fonctions

- **Fonctions** : `snake_case` en français
- **Classes** : `PascalCase` en français
- **Constantes** : `MAJUSCULES_AVEC_UNDERSCORES`

```python
# Exemples
def calculer_montant_total(volume, tarif):
    return volume * tarif

class GestionnaireEcoles:
    pass

NIVEAUX_AUTORISES = ['Licence 1', 'Licence 2', 'Master 1']
```

### Debugging

#### Activer le mode debug

```python
# Dans app.py
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

#### Vérifier la santé de l'application

```bash
curl http://localhost:5000/sante
```

Réponse attendue :
```json
{
  "statut": "sain",
  "base_de_donnees": "connectée",
  "message": "L'application fonctionne correctement"
}
```

---

## 🚀 Déploiement

### Option 1 : Application Portable (Desktop)

#### Avec PyInstaller

```bash
# Installer PyInstaller
pip install pyinstaller

# Créer l'exécutable
pyinstaller --onefile --add-data "data;data" --add-data "templates;templates" --add-data "static;static" app.py
```

L'exécutable sera dans le dossier `dist/`.

### Option 2 : Déploiement sur PythonAnywhere

1. **Créer un compte** sur [PythonAnywhere](https://www.pythonanywhere.com)

2. **Uploader le code**
   ```bash
   git clone https://github.com/VOTRE_USERNAME/projet_mr_koffi.git
   ```

3. **Installer les dépendances**
   ```bash
   pip install --user -r requirements.txt
   ```

4. **Configurer le fichier WSGI**
   ```python
   import sys
   path = '/home/VOTRE_USERNAME/projet_mr_koffi'
   if path not in sys.path:
       sys.path.append(path)
   
   from app import app as application
   ```

5. **Configurer `.env` pour production**
   ```env
   ENVIRONNEMENT_FLASK=production
   UTILISER_SQLITE=False
   HOTE_MYSQL=VOTRE_USERNAME.mysql.pythonanywhere-services.com
   UTILISATEUR_MYSQL=VOTRE_USERNAME
   MOT_DE_PASSE_MYSQL=votre_mot_de_passe
   NOM_DB_MYSQL=VOTRE_USERNAME$gestion_enseignement
   CLE_SECRETE=cle_secrete_production_tres_longue
   ```

6. **Recharger l'application** depuis le dashboard PythonAnywhere

### Option 3 : Serveur Linux (Ubuntu)

```bash
# Installer les dépendances système
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx

# Cloner le projet
git clone https://github.com/VOTRE_USERNAME/projet_mr_koffi.git
cd projet_mr_koffi

# Créer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Installer Gunicorn
pip install gunicorn

# Lancer avec Gunicorn
gunicorn --bind 0.0.0.0:5000 wsgi:app
```

---

## ❓ FAQ

### Q1 : Comment changer le port de l'application ?

**R :** Modifiez le fichier `app.py` :

```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)  # Changez 5000 en 8080
```

### Q2 : Comment réinitialiser la base de données ?

**R :** Supprimez le fichier `data/gestion.db` et relancez l'application. Les tables seront recréées automatiquement.

```bash
# Sur Windows
del data\gestion.db

# Sur Linux/Mac
rm data/gestion.db
```

### Q3 : Comment passer de SQLite à MySQL ?

**R :** Modifiez le fichier `.env` :

```env
ENVIRONNEMENT_FLASK=production
UTILISER_SQLITE=False
HOTE_MYSQL=localhost
UTILISATEUR_MYSQL=root
MOT_DE_PASSE_MYSQL=votre_mot_de_passe
NOM_DB_MYSQL=gestion_enseignement
```

### Q4 : L'application ne démarre pas, que faire ?

**R :** Vérifiez :

1. Python est bien installé : `python --version`
2. L'environnement virtuel est activé
3. Les dépendances sont installées : `pip install -r requirements.txt`
4. Le fichier `.env` est correctement configuré
5. Consultez les logs d'erreur dans le terminal

### Q5 : Comment sauvegarder mes données ?

**R :** 

- **SQLite** : Copiez le fichier `data/gestion.db`
- **MySQL** : Utilisez `mysqldump`

```bash
# Backup SQLite
cp data/gestion.db data/gestion_backup_$(date +%Y%m%d).db

# Backup MySQL
mysqldump -u root -p gestion_enseignement > backup.sql
```

### Q6 : Comment ajouter un nouveau niveau (ex: Doctorat 2) ?

**R :** Modifiez les templates où les niveaux sont listés :

```html
<!-- Dans templates/modules/ajouter.html -->
<select name="niveau">
    <option value="Licence 1">Licence 1</option>
    <!-- ... -->
    <option value="Doctorat 2">Doctorat 2</option>  <!-- Ajouter ici -->
</select>
```

### Q7 : Comment personnaliser les couleurs de l'interface ?

**R :** Modifiez le fichier `static/css/style.css` :

```css
:root {
  --couleur-principale: #1e40af;  /* Changez cette valeur */
  --couleur-accent: #3b82f6;
  /* ... */
}
```

---

## 📞 Support et Contact

Pour toute question ou problème :

- **Email** : support@exemple.com
- **GitHub Issues** : [Créer une issue](https://github.com/VOTRE_USERNAME/projet_mr_koffi/issues)

---

## 📄 Licence

© 2024 Mr Koffi Elise - Tous droits réservés

---

## 🙏 Remerciements

- **Flask** : Framework web Python
- **Bootstrap** : Framework CSS
- **SQLite** : Base de données légère
- **Pandas** : Traitement de données pour les exports
- **ReportLab** : Génération de PDF

---

**Dernière mise à jour** : Décembre 2025
**Version** : 2.0.0 (Architecture Professionnelle)