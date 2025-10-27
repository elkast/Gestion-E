# 🎓 Système de Gestion d'Enseignement

Application Flask pour la gestion des modules d'enseignement, établissements et paiements.

## 🚀 Déploiement sur Railway

✅ **L'application est prête pour Railway!**

Consultez [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) pour le guide complet de déploiement.

### Démarrage Rapide

1. **Pousser vers Git**
   ```bash
   git add .
   git commit -m "Ready for Railway deployment"
   git push
   ```

2. **Configurer Railway**
   - Connectez votre dépôt à Railway
   - Ajoutez un service MySQL
   - Les variables d'environnement seront configurées automatiquement

3. **Déployer**
   - Railway déploie automatiquement!

## 💻 Installation Locale

### Prérequis
- Python 3.13+
- MySQL 5.7+ ou MariaDB 10+

### Installation

1. **Cloner le projet**
   ```bash
   git clone <votre-repo>
   cd projet_mr_koffi
   ```

2. **Créer un environnement virtuel**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer la base de données**
   ```bash
   # Créer la base de données
   mysql -u root -p
   CREATE DATABASE gestion_enseignement;
   exit;
   
   # Importer le schéma
   mysql -u root -p gestion_enseignement < database.sql
   ```

5. **Configurer les variables d'environnement**
   ```bash
   # Copier le fichier exemple
   cp .env.example .env
   
   # Éditer .env avec vos informations
   ```

6. **Tester la connexion**
   ```bash
   python test_connection.py
   ```

7. **Lancer l'application**
   ```bash
   python app.py
   ```

   L'application sera accessible sur http://localhost:5000

## 📁 Structure du Projet

```
projet_mr_koffi/
├── app.py                    # Application Flask principale
├── config.py                 # Configuration
├── requirements.txt          # Dépendances Python
├── Procfile                  # Configuration Railway
├── nixpacks.toml            # Configuration build Railway
├── database.sql             # Schéma de base de données
├── test_connection.py       # Script de test MySQL
├── static/
│   └── style.css           # Styles CSS
└── templates/              # Templates HTML
    ├── index.html
    ├── ecoles.html
    ├── ajouter_module.html
    └── ...
```

## 🔧 Technologies

- **Backend**: Flask 3.1.2
- **Base de données**: MySQL avec PyMySQL
- **Serveur**: Gunicorn (production)
- **Frontend**: HTML, CSS, Bootstrap
- **Export**: Pandas, XlsxWriter, ReportLab

## 📊 Fonctionnalités

- ✅ Gestion des établissements (écoles/universités)
- ✅ Gestion des modules d'enseignement
- ✅ Gestion des volumes horaires (CM, TD, TP)
- ✅ Suivi des paiements
- ✅ États financiers par école
- ✅ Export Excel et PDF
- ✅ Tableau de bord avec statistiques

## 🔐 Sécurité

- Variables d'environnement pour les informations sensibles
- Clé secrète Flask pour les sessions
- Connexions MySQL sécurisées

## 📝 Documentation

- [Guide de Déploiement Railway](RAILWAY_DEPLOYMENT.md)
- [Historique des Corrections](RAILWAY_FIX.md)

## 🐛 Dépannage

### Erreur de connexion MySQL
```bash
# Vérifier que MySQL est démarré
# Windows
net start MySQL

# Linux
sudo systemctl start mysql

# Tester la connexion
python test_connection.py
```

### Erreur d'import
```bash
# Réinstaller les dépendances
pip install -r requirements.txt --force-reinstall
```

## 📞 Support

Pour toute question ou problème:
1. Consultez [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md)
2. Vérifiez les logs Railway
3. Testez localement avec `test_connection.py`

## 📄 Licence

Ce projet est sous licence privée.

---

**Dernière mise à jour**: 27 Octobre 2025