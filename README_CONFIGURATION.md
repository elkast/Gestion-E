# Configuration de la Base de Données

## ✅ Changements Appliqués

L'application utilise maintenant **SQLite par défaut** pour le développement local, ce qui élimine le besoin de configurer MySQL.

### Avantages
- ✅ **Pas de configuration requise** - L'application fonctionne immédiatement
- ✅ **Base de données locale** - Fichier `gestion_enseignement.db` créé automatiquement
- ✅ **Compatible MySQL** - Peut basculer vers MySQL pour la production
- ✅ **Pas de message d'erreur** - L'application démarre sans problème

## 🚀 Démarrage Rapide

### Développement Local (SQLite)
```bash
python app.py
```

L'application démarre sur `http://127.0.0.1:5000`

### Production (MySQL)
Pour utiliser MySQL en production, définissez la variable d'environnement :

```bash
# Windows PowerShell
$env:USE_SQLITE="False"
$env:MYSQL_HOST="votre-host"
$env:MYSQL_USER="votre-user"
$env:MYSQL_PASSWORD="votre-password"
$env:MYSQL_DB="votre-database"
$env:MYSQL_PORT="3306"

python app.py
```

```bash
# Linux/Mac
export USE_SQLITE=False
export MYSQL_HOST=votre-host
export MYSQL_USER=votre-user
export MYSQL_PASSWORD=votre-password
export MYSQL_DB=votre-database
export MYSQL_PORT=3306

python app.py
```

## 📁 Structure de la Base de Données

### Tables Créées Automatiquement (SQLite)

1. **ecoles** - Établissements d'enseignement
2. **modules** - Modules d'enseignement
3. **paiements** - Historique des paiements
4. **ecole_niveau_volumes** - Volumes par niveau et école

## 🔧 Configuration Avancée

### Fichier `config.py`

```python
class Config:
    # Utilise SQLite par défaut (True) ou MySQL (False)
    USE_SQLITE = os.environ.get('USE_SQLITE', 'True').lower() == 'true'
    
    # Chemin de la base SQLite
    SQLITE_DB = os.environ.get('SQLITE_DB', 'gestion_enseignement.db')
    
    # Configuration MySQL (pour production)
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'gestion_enseignement')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
```

## 🔄 Migration SQLite → MySQL

Pour migrer vos données de SQLite vers MySQL :

1. Exportez les données depuis SQLite
2. Créez la base MySQL
3. Importez les données
4. Changez `USE_SQLITE=False`

## 🛠️ Compatibilité

Le code est compatible avec les deux bases de données grâce à un système de conversion automatique des placeholders :
- SQLite utilise `?`
- MySQL utilise `%s`

Le système convertit automatiquement les requêtes selon la base utilisée.

## 📝 Notes Techniques

### Wrapper de Cursor SQLite
Un wrapper `PatchedSQLiteCursor` convertit automatiquement les placeholders MySQL (`%s`) en placeholders SQLite (`?`), permettant d'utiliser la même syntaxe SQL partout dans le code.

### Initialisation Automatique
Au premier démarrage avec SQLite, toutes les tables sont créées automatiquement avec le bon schéma.

## ❓ Dépannage

### L'application ne démarre pas
- Vérifiez que Python 3.x est installé
- Installez les dépendances : `pip install -r requirements.txt`

### Erreur de base de données
- Supprimez `gestion_enseignement.db` et redémarrez
- Les tables seront recréées automatiquement

### Basculer vers MySQL
- Définissez `USE_SQLITE=False`
- Configurez toutes les variables MySQL
- Assurez-vous que le serveur MySQL est accessible