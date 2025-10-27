# Déploiement sur Railway.com

## Problème résolu ✅

L'erreur `ImportError: libmariadb.so.3: cannot open shared object file` a été corrigée en remplaçant `flask-mysqldb` (qui nécessite des bibliothèques système C) par `PyMySQL` (client MySQL pur Python).

## Changements effectués

1. **requirements.txt** - Nettoyé et mis à jour avec PyMySQL au lieu de mysqlclient
2. **app.py** - Modifié pour utiliser PyMySQL avec gestion de connexion Flask
3. **nixpacks.toml** - Simplifié (plus besoin de packages système)
4. **config.py** - Ajout du support pour MYSQL_PORT

## Variables d'environnement à configurer sur Railway

Dans votre projet Railway, configurez ces variables d'environnement :

```
MYSQL_HOST=<votre_host_mysql>
MYSQL_USER=<votre_utilisateur>
MYSQL_PASSWORD=<votre_mot_de_passe>
MYSQL_DB=gestion_enseignement
MYSQL_PORT=3306
SECRET_KEY=<votre_cle_secrete_aleatoire>
PORT=5000
```

## Déploiement

1. Connectez votre dépôt GitHub à Railway
2. Railway détectera automatiquement qu'il s'agit d'une application Python
3. Configurez les variables d'environnement ci-dessus
4. Déployez !

## Base de données

Si vous n'avez pas encore de base de données MySQL sur Railway :

1. Ajoutez un service MySQL depuis le tableau de bord Railway
2. Railway fournira automatiquement les variables MYSQL_HOST, MYSQL_USER, etc.
3. Importez votre fichier database.sql dans la nouvelle base de données

## Test local

Pour tester localement avec les nouvelles modifications :

```bash
pip install -r requirements.txt
python app.py
```

L'application démarrera sur http://localhost:5000