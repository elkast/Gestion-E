# 📚 Index de la Documentation

Bienvenue dans la documentation du projet **Gestion d'Enseignement** - Application Web.

---

## 🎯 Par où commencer ?

### Vous voulez déployer rapidement ?
👉 **[DEMARRAGE_RAPIDE.md](DEMARRAGE_RAPIDE.md)** - 5 minutes pour déployer

### Vous voulez comprendre le projet ?
👉 **[README.md](README.md)** - Vue d'ensemble du projet

### Vous voulez un guide détaillé ?
👉 **[DEPLOIEMENT_PYTHONANYWHERE.md](DEPLOIEMENT_PYTHONANYWHERE.md)** - Guide complet étape par étape

---

## 📖 Documentation disponible

### 🚀 Déploiement

| Document | Description | Temps de lecture |
|----------|-------------|------------------|
| **[DEMARRAGE_RAPIDE.md](DEMARRAGE_RAPIDE.md)** | Guide ultra-rapide (5 min) | ⏱️ 2 min |
| **[DEPLOIEMENT_PYTHONANYWHERE.md](DEPLOIEMENT_PYTHONANYWHERE.md)** | Guide complet avec explications | ⏱️ 15 min |
| **[CHECKLIST_DEPLOIEMENT_WEB.md](CHECKLIST_DEPLOIEMENT_WEB.md)** | Checklist point par point | ⏱️ 5 min |

### 📋 Informations générales

| Document | Description | Temps de lecture |
|----------|-------------|------------------|
| **[README.md](README.md)** | Documentation générale du projet | ⏱️ 5 min |
| **[RESUME_MIGRATION_WEB.md](RESUME_MIGRATION_WEB.md)** | Résumé de la migration Desktop → Web | ⏱️ 10 min |
| **[CHANGELOG_v1.0.md](CHANGELOG_v1.0.md)** | Historique des versions | ⏱️ 3 min |

### 🔧 Fichiers techniques

| Fichier | Description | Usage |
|---------|-------------|-------|
| **[.env.example](.env.example)** | Template de configuration | Copier en `.env` |
| **[.gitignore](.gitignore)** | Fichiers à ignorer par Git | Automatique |
| **[requirements.txt](requirements.txt)** | Dépendances Python | `pip install -r` |
| **[wsgi.py](wsgi.py)** | Configuration WSGI | PythonAnywhere |
| **[run_local.py](run_local.py)** | Script développement local | `python run_local.py` |

---

## 🗺️ Parcours recommandés

### Pour un déploiement rapide

1. **[DEMARRAGE_RAPIDE.md](DEMARRAGE_RAPIDE.md)** - Suivre les 5 étapes
2. **[.env.example](.env.example)** - Créer votre fichier `.env`
3. Déployer !

### Pour comprendre et déployer

1. **[README.md](README.md)** - Comprendre le projet
2. **[RESUME_MIGRATION_WEB.md](RESUME_MIGRATION_WEB.md)** - Comprendre les changements
3. **[DEPLOIEMENT_PYTHONANYWHERE.md](DEPLOIEMENT_PYTHONANYWHERE.md)** - Guide détaillé
4. **[CHECKLIST_DEPLOIEMENT_WEB.md](CHECKLIST_DEPLOIEMENT_WEB.md)** - Vérifier chaque étape

### Pour le développement local

1. **[README.md](README.md)** - Section "Installation locale"
2. **[.env.example](.env.example)** - Créer `.env` avec `USE_SQLITE=True`
3. **[run_local.py](run_local.py)** - Lancer l'application
4. Visiter `http://localhost:5000`

---

## 🎓 Guides par niveau

### Débutant
- ✅ Suivez **[DEMARRAGE_RAPIDE.md](DEMARRAGE_RAPIDE.md)**
- ✅ Utilisez la **[CHECKLIST_DEPLOIEMENT_WEB.md](CHECKLIST_DEPLOIEMENT_WEB.md)**

### Intermédiaire
- ✅ Lisez **[DEPLOIEMENT_PYTHONANYWHERE.md](DEPLOIEMENT_PYTHONANYWHERE.md)**
- ✅ Comprenez **[RESUME_MIGRATION_WEB.md](RESUME_MIGRATION_WEB.md)**

