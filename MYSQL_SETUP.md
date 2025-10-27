# 🗄️ Configuration MySQL sur Railway

## ✅ Problème Actuel

Votre application démarre correctement mais ne peut pas se connecter à MySQL:
```
ConnectionRefusedError: [Errno 111] Connection refused
Can't connect to MySQL server on 'localhost'
```

**Cause:** Les variables d'environnement MySQL ne sont pas configurées.

## 🚀 Solution (5 minutes)

### Étape 1: Ajouter MySQL à Railway

1. **Ouvrez votre projet Railway**
   - https://railway.app/dashboard

2. **Cliquez sur "+ New"**

3. **Sélectionnez "Database"**

4. **Choisissez "MySQL"**

5. **Railway va créer le service MySQL**
   - Attendez 1-2 minutes que MySQL démarre

### Étape 2: Vérifier les Variables

1. **Cliquez sur votre service d'application (pas MySQL)**

2. **Allez dans "Variables"**

3. **Vérifiez que ces variables existent:**
   ```
   MYSQL_HOST=<généré automatiquement>
   MYSQL_USER=<généré automatiquement>
   MYSQL_PASSWORD=<généré automatiquement>
   MYSQL_DB=<généré automatiquement>
   MYSQLPORT=<généré automatiquement>
   ```

4. **Si elles n'existent pas, ajoutez-les manuellement:**
   - Cliquez sur le service MySQL
   - Copiez les valeurs de connexion
   - Retournez à votre service d'application
   - Variables → + New Variable
   - Ajoutez chaque variable

5. **Ajoutez SECRET_KEY si manquant:**
   ```
   SECRET_KEY=votre_cle_secrete_aleatoire_123456789
   ```

### Étape 3: Importer la Base de Données

**Option A: Via Railway CLI (Recommandé)**
```bash
# Installer Railway CLI
npm i -g @railway/cli

# Se connecter
railway login

# Lier le projet
railway link

# Se connecter à MySQL
railway connect mysql

# Dans le shell MySQL, importer le schéma
source database.sql;

# Ou directement:
exit
```

**Option B: Via MySQL Client**
```bash
# Récupérer les credentials depuis Railway → MySQL → Connect
mysql -h <MYSQL_HOST> -u <MYSQL_USER> -p<MYSQL_PASSWORD> <MYSQL_DB> < database.sql
```

**Option C: Via Railway Web Interface**
1. Railway → MySQL service → Data
2. Cliquez sur "Query"
3. Copiez-collez le contenu de `database.sql`
4. Exécutez

### Étape 4: Redéployer

1. **Railway Dashboard → Votre service d'application**
2. **Deployments → ... → Redeploy**
3. **Attendez 1-2 minutes**

### Étape 5: Vérifier

1. **Ouvrez votre application**
2. **Vous devriez voir le tableau de bord**
3. **Ou visitez `/health` pour vérifier la connexion**

## 🔍 Vérification

### Test de Santé
Visitez: `https://votre-app.railway.app/health`

**Réponse attendue:**
```json
{
  "status": "healthy",
  "database": "connected",
  "message": "Application is running correctly"
}
```

### Logs
Dans Railway → Deployments → Logs, vous devriez voir:
```
[INFO] Starting gunicorn 23.0.0
[INFO] Listening at: http://0.0.0.0:8080
[INFO] Booting worker with pid: 4
```

**Sans erreurs de connexion!**

## ❌ Dépannage

### Erreur: "Connection refused"
- MySQL n'est pas démarré → Attendez 2 minutes
- Variables incorrectes → Vérifiez les variables

### Erreur: "Access denied"
- Mot de passe incorrect → Vérifiez MYSQL_PASSWORD
- Utilisateur incorrect → Vérifiez MYSQL_USER

### Erreur: "Unknown database"
- Base de données non créée → Importez database.sql
- Nom incorrect → Vérifiez MYSQL_DB

### Erreur: "Table doesn't exist"
- Schéma non importé → Importez database.sql

## 📊 Structure de la Base de Données

Après l'import, vous devriez avoir ces tables:
- `ecoles` - Établissements
- `modules` - Modules d'enseignement
- `paiements` - Paiements
- `ecole_niveau_volumes` - Volumes par niveau

## 🎯 Checklist Finale

- [ ] Service MySQL créé dans Railway
- [ ] Variables d'environnement configurées
- [ ] database.sql importé
- [ ] Application redéployée
- [ ] `/health` retourne "healthy"
- [ ] Page d'accueil fonctionne

## 📞 Support

Si vous avez des problèmes:
1. Vérifiez les logs Railway
2. Testez `/health`
3. Vérifiez les variables d'environnement
4. Consultez TROUBLESHOOTING.md

---

**Temps total: 5-10 minutes**
**Dernière mise à jour: 27 Octobre 2025**