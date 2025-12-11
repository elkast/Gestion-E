# 🎓 Gestion d'Enseignement - Application Web

[![Flask](https://img.shields.io/badge/Flask-3.1.2-blue.svg)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Private-red.svg)]()

Application web moderne développée avec Flask pour la gestion complète des établissements scolaires, modules d'enseignement et suivi des paiements. Optimisée pour le déploiement en production sur PythonAnywhere.

## 🌟 Fonctionnalités Principales

### 📚 Gestion des Établissements Scolaires
- ✅ Ajout, modification et suppression d'établissements
- ✅ Gestion des informations détaillées (nom, type, ville, contact)
- ✅ Suivi des volumes horaires par niveau (CM, TD, TP)

### 🎓 Gestion des Modules
- ✅ Création de modules avec calculs automatiques des volumes et montants
- ✅ Gestion par niveaux académiques (Licence 1-3, Master 1-2, Doctorat)
- ✅ Calcul automatique des tarifs horaires et totaux
- ✅ Modification et suppression de modules

### 💰 Suivi des Paiements
- ✅ Enregistrement des paiements par module
- ✅ Calcul automatique du statut (partiel, complet, excédent)
- ✅ Gestion des types de paiement et références
- ✅ Historique complet des transactions

### 📊 Rapports et Exports
- ✅ Tableaux de bord avec statistiques financières
- ✅ Rapports financiers par établissement
- ✅ Export Excel avec données complètes
- ✅ Export PDF pour les rapports

### 🎨 Interface Utilisateur
- ✅ Design moderne et responsive
- ✅ Interface intuitive avec navigation fluide
- ✅ Messages de feedback utilisateur
- ✅ Gestion des erreurs et validations

## 🚀 Déploiement

Cette application est optimisée pour le déploiement sur **PythonAnywhere**.

## 💻 Installation et Configuration

### Prérequis Système

- **Python** : Version 3.8 ou supérieure
- **Base de données** :
  - MySQL 5.7+ (recommandé pour production)
  - SQLite 3+ (pour développement/tests locaux)
- **Mémoire** : Minimum 512MB RAM
- **Espace disque** : 100MB libre

### 🚀 Installation Rapide

```bash
# 1. Cloner le repository
git clone https://github.com/VOTRE_USERNAME/projet_mr_koffi.git
cd projet_mr_koffi

# 2. Créer l'environnement virtuel
python -m venv venv

# 3. Activer l'environnement virtuel
# Sur Linux/Mac :
source venv/bin/activate
# Sur Windows :
venv\Scripts\activate

# 4. Installer les dépendances
pip install -r requirements.txt

# 5. Configurer les variables d'environnement
cp .env .env.local  # Copier le fichier .env existant
# Éditer .env.local avec vos paramètres locaux

# 6. Lancer l'application
python app.py
```

### 🔧 Configuration Détaillée

#### Variables d'Environnement (.env)

```bash
# Configuration de la base de données
USE_SQLITE=True                    # True pour SQLite, False pour MySQL
SQLITE_DB=gestion_enseignement.db  # Chemin vers la DB SQLite

# Configuration MySQL (si USE_SQLITE=False)
MYSQL_HOST=localhost
MYSQL_USER=votre_utilisateur
MYSQL_PASSWORD=votre_mot_de_passe
MYSQL_DB=gestion_enseignement
MYSQL_PORT=3306

# Configuration Flask
SECRET_KEY=votre_cle_secrete_unique
FLASK_DEBUG=True                   # True pour développement
FLASK_ENV=development

# Sécurité
SESSION_COOKIE_SECURE=False        # True en production HTTPS
```

#### Base de Données

**Pour MySQL (Production) :**
```sql
CREATE DATABASE gestion_enseignement CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-- Créer les tables selon le schéma de l'application
```

**Pour SQLite (Développement) :**
- La base de données est créée automatiquement au premier lancement
- Fichier : `gestion_enseignement.db`

### 🌐 Accès à l'Application

Une fois lancée, l'application est accessible sur :
- **Développement** : http://localhost:5000
- **Production** : Selon votre configuration de déploiement

### 🏥 Vérification du Fonctionnement

Testez l'endpoint de santé :
```bash
curl http://localhost:5000/health
```

Réponse attendue :
```json
{
  "status": "healthy",
  "database": "connected",
  "message": "Application is running correctly"
}
```

## 📁 Structure du projet

```
projet_mr_koffi/
├── app.py                          # Point d'entrée de l'application
├── wsgi.py                         # Configuration WSGI pour PythonAnywhere
├── config.py                       # Configuration de l'application
├── requirements.txt                # Dépendances Python
├── .env.example                    # Exemple de configuration
├── blueprints/                     # Modules de l'application
│   ├── __init__.py
│   ├── db.py                       # Gestion de la base de données
│   ├── principal.py                # Routes principales
│   ├── ecoles.py                   # Gestion des écoles
│   └── paiements.py                # Gestion des paiements
├── templates/                      # Templates HTML
│   ├── index.html
│   ├── ecoles.html
│   ├── paiements.html
│   └── ...
├── static/                         # Fichiers statiques (CSS, JS, images)
│   └── style.css
└── schema_final_utf8.sql           # Schéma de la base de données
```

## 🗄️ Base de Données

### Schéma des Tables

L'application utilise les tables suivantes :

- **`ecoles`** : Établissements scolaires (id, nom, type, ville, contact, téléphone)
- **`modules`** : Modules d'enseignement (id, nom, école, niveau, volumes horaires, tarifs)
- **`paiements`** : Transactions financières (id, module, montant, type, référence, date)
- **`ecole_niveau_volumes`** : Volumes par niveau et établissement

### Support Multi-Base de Données

| Aspect | MySQL (Production) | SQLite (Développement) |
|--------|-------------------|------------------------|
| **Performance** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Concurrency** | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Taille max** | Illimitée | 1GB |
| **Migration** | Manuel | Automatique |
| **Backup** | Outils dédiés | Copie fichier |

### Configuration

```python
# config.py - Configuration automatique
USE_SQLITE = os.environ.get('USE_SQLITE', 'True').lower() == 'true'
if USE_SQLITE:
    # Configuration SQLite
else:
    # Configuration MySQL avec PyMySQL
```

## 🔐 Sécurité et Conformité

### Mesures de Sécurité Implémentées

- **🔑 Authentification** : Sessions Flask sécurisées
- **🛡️ CSRF Protection** : Protection contre les attaques cross-site
- **🔒 Secrets Management** : Clés secrètes via variables d'environnement
- **✅ Input Validation** : Validation côté serveur pour tous les formulaires
- **🚫 SQL Injection** : Requêtes paramétrées avec placeholders
- **🍪 Session Security** : Cookies HttpOnly et SameSite configurés

### Conformité RGPD

- ✅ Données personnelles minimisées
- ✅ Pas de stockage de mots de passe (utilisation future possible)
- ✅ Logs d'accès pour audit
- ✅ Possibilité de suppression des données

## 🌐 API Endpoints

### Routes Principales

| Endpoint | Méthode | Description | Authentification |
|----------|---------|-------------|------------------|
| `GET /` | GET | Tableau de bord principal | - |
| `GET /health` | GET | Vérification santé application | - |
| `GET /ecoles` | GET | Liste des établissements | - |
| `POST /ajouter-ecole` | POST | Ajouter un établissement | - |
| `GET /module/<id>` | GET | Détails d'un module | - |
| `POST /ajouter-module` | POST | Créer un nouveau module | - |
| `GET /module/<id>/paiements` | GET | Historique paiements module | - |
| `POST /ajouter-paiement` | POST | Enregistrer un paiement | - |
| `GET /export/excel` | GET | Export données Excel | - |
| `GET /export/pdf` | GET | Export rapport PDF | - |

### Codes de Réponse

- **200** : Succès
- **404** : Ressource non trouvée
- **500** : Erreur serveur
- **503** : Service indisponible (DB)

## 🛠️ Stack Technologique

### Backend
- **Framework** : Flask 3.1.2
- **Werkzeug** : 3.1.3 (WSGI utility)
- **Jinja2** : 3.1.6 (Templating)
- **python-dotenv** : 1.0.1 (Configuration)

### Base de Données
- **MySQL** : PyMySQL 1.1.1
- **SQLite** : Inclus dans Python

### Data Processing & Export
- **pandas** : 2.3.3 (Manipulation données)
- **numpy** : 2.3.3 (Calculs numériques)
- **XlsxWriter** : 3.2.9 (Export Excel)
- **ReportLab** : 4.4.4 (Génération PDF)

### Déploiement
- **PythonAnywhere** : Hébergement recommandé
- **WSGI** : Interface serveur web
- **Gunicorn** : Serveur WSGI alternatif

### Développement
- **IDE** : VS Code recommandé
- **Version Control** : Git
- **Virtual Environment** : venv

## � Licence

Ce projet est sous licence privée.

## 👥 Auteur

Développé pour M. Koffi

## 🆘 Support

Pour toute question ou problème :
1. Consultez [DEPLOIEMENT_PYTHONANYWHERE.md](DEPLOIEMENT_PYTHONANYWHERE.md)
2. Vérifiez les logs d'erreur
3. Testez l'endpoint `/health`

---

**Version** : 2.0 - Web Application
**Dernière mise à jour** : 2025