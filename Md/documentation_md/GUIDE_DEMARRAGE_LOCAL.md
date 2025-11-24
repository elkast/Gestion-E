# 🚀 Guide de Démarrage Rapide - Développement Local

## ✅ Problème résolu : Erreur MySQL

L'erreur que vous aviez :
```
pymysql.err.OperationalError: (2003, "Can't connect to MySQL server on 'YOUR_USERNAME.mysql.pythonanywhere-services.com'")
```

**Cause** : Le fichier `.env` était configuré pour MySQL (production) au lieu de SQLite (développement local).

**Solution appliquée** : Configuration automatique pour utiliser SQLite en local.

---

## 📋 Démarrage en 3 étapes

### 1️⃣ Vérifier que tout est installé

```bash
# Vérifier Python
python --version

# Activer l'environnement virtuel (si pas déjà activé)
venv\Scripts\activate

# Installer/mettre à jour les dépendances
pip install -r requirements.txt
```

### 2️⃣ Lancer l'application

**Option A : Utiliser le script de lancement (RECOMMANDÉ)**
```bash
python run_local.py
```

**Option B : Lancer directement**
```bash
python app.py
```

### 3️⃣ Accéder à l'application

Ouvrez votre navigateur et allez sur :
- **URL principale** : http://localhost:5000
- **Health check** : http://localhost:5000/health

---

## 🔧 Configuration

### Fichier `.env` (Développement Local)

Le fichier `.env` est maintenant configuré pour SQLite :

```env
USE_SQLITE=True
SQLITE_DB=gestion_enseignement.db
FLASK_DEBUG=True
FLASK_ENV=development
```

### Fichier `.env.production` (Pour PythonAnywhere)

Quand vous déployez sur PythonAnywhere, renommez `.env.production` en `.env` et remplissez :

```env
USE_SQLITE=False
MYSQL_HOST=VOTRE_USERNAME.mysql.pythonanywhere-services.com
MYSQL_USER=VOTRE_USERNAME
MYSQL_PASSWORD=VOTRE_MOT_DE_PASSE
MYSQL_DB=VOTRE_USERNAME$gestion_enseignement
```

---

## 📱 Design Responsive

L'application est maintenant **100% responsive** :

✅ **Desktop** (> 992px) : Interface complète avec tous les détails
✅ **Tablette** (768px - 992px) : Interface adaptée
✅ **Mobile** (< 768px) : Interface optimisée pour smartphone
✅ **Petit mobile** (< 576px) : Interface compacte

### Fonctionnalités responsive :
- Navigation adaptative
- Tableaux scrollables horizontalement sur mobile
- Boutons empilés verticalement sur petit écran
- Formulaires optimisés (pas de zoom automatique iOS)
- Cartes statistiques redimensionnées
- Textes et polices adaptés

---

## 🗂️ Structure des fichiers

```
projet_mr_koffi/
├── .env                    ← Configuration LOCALE (SQLite)
├── .env.example            ← Template pour local
├── .env.production         ← Template pour PythonAnywhere
├── app.py                  ← Application Flask principale
├── run_local.py            ← Script de lancement LOCAL
├── config.py               ← Configuration
├── requirements.txt        ← Dépendances Python
├── gestion_enseignement.db ← Base de données SQLite (LOCAL)
├── blueprints/             ← Code source
├── templates/              ← Pages HTML
└── static/
    └── style.css           ← CSS responsive
```

---

## 🔄 Différences Local vs Production

| Aspect | Local (Votre PC) | Production (PythonAnywhere) |
|--------|------------------|------------------------------|
| **Base de données** | SQLite | MySQL |
| **Fichier .env** | `USE_SQLITE=True` | `USE_SQLITE=False` |
| **Debug** | `FLASK_DEBUG=True` | `FLASK_DEBUG=False` |
| **Lancement** | `python run_local.py` | Configuré dans WSGI |
| **URL** | http://localhost:5000 | https://USERNAME.pythonanywhere.com |

---

## 🆘 Dépannage

### Erreur : "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Erreur : "Can't connect to MySQL"
Vérifiez que votre `.env` contient :
```env
USE_SQLITE=True
```

### L'application ne démarre pas
1. Vérifiez que le port 5000 n'est pas utilisé
2. Essayez de redémarrer votre terminal
3. Vérifiez que l'environnement virtuel est activé

### La base de données est vide
La base SQLite `gestion_enseignement.db` se créera automatiquement au premier lancement.
Si elle n'existe pas, importez le schéma :
```bash
sqlite3 gestion_enseignement.db < schema_final_utf8.sql
```

---

## 📝 Commandes utiles

```bash
# Activer l'environnement virtuel
venv\Scripts\activate

# Lancer l'application
python run_local.py

# Installer une nouvelle dépendance
pip install nom_package
pip freeze > requirements.txt

# Vérifier la santé de l'app
curl http://localhost:5000/health

# Arrêter le serveur
Ctrl + C
```

---

## ✅ Checklist avant de coder

- [ ] Environnement virtuel activé
- [ ] Dépendances installées (`pip install -r requirements.txt`)
- [ ] Fichier `.env` configuré pour SQLite
- [ ] Application lancée (`python run_local.py`)
- [ ] Navigateur ouvert sur http://localhost:5000
- [ ] Aucune erreur dans le terminal

---

## 🎯 Prochaines étapes

1. **Développer en local** avec SQLite
2. **Tester toutes les fonctionnalités**
3. **Quand prêt pour la production** :
   - Suivre [DEPLOIEMENT_PYTHONANYWHERE.md](DEPLOIEMENT_PYTHONANYWHERE.md)
   - Utiliser `.env.production` comme base
   - Configurer MySQL sur PythonAnywhere

---

**Bon développement ! 🚀**

Pour toute question, consultez :
- [README.md](README.md) - Documentation générale
- [DEPLOIEMENT_PYTHONANYWHERE.md](DEPLOIEMENT_PYTHONANYWHERE.md) - Déploiement production
- [INDEX_DOCUMENTATION.md](INDEX_DOCUMENTATION.md) - Index de toute la documentation