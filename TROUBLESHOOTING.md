# 🔍 Guide de Dépannage Railway

## Erreur: "No module named 'main'"

### Cause
Railway cherche un module `main.py` au lieu de `app.py`

### Solutions (dans l'ordre)

#### Solution 1: Configuration Manuelle Railway (RECOMMANDÉ)
1. Allez dans Railway Dashboard
2. Sélectionnez votre service
3. Settings → Deploy
4. Dans "Start Command", entrez:
   ```
   gunicorn app:app --bind 0.0.0.0:$PORT
   ```
5. Cliquez sur "Save"
6. Redéployez

#### Solution 2: Vérifier les Fichiers
Assurez-vous que ces fichiers existent:
- ✅ `app.py` (pas `main.py`)
- ✅ `Procfile`
- ✅ `railway.toml`
- ✅ `nixpacks.toml`
- ✅ `requirements.txt`

#### Solution 3: Supprimer les Fichiers de Configuration
Parfois, trop de fichiers de configuration créent des conflits.

**Essayez de supprimer:**
```bash
rm nixpacks.toml
rm railway.toml
```

**Gardez seulement:**
- `Procfile`
- `requirements.txt`

**Puis dans Railway Dashboard → Settings → Deploy:**
- Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`

#### Solution 4: Créer un Alias
Si rien ne fonctionne, créez un fichier `main.py`:

```python
# main.py
from app import app

if __name__ == '__main__':
    app.run()
```

Puis changez le Procfile:
```
web: gunicorn main:app
```

## Erreur: "Worker failed to boot"

### Cause
Problème de connexion à la base de données

### Solution
1. Vérifiez les variables d'environnement dans Railway
2. Assurez-vous que le service MySQL est démarré
3. Testez la connexion:
   ```bash
   railway run python test_connection.py
   ```

## Erreur: "Application timeout"

### Cause
L'application prend trop de temps à démarrer

### Solution
1. Augmentez le timeout dans `railway.toml`:
   ```toml
   [deploy]
   healthcheckTimeout = 300
   ```

2. Ou simplifiez l'initialisation dans `app.py`

## Erreur: "Port already in use"

### Cause
Le port n'est pas correctement configuré

### Solution
Assurez-vous que votre commande utilise `$PORT`:
```
gunicorn app:app --bind 0.0.0.0:$PORT
```

## Commandes Utiles

### Voir les Logs en Temps Réel
```bash
railway logs
```

### Se Connecter au Service
```bash
railway shell
```

### Tester Localement
```bash
# Installer Railway CLI
npm i -g @railway/cli

# Se connecter
railway login

# Lier le projet
railway link

# Exécuter localement avec les variables Railway
railway run python app.py
```

## Checklist de Déploiement

Avant de déployer, vérifiez:

- [ ] `app.py` existe et contient `app = Flask(__name__)`
- [ ] `requirements.txt` contient toutes les dépendances
- [ ] `Procfile` contient `web: gunicorn app:app`
- [ ] Variables d'environnement configurées dans Railway
- [ ] Service MySQL créé et démarré
- [ ] Base de données importée (`database.sql`)
- [ ] `SECRET_KEY` défini dans les variables

## Contact Support Railway

Si rien ne fonctionne:
1. Railway Discord: https://discord.gg/railway
2. Railway Docs: https://docs.railway.app
3. Railway Status: https://status.railway.app

---

**Dernière mise à jour**: 27 Octobre 2025