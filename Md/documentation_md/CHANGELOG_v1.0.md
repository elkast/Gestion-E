# Changelog - Zen Faskk Desktop

## Version 1.0 - Corrections pour Déploiement Desktop

### 🐛 Corrections de Bugs

#### ✅ CRITIQUE : Erreur "signal only works in main thread" (RÉSOLU)
**Problème** :
```
ValueError: signal only works in main thread of the main interpreter
```

**Cause** :
- Flask lancé dans un thread séparé avec `debug=True` et `use_reloader=True`
- Sur Windows, les signaux (SIGTERM) ne peuvent être gérés que dans le thread principal
- Le reloader de Werkzeug tentait de configurer des gestionnaires de signaux dans un thread

**Solution appliquée** :
1. **app.py** - Ligne 71-78 :
   - Création d'une fonction `start_flask()` dédiée
   - Ajout de `debug=False` pour désactiver le mode debug
   - Ajout de `use_reloader=False` pour désactiver le reloader
   - Ajout de `threaded=True` pour supporter les requêtes concurrentes
   - Thread configuré en mode `daemon=True`
   - Ajout d'une pause de 1 seconde pour laisser Flask démarrer

2. **config.py** - Ligne 21 :
   - Changement de `DEBUG = 'True'` par défaut à `DEBUG = 'False'`
   - Permet de désactiver le debug même sans variable d'environnement

**Impact** :
- ✅ L'application démarre sans erreur sur Windows
- ✅ Compatible avec pywebview
- ✅ Prêt pour le déploiement desktop

### 📦 Nouveaux Fichiers de Déploiement

#### 1. `lancer_application.bat`
- Script de lancement automatique pour Windows
- Crée l'environnement virtuel si nécessaire
- Installe les dépendances automatiquement
- Lance l'application
- Gestion des erreurs avec messages clairs

#### 2. `verifier_installation.py`
- Vérifie la version de Python (minimum 3.8)
- Vérifie la présence de tous les fichiers requis
- Vérifie l'installation des dépendances
- Vérifie la base de données
- Affiche un rapport détaillé

#### 3. `LISEZMOI.txt`
- Guide d'installation simplifié pour utilisateurs finaux
- Instructions en 3 étapes
- Section dépannage
- Format texte brut pour compatibilité maximale

#### 4. `GUIDE_DEPLOIEMENT_DESKTOP.md`
- Documentation technique complète
- Instructions détaillées pour Option A (Python) et Option B (Exécutable)
- Résolution des problèmes courants
- Configuration pour production
- Notes importantes pour les développeurs

#### 5. `CHECKLIST_DEPLOIEMENT.md`
- Liste de contrôle complète avant déploiement
- Fichiers à inclure/exclure
- Étapes de préparation du package
- Tests à effectuer
- Documentation des corrections appliquées

#### 6. `creer_package_distribution.bat`
- Script automatique de création du package
- Copie tous les fichiers nécessaires
- Nettoie les fichiers temporaires
- Crée une archive ZIP prête à distribuer
- Génère un README d'installation

#### 7. `CHANGELOG_v1.0.md` (ce fichier)
- Historique des modifications
- Documentation des corrections
- Guide de migration

### 🔧 Modifications de Code

#### app.py
```python
# AVANT (ligne 72-73)
threading.Thread(target=app.run, kwargs={'host': '127.0.0.1', 'port': 5000}).start()

# APRÈS (ligne 71-78)
def start_flask():
    """Démarre le serveur Flask sans reloader ni debugger"""
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False, threaded=True)

flask_thread = threading.Thread(target=start_flask, daemon=True)
flask_thread.start()
time.sleep(1)  # Pause pour laisser Flask démarrer
```

#### config.py
```python
# AVANT (ligne 21)
DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'

# APRÈS (ligne 21)
DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
```

### 📋 Fichiers Modifiés

| Fichier | Changements | Impact |
|---------|-------------|--------|
| `app.py` | Fonction `start_flask()`, paramètres Flask | ✅ Critique - Corrige l'erreur signal |
| `config.py` | DEBUG=False par défaut | ✅ Important - Sécurité production |

### 📋 Nouveaux Fichiers

| Fichier | Type | Description |
|---------|------|-------------|
| `lancer_application.bat` | Script | Lancement automatique |
| `verifier_installation.py` | Script | Vérification pré-lancement |
| `LISEZMOI.txt` | Documentation | Guide utilisateur |
| `GUIDE_DEPLOIEMENT_DESKTOP.md` | Documentation | Guide technique |
| `CHECKLIST_DEPLOIEMENT.md` | Documentation | Liste de contrôle |
| `creer_package_distribution.bat` | Script | Création package |
| `CHANGELOG_v1.0.md` | Documentation | Ce fichier |

### 🚀 Instructions de Déploiement

#### Pour créer un package de distribution :
```batch
# Exécuter le script de création de package
creer_package_distribution.bat

# Cela créera :
# - Un dossier ZenFaskk_Desktop_v1.0/
# - Une archive ZenFaskk_Desktop_v1.0.zip
```

#### Pour installer sur un nouveau PC :
```batch
# 1. Extraire le ZIP
# 2. Double-cliquer sur lancer_application.bat
# 3. L'application s'ouvre automatiquement
```

### ⚠️ Notes Importantes

1. **Ne jamais activer `debug=True` avec pywebview sur Windows**
   - Cause l'erreur "signal only works in main thread"
   - Incompatible avec le threading

2. **Le reloader Flask ne fonctionne pas dans un thread**
   - Toujours utiliser `use_reloader=False` avec pywebview

3. **Base de données SQLite portable**
   - Le fichier `.db` peut être copié entre PCs
   - Sauvegarder régulièrement

4. **Python 3.8+ requis**
   - Versions antérieures non testées
   - Recommandé : Python 3.8 à 3.11

### 🔄 Migration depuis Version Précédente

Si vous avez une version antérieure :

1. **Sauvegarder la base de données**
   ```batch
   copy gestion_enseignement.db gestion_enseignement_backup.db
   ```

2. **Remplacer les fichiers**
   - `app.py` (IMPORTANT - contient la correction)
   - `config.py` (IMPORTANT - DEBUG désactivé)

3. **Tester**
   ```batch
   python verifier_installation.py
   python app.py
   ```

### 📞 Support

Pour toute question ou problème :
- Consulter `GUIDE_DEPLOIEMENT_DESKTOP.md`
- Exécuter `verifier_installation.py` pour diagnostiquer
- Vérifier ce changelog pour les corrections connues

---

**Version** : 1.0  
**Date** : 2025  
**Status** : ✅ Stable - Prêt pour production  
**Testé sur** : Windows 10/11, Python 3.8+