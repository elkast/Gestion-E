# 🚀 Démarrage Rapide - 5 Minutes

## Pour déployer sur PythonAnywhere

### 1️⃣ Créer un compte (2 min)

1. Allez sur [pythonanywhere.com](https://www.pythonanywhere.com)
2. Cliquez sur "Start running Python online in less than a minute!"
3. Créez un compte gratuit
4. Confirmez votre email

### 2️⃣ Télécharger les fichiers (1 min)

Dans PythonAnywhere, onglet "Files" :
1. Créez un dossier `projet_mr_koffi`
2. Téléchargez tous les fichiers SAUF :
   - ❌ `venv/`
   - ❌ `__pycache__/`
   - ❌ `.git/`

**Fichiers essentiels à télécharger** :
- ✅ `app.py`
- ✅ `wsgi.py`
- ✅ `config.py`
- ✅ `requirements.txt`
- ✅ Dossier `blueprints/`
- ✅ Dossier `templates/`
- ✅ Dossier `static/`
- ✅ `schema_final_utf8.sql`

### 3️⃣ Créer la base de données (1 min)

Onglet "Databases" :
1. Créez une base MySQL
2. Notez le nom : `YOUR_USERNAME$gestion_enseignement`
3. Définissez un mot de passe
4. Importez `schema_final_utf8.sql` via phpMyAdmin

### 4️⃣ Configurer l'application (1 min)

Onglet "Files", créez `.env` :
```env
USE_SQLITE=False
MYSQL_HOST=YOUR_USERNAME.mysql.pythonanywhere-services.com
MYSQL_USER=YOUR_USERNAME
MYSQL_PASSWORD=votre_mot_de_passe
MYSQL_DB=YOUR_USERNAME$gestion_enseignement
SECRET_KEY=votre_cle_secrete_aleatoire
FLASK_DEBUG=False
```

Générer une clé secrète dans la console Bash :
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### 5️⃣ Installer et lancer (30 sec)

Console Bash :
```bash
cd ~/projet_mr_koffi
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Onglet "Web" :
1. Add a new web app → Manual configuration → Python 3.10
2. WSGI file : Remplacez `YOUR_USERNAME` dans le contenu de `wsgi.py`
3. Virtualenv : `/home/YOUR_USERNAME/projet_mr_koffi/venv`
4. Static files : `/static/` → `/home/YOUR_USERNAME/projet_mr_koffi/static/`
5. Cliquez sur **Reload**

### ✅ C'est fait !

Visitez : `https://YOUR_USERNAME.pythonanywhere.com`

---

## 🆘 Problème ?

### Erreur 502
```bash
tail -f /var/log/YOUR_USERNAME.pythonanywhere.com.error.log
```

### Base de données
Vérifiez `.env` et testez :
```bash
mysql -u YOUR_USERNAME -p -h YOUR_USERNAME.mysql.pythonanywhere-services.com
```

---

## 📚 Documentation complète

Pour plus de détails, consultez :
- [DEPLOIEMENT_PYTHONANYWHERE.md](DEPLOIEMENT_PYTHONANYWHERE.md) - Guide complet
- [CHECKLIST_DEPLOIEMENT_WEB.md](CHECKLIST_DEPLOIEMENT_WEB.md) - Checklist détaillée
- [README.md](README.md) - Documentation générale