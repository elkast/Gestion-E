# ✅ Checklist de Déploiement Web - PythonAnywhere

## 📋 Avant le déploiement

### Préparation des fichiers

- [ ] Tous les fichiers nécessaires sont présents
- [ ] Le fichier `.env` est créé à partir de `.env.example`
- [ ] Les dossiers inutiles sont supprimés (venv, __pycache__, dist, etc.)
- [ ] Le fichier `requirements.txt` contient uniquement les dépendances web
- [ ] Le fichier `wsgi.py` est configuré
- [ ] Le fichier `.gitignore` exclut les fichiers sensibles

### Vérification du code

- [ ] `app.py` ne contient plus de code desktop (pywebview)
- [ ] `config.py` charge les variables depuis `.env`
- [ ] Toutes les routes Flask fonctionnent en local
- [ ] L'endpoint `/health` retourne "healthy"
- [ ] Pas d'erreurs dans les logs

---

## 🌐 Déploiement sur PythonAnywhere

### 1. Compte et configuration initiale

- [ ] Compte PythonAnywhere créé
- [ ] Email confirmé
- [ ] Console Bash accessible

### 2. Téléchargement des fichiers

- [ ] Projet cloné via Git OU
- [ ] Fichiers téléchargés manuellement dans `/home/USERNAME/projet_mr_koffi/`
- [ ] Structure de dossiers vérifiée :
  - [ ] `app.py`
  - [ ] `wsgi.py`
  - [ ] `config.py`
  - [ ] `requirements.txt`
  - [ ] `.env`
  - [ ] `blueprints/`
  - [ ] `templates/`
  - [ ] `static/`
  - [ ] `schema_final_utf8.sql`

### 3. Base de données MySQL

- [ ] Base de données MySQL créée sur PythonAnywhere
- [ ] Nom de la base : `USERNAME$gestion_enseignement`
- [ ] Mot de passe MySQL défini
- [ ] Schéma importé (`schema_final_utf8.sql`)
- [ ] Tables créées avec succès
- [ ] Connexion testée depuis la console

### 4. Configuration de l'environnement

- [ ] Fichier `.env` créé avec les bonnes valeurs :
  - [ ] `USE_SQLITE=False`
  - [ ] `MYSQL_HOST=USERNAME.mysql.pythonanywhere-services.com`
  - [ ] `MYSQL_USER=USERNAME`
  - [ ] `MYSQL_PASSWORD=***`
  - [ ] `MYSQL_DB=USERNAME$gestion_enseignement`
  - [ ] `SECRET_KEY=***` (clé aléatoire générée)
  - [ ] `FLASK_DEBUG=False`
  - [ ] `FLASK_ENV=production`

### 5. Installation des dépendances

- [ ] Environnement virtuel créé : `python3 -m venv venv`
- [ ] Environnement activé : `source venv/bin/activate`
- [ ] Pip mis à jour : `pip install --upgrade pip`
- [ ] Dépendances installées : `pip install -r requirements.txt`
- [ ] Aucune erreur d'installation

### 6. Configuration de l'application Web

- [ ] Nouvelle Web App créée (Manual configuration)
- [ ] Python 3.10 ou 3.11 sélectionné
- [ ] Fichier WSGI configuré avec le bon username
- [ ] Virtual environment configuré : `/home/USERNAME/projet_mr_koffi/venv`
- [ ] Fichiers statiques configurés :
  - [ ] URL : `/static/`
  - [ ] Directory : `/home/USERNAME/projet_mr_koffi/static/`

### 7. Premier lancement

- [ ] Application rechargée (bouton "Reload")
- [ ] Site accessible : `USERNAME.pythonanywhere.com`
- [ ] Page d'accueil s'affiche correctement
- [ ] Endpoint `/health` retourne `{"status": "healthy"}`
- [ ] Aucune erreur 502 Bad Gateway

---

## 🧪 Tests post-déploiement

### Tests fonctionnels

- [ ] Page d'accueil accessible
- [ ] Liste des écoles s'affiche
- [ ] Ajout d'une école fonctionne
- [ ] Modification d'une école fonctionne
- [ ] Suppression d'une école fonctionne
- [ ] Gestion des modules fonctionne
- [ ] Gestion des paiements fonctionne
- [ ] Export Excel fonctionne
- [ ] Export PDF fonctionne

### Tests de sécurité

- [ ] `.env` n'est pas accessible publiquement
- [ ] Clé secrète changée (pas la valeur par défaut)
- [ ] Mode DEBUG désactivé (`FLASK_DEBUG=False`)
- [ ] Pas d'informations sensibles dans les logs

### Tests de performance

- [ ] Temps de chargement < 3 secondes
- [ ] Pas d'erreurs dans les logs
- [ ] Base de données répond correctement

---

## 📊 Surveillance et maintenance

### Logs à surveiller

- [ ] `/var/log/USERNAME.pythonanywhere.com.error.log`
- [ ] `/var/log/USERNAME.pythonanywhere.com.access.log`
- [ ] `/var/log/USERNAME.pythonanywhere.com.server.log`

### Sauvegardes

- [ ] Script de sauvegarde MySQL créé
- [ ] Tâche planifiée configurée (si compte payant)
- [ ] Sauvegarde manuelle effectuée

### Monitoring

- [ ] Endpoint `/health` vérifié régulièrement
- [ ] Alertes configurées (si disponible)

---

## 🔄 Mises à jour futures

### Procédure de mise à jour

1. [ ] Sauvegarder la base de données
2. [ ] Télécharger les nouveaux fichiers
3. [ ] Mettre à jour les dépendances : `pip install -r requirements.txt --upgrade`
4. [ ] Recharger l'application (bouton "Reload")
5. [ ] Tester les fonctionnalités

---

## ❌ Dépannage

### Erreur 502 Bad Gateway

- [ ] Vérifier les logs d'erreur
- [ ] Vérifier le fichier WSGI
- [ ] Vérifier que le virtual environment est correct
- [ ] Vérifier que toutes les dépendances sont installées

### Erreur de base de données

- [ ] Vérifier les informations dans `.env`
- [ ] Tester la connexion MySQL manuellement
- [ ] Vérifier que la base existe
- [ ] Vérifier les permissions

### Fichiers statiques ne chargent pas

- [ ] Vérifier la configuration "Static files"
- [ ] Vérifier que le dossier `static/` existe
- [ ] Vérifier les permissions du dossier

---

## 📝 Notes importantes

1. **Compte gratuit PythonAnywhere** :
   - Limité à 1 application web
   - Pas de HTTPS personnalisé
   - Pas de domaine personnalisé
   - Tâches planifiées limitées

2. **Compte payant recommandé pour** :
   - HTTPS personnalisé
   - Domaine personnalisé
   - Plusieurs applications
   - Tâches planifiées illimitées
   - Support prioritaire

3. **Sécurité** :
   - Ne jamais commiter le fichier `.env`
   - Changer la clé secrète en production
   - Désactiver le mode DEBUG
   - Faire des sauvegardes régulières

---

## ✅ Validation finale

- [ ] Application accessible publiquement
- [ ] Toutes les fonctionnalités testées
- [ ] Aucune erreur dans les logs
- [ ] Documentation à jour
- [ ] Sauvegarde effectuée
- [ ] Utilisateurs informés de la nouvelle URL

---

**Date de déploiement** : _______________
**URL de l'application** : https://USERNAME.pythonanywhere.com
**Version** : 2.0 - Web Application
**Status** : ✅ Déployé avec succès