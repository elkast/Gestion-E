de# 🚀 Guide de Déploiement sur PythonAnywhere

## 📋 Prérequis

1. Compte PythonAnywhere (gratuit ou payant)
2. Tous les fichiers de ce projet
3. Accès à la console Bash sur PythonAnywhere

---

## 🔧 Étape 1 : Créer un compte PythonAnywhere

1. Allez sur [www.pythonanywhere.com](https://www.pythonanywhere.com)
2. Créez un compte gratuit (Beginner Account)
3. Confirmez votre email

---

## 📤 Étape 2 : Télécharger les fichiers

### Option A : Via Git (Recommandé)

```bash
# Dans la console Bash de PythonAnywhere
cd ~
git clone https://github.com/VOTRE_USERNAME/projet_mr_koffi.git
cd projet_mr_koffi
```

### Option B : Téléchargement manuel

1. Allez dans l'onglet "Files" sur PythonAnywhere
2. Créez un dossier `projet_mr_koffi`
3. Téléchargez tous les fichiers du projet dans ce dossier

**Fichiers essentiels à télécharger :**
- `app.py`
- `wsgi.py`
- `config.py`
- `requirements.txt`
- `.env` (créé à partir de `.env.example`)
- Dossier `blueprints/` (tous les fichiers)
- Dossier `templates/` (tous les fichiers)
- Dossier `static/` (tous les fichiers)
- `schema_final_utf8.sql` (pour créer la base de données)

**Fichiers à NE PAS télécharger :**
- ❌ `venv/`
- ❌ `__pycache__/`
- ❌ `dist/`
- ❌ `new_dist/`
- ❌ `*.pyc`
- ❌ Fichiers `.bat` (Windows uniquement)

---

## 🗄️ Étape 3 : Configurer la base de données MySQL

### 3.1 Créer la base de données

1. Allez dans l'onglet "Databases" sur PythonAnywhere
2. Créez une nouvelle base de données MySQL
3. Notez le nom : `YOUR_USERNAME$gestion_enseignement`
4. Définissez un mot de passe MySQL

### 3.2 Importer le schéma

```bash
# Dans la console Bash
cd ~/projet_mr_koffi
mysql -u YOUR_USERNAME -p -h YOUR_USERNAME.mysql.pythonanywhere-services.com YOUR_USERNAME\$gestion_enseignement < schema_final_utf8.sql
```

Ou utilisez l'interface phpMyAdmin fournie par PythonAnywhere pour importer `schema_final_utf8.sql`.

---

## 🔐 Étape 4 : Configurer les variables d'environnement

1. Créez un fichier `.env` à partir de `.env.example` :

```bash
cd ~/projet_mr_koffi
cp .env.example .env
nano .env
```

2. Remplissez les valeurs :

```env
USE_SQLITE=False
MYSQL_HOST=YOUR_USERNAME.mysql.pythonanywhere-services.com
MYSQL_USER=YOUR_USERNAME
MYSQL_PASSWORD=votre_mot_de_passe_mysql
MYSQL_DB=YOUR_USERNAME$gestion_enseignement
MYSQL_PORT=3306

SECRET_KEY=generez_une_cle_secrete_aleatoire_ici
FLASK_DEBUG=False
FLASK_ENV=production
```

**Pour générer une clé secrète :**
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

---

## 📦 Étape 5 : Installer les dépendances

```bash
cd ~/projet_mr_koffi
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🌐 Étape 6 : Configurer l'application Web

1. Allez dans l'onglet "Web" sur PythonAnywhere
2. Cliquez sur "Add a new web app"
3. Choisissez "Manual configuration" (pas Flask)
4. Sélectionnez Python 3.10 ou 3.11

### 6.1 Configuration du WSGI file

1. Cliquez sur le lien du fichier WSGI
2. Supprimez tout le contenu
3. Remplacez par le contenu de votre `wsgi.py` en modifiant `YOUR_USERNAME` :

```python
import sys
import os

# Remplacez YOUR_USERNAME par votre nom d'utilisateur PythonAnywhere
project_home = '/home/YOUR_USERNAME/projet_mr_koffi'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.environ['USE_SQLITE'] = 'False'
os.environ['FLASK_DEBUG'] = 'False'

from app import app as application
```

### 6.2 Configuration du Virtual Environment

1. Dans l'onglet "Web", section "Virtualenv"
2. Entrez le chemin : `/home/YOUR_USERNAME/projet_mr_koffi/venv`

### 6.3 Configuration des fichiers statiques

Dans la section "Static files", ajoutez :

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/YOUR_USERNAME/projet_mr_koffi/static/` |

---

## ✅ Étape 7 : Tester et lancer

1. Cliquez sur le bouton vert "Reload" dans l'onglet Web
2. Visitez votre site : `YOUR_USERNAME.pythonanywhere.com`
3. Testez l'endpoint de santé : `YOUR_USERNAME.pythonanywhere.com/health`

---

## 🔍 Dépannage

### Erreur 502 Bad Gateway

```bash
# Vérifiez les logs d'erreur
tail -f /var/log/YOUR_USERNAME.pythonanywhere.com.error.log

# Vérifiez que les dépendances sont installées
cd ~/projet_mr_koffi
source venv/bin/activate
pip list
```

### Erreur de connexion à la base de données

1. Vérifiez les informations dans `.env`
2. Testez la connexion MySQL :

```bash
mysql -u YOUR_USERNAME -p -h YOUR_USERNAME.mysql.pythonanywhere-services.com
```

### Erreur d'import

```bash
# Vérifiez que le chemin est correct dans wsgi.py
cd ~/projet_mr_koffi
python3 -c "from app import app; print('OK')"
```

### Les fichiers statiques ne chargent pas

1. Vérifiez la configuration "Static files" dans l'onglet Web
2. Assurez-vous que le dossier `static/` existe et contient vos fichiers

---

## 🔄 Mise à jour de l'application

```bash
cd ~/projet_mr_koffi
git pull  # Si vous utilisez Git
# OU téléchargez les nouveaux fichiers manuellement

source venv/bin/activate
pip install -r requirements.txt --upgrade

# Rechargez l'application dans l'onglet Web (bouton Reload)
```

---

## 📊 Surveillance

### Logs

```bash
# Logs d'erreur
tail -f /var/log/YOUR_USERNAME.pythonanywhere.com.error.log

# Logs d'accès
tail -f /var/log/YOUR_USERNAME.pythonanywhere.com.access.log

# Logs du serveur
tail -f /var/log/YOUR_USERNAME.pythonanywhere.com.server.log
```

### Endpoint de santé

Visitez régulièrement : `https://YOUR_USERNAME.pythonanywhere.com/health`

---

## 🎯 Optimisations pour la production

### 1. Activer HTTPS (compte payant)

PythonAnywhere offre HTTPS gratuit sur les comptes payants.

### 2. Configurer un domaine personnalisé (compte payant)

1. Achetez un nom de domaine
2. Configurez-le dans l'onglet "Web" de PythonAnywhere

### 3. Sauvegardes automatiques

```bash
# Créez un script de sauvegarde
nano ~/backup_db.sh
```

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
mysqldump -u YOUR_USERNAME -p'YOUR_PASSWORD' -h YOUR_USERNAME.mysql.pythonanywhere-services.com YOUR_USERNAME\$gestion_enseignement > ~/backups/db_$DATE.sql
```

Configurez une tâche planifiée dans l'onglet "Tasks".

---

## 📝 Checklist finale

- [ ] Base de données MySQL créée et configurée
- [ ] Fichier `.env` créé avec les bonnes valeurs
- [ ] Dépendances installées (`requirements.txt`)
- [ ] Fichier WSGI configuré avec le bon username
- [ ] Virtual environment configuré
- [ ] Fichiers statiques configurés
- [ ] Application rechargée (bouton Reload)
- [ ] Site accessible via `YOUR_USERNAME.pythonanywhere.com`
- [ ] Endpoint `/health` retourne "healthy"
- [ ] Toutes les fonctionnalités testées

---

## 🆘 Support

- Documentation PythonAnywhere : https://help.pythonanywhere.com/
- Forums PythonAnywhere : https://www.pythonanywhere.com/forums/
- Documentation Flask : https://flask.palletsprojects.com/

---

**Version** : 2.0 - Web Application
**Date** : 2025
**Status** : ✅ Prêt pour déploiement web