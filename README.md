# 🎓 Gestion d'Enseignement - Application Web

Application web Flask pour la gestion des établissements scolaires, modules et paiements.

## 🌟 Fonctionnalités

- ✅ Gestion des établissements scolaires
- ✅ Gestion des modules par niveau
- ✅ Suivi des paiements
- ✅ Génération de rapports financiers
- ✅ Export Excel et PDF
- ✅ Interface utilisateur moderne et responsive

## 🚀 Déploiement

Cette application est optimisée pour le déploiement sur **PythonAnywhere**.

📖 **Consultez le guide complet** : [DEPLOIEMENT_PYTHONANYWHERE.md](DEPLOIEMENT_PYTHONANYWHERE.md)

## 💻 Installation locale (développement)

### Prérequis

- Python 3.8+
- MySQL (ou SQLite pour les tests)

### Installation

1. Clonez le repository :
```bash
git clone https://github.com/VOTRE_USERNAME/projet_mr_koffi.git
cd projet_mr_koffi
```

2. Créez un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

4. Configurez les variables d'environnement :
```bash
cp .env.example .env
# Éditez .env avec vos paramètres
```

5. Initialisez la base de données :
```bash
# Pour MySQL
mysql -u root -p < schema_final_utf8.sql

# Pour SQLite (tests locaux)
sqlite3 gestion_enseignement.db < schema_final_utf8.sql
```

6. Lancez l'application :
```bash
python app.py
```

7. Accédez à l'application :
```
http://localhost:5000
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

## 🗄️ Base de données

L'application supporte deux types de bases de données :

- **MySQL** : Pour la production (PythonAnywhere, Railway, etc.)
- **SQLite** : Pour les tests locaux

Configuration via variables d'environnement dans `.env`.

## 🔐 Sécurité

- ✅ Clé secrète Flask configurée
- ✅ Mots de passe stockés de manière sécurisée
- ✅ Protection CSRF
- ✅ Variables d'environnement pour les informations sensibles

## 📊 Endpoints

- `/` - Page d'accueil
- `/ecoles` - Gestion des établissements
- `/module/<id>/paiements` - Gestion des paiements
- `/health` - Vérification de l'état de l'application

## 🛠️ Technologies utilisées

- **Backend** : Flask 3.1.2
- **Base de données** : MySQL / SQLite
- **Frontend** : HTML, CSS, JavaScript
- **Export** : ReportLab (PDF), XlsxWriter (Excel)
- **Déploiement** : PythonAnywhere

## 📝 Licence

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