### Avancé
- ✅ Consultez tous les documents
- ✅ Modifiez `config.py` et `wsgi.py` selon vos besoins
- ✅ Optimisez la base de données

---

## 📂 Structure des fichiers

```
projet_mr_koffi/
│
├── 📚 DOCUMENTATION (vous êtes ici)
│   ├── INDEX_DOCUMENTATION.md          ← Vous êtes ici
│   ├── DEMARRAGE_RAPIDE.md             ← Démarrage rapide
│   ├── README.md                       ← Vue d'ensemble
│   ├── DEPLOIEMENT_PYTHONANYWHERE.md   ← Guide complet
│   ├── CHECKLIST_DEPLOIEMENT_WEB.md    ← Checklist
│   ├── RESUME_MIGRATION_WEB.md         ← Résumé migration
│   └── CHANGELOG_v1.0.md               ← Historique
│
├── ⚙️ CONFIGURATION
│   ├── .env.example                    ← Template config
│   ├── .gitignore                      ← Fichiers ignorés
│   ├── config.py                       ← Configuration app
│   ├── requirements.txt                ← Dépendances
│   └── wsgi.py                         ← WSGI PythonAnywhere
│
├── 🚀 APPLICATION
│   ├── app.py                          ← Point d'entrée
│   ├── run_local.py                    ← Dev local
│   ├── blueprints/                     ← Code source
│   ├── templates/                      ← Templates HTML
│   └── static/                         ← CSS, JS, images
│
└── 🗄️ BASE DE DONNÉES
    ├── schema_final_utf8.sql           ← Schéma MySQL
    ├── create_mysql_db.sql             ← Script création
    └── gestion_enseignement.db         ← SQLite (dev)
```

---

## ❓ Questions fréquentes

### Quel document lire en premier ?
👉 **[DEMARRAGE_RAPIDE.md](DEMARRAGE_RAPIDE.md)** si vous voulez déployer rapidement
👉 **[README.md](README.md)** si vous voulez comprendre le projet

### Comment déployer sur PythonAnywhere ?
👉 Suivez **[DEPLOIEMENT_PYTHONANYWHERE.md](DEPLOIEMENT_PYTHONANYWHERE.md)**

### Comment tester en local ?
👉 Voir section "Installation locale" dans **[README.md](README.md)**

### Quels fichiers télécharger sur PythonAnywhere ?
👉 Voir section "Fichiers essentiels" dans **[DEMARRAGE_RAPIDE.md](DEMARRAGE_RAPIDE.md)**

### Comment configurer la base de données ?
👉 Voir **[DEPLOIEMENT_PYTHONANYWHERE.md](DEPLOIEMENT_PYTHONANYWHERE.md)** - Étape 3

### J'ai une erreur 502, que faire ?
👉 Voir section "Dépannage" dans **[DEPLOIEMENT_PYTHONANYWHERE.md](DEPLOIEMENT_PYTHONANYWHERE.md)**

---

## 🆘 Besoin d'aide ?

1. Consultez la section "Dépannage" dans **[DEPLOIEMENT_PYTHONANYWHERE.md](DEPLOIEMENT_PYTHONANYWHERE.md)**
2. Vérifiez la **[CHECKLIST_DEPLOIEMENT_WEB.md](CHECKLIST_DEPLOIEMENT_WEB.md)**
3. Testez l'endpoint `/health` de votre application

---

## ✅ Checklist rapide

Avant de déployer, assurez-vous d'avoir :
- [ ] Lu au moins **[DEMARRAGE_RAPIDE.md](DEMARRAGE_RAPIDE.md)**
- [ ] Créé un compte PythonAnywhere
- [ ] Téléchargé tous les fichiers nécessaires
- [ ] Créé le fichier `.env` à partir de `.env.example`
- [ ] Créé la base de données MySQL
- [ ] Suivi la **[CHECKLIST_DEPLOIEMENT_WEB.md](CHECKLIST_DEPLOIEMENT_WEB.md)**

---

**Bonne chance avec votre déploiement ! 🚀**

**Version** : 2.0 - Web Application
**Dernière mise à jour** : 2025