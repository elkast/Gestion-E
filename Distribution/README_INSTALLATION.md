# Guide d'Installation - Application Desktop

## Gestion Enseignement Mr Koffi Elise - Version EXE

---

## 🚀 Installation Rapide

### Pour l'Utilisateur Final

**C'EST TRÈS SIMPLE !**

1. **Extraire** le fichier ZIP
2. **Double-cliquer** sur `GestionEnseignement.exe`
3. **C'est tout !** ✅

**AUCUNE INSTALLATION REQUISE !**

---

## 📋 Prérequis

### Version EXE (Recommandée)
- ✅ **Aucun prérequis** - Fonctionne directement
- ✅ Windows 10/11
- ✅ ~100 MB d'espace disque

### Version Python (Alternative)
- Python 3.8 ou supérieur
- Télécharger depuis : https://www.python.org/downloads/
- **IMPORTANT** : Cocher "Add Python to PATH" lors de l'installation

---

## 💻 Utilisation

### Démarrage de l'Application

**Version EXE :**
```
Double-clic sur : GestionEnseignement.exe
```

**Version Python :**
```
Double-clic sur : lancer_application.bat
```

L'application s'ouvrira automatiquement dans votre navigateur.

---

## 📊 Fonctionnalités

### Gestion des Établissements
- ✅ Ajouter, modifier, supprimer des écoles
- ✅ Suivre les volumes par niveau
- ✅ États financiers par école

### Gestion des Modules
- ✅ Créer des modules d'enseignement
- ✅ Calculs automatiques des montants
- ✅ Volumes horaires (CM, TD, TP)
- ✅ Années universitaires automatiques (10 ans)

### Gestion des Paiements
- ✅ Enregistrer les paiements
- ✅ Références automatiques
- ✅ Validation des montants (pas de dépassement)
- ✅ Suivi du reste à payer
- ✅ Colonne "Reste" dans le tableau

### Exports
- ✅ Export Excel avec formatage
- ✅ Export PDF des rapports
- ✅ États financiers détaillés

---

## 💾 Sauvegarde des Données

### Emplacement
Vos données sont stockées dans : `data/gestion.db`

### Pour Sauvegarder
1. Copier le fichier `data/gestion.db`
2. Coller dans un endroit sûr (clé USB, cloud, etc.)

### Pour Restaurer
1. Remplacer `data/gestion.db` par votre sauvegarde

**IMPORTANT** : Sauvegardez régulièrement ce fichier !

---

## 🔧 Résolution de Problèmes

### L'application ne démarre pas

**Solution 1 :** Vérifier l'antivirus
- L'EXE peut être détecté comme suspect (faux positif)
- Ajouter une exception dans l'antivirus

**Solution 2 :** Vérifier les permissions
- Clic droit sur l'EXE → Propriétés → Débloquer

**Solution 3 :** Lancer en mode administrateur
- Clic droit sur l'EXE → Exécuter en tant qu'administrateur

### L'application est lente au démarrage

**Normal !** La première fois, l'EXE extrait les fichiers temporaires.
Les lancements suivants seront plus rapides (2-5 secondes).

### Le port 5000 est déjà utilisé

**Solution :** Fermer les autres applications Flask ou redémarrer l'ordinateur.

### Erreur "Module not found"

**Solution :** Utiliser la version EXE (tous les modules sont inclus).

---

## 📱 Compatibilité

### Systèmes d'Exploitation
- ✅ Windows 10
- ✅ Windows 11
- ✅ Windows 8.1
- ⚠️ Windows 7 (peut nécessiter des mises à jour)

### Navigateurs
- ✅ Chrome
- ✅ Firefox
- ✅ Edge
- ✅ Safari

---

## 🔒 Sécurité

### Données
- Stockées localement sur votre ordinateur
- Aucune connexion internet requise
- Pas de transmission de données

### Antivirus
- L'EXE peut être détecté comme suspect
- C'est un **faux positif** courant avec PyInstaller
- L'application est 100% sûre

---

## 📞 Support

### Documentation
- `LIRE_MOI.txt` - Guide rapide
- `GUIDE_COMPLET_DISTRIBUTION.md` - Guide détaillé
- `schema.sql` - Schéma de la base de données

### En Cas de Problème
1. Vérifier l'antivirus
2. Lancer en mode administrateur
3. Vérifier les permissions
4. Contacter l'administrateur

---

## ✨ Nouveautés

### Version 1.0

✅ **Validation des Paiements**
- Impossible de dépasser le montant restant
- Message d'erreur clair

✅ **Références Automatiques**
- Génération automatique si champ vide
- Format : PAY-{module}-{numéro}-{timestamp}

✅ **Colonne "Reste"**
- Affichage du reste à payer après chaque paiement
- Calcul automatique

✅ **Années Universitaires**
- Génération automatique de 10 années
- Sélection de l'année actuelle par défaut

✅ **Application EXE**
- Aucune installation Python requise
- Portable et professionnel

---

## 🎯 Utilisation Quotidienne

### Workflow Typique

1. **Lancer l'application**
   - Double-clic sur l'EXE

2. **Ajouter un établissement** (si nouveau)
   - Menu "Établissements" → Ajouter

3. **Créer un module**
   - Menu "Nouveau Module"
   - Remplir les informations
   - Les calculs se font automatiquement

4. **Enregistrer les paiements**
   - Cliquer sur "Paiements" d'un module
   - Ajouter un paiement
   - La référence se génère automatiquement

5. **Exporter les données**
   - Menu "Export" → Excel ou PDF

6. **Sauvegarder** (régulièrement)
   - Copier `data/gestion.db`

---

## 📊 Conseils d'Utilisation

### Bonnes Pratiques

✅ **Sauvegarde** : Sauvegarder `data/gestion.db` chaque semaine
✅ **Nomenclature** : Utiliser des noms clairs pour les modules
✅ **Vérification** : Vérifier les montants avant validation
✅ **Export** : Exporter régulièrement en Excel pour archivage

### À Éviter

❌ Ne pas supprimer le dossier `data/`
❌ Ne pas modifier manuellement `gestion.db`
❌ Ne pas lancer plusieurs instances en même temps

---

## 🔄 Mise à Jour

Pour mettre à jour vers une nouvelle version :

1. **Sauvegarder** `data/gestion.db`
2. **Extraire** la nouvelle version
3. **Copier** votre `gestion.db` dans le nouveau dossier `data/`
4. **Lancer** la nouvelle version

---

## 📝 Informations Techniques

### Taille de l'Application
- **EXE** : ~80-120 MB
- **Données** : Variable selon utilisation

### Technologies
- **Backend** : Flask (Python)
- **Base de données** : SQLite
- **Frontend** : HTML, CSS, Bootstrap 5
- **Exports** : pandas, xlsxwriter, reportlab

### Performance
- **Démarrage** : 2-5 secondes
- **Utilisation** : Rapide et fluide
- **Fonctionne hors ligne** : Oui

---

## ✅ Checklist Premier Démarrage

- [ ] Extraire le ZIP
- [ ] Double-cliquer sur GestionEnseignement.exe
- [ ] Vérifier que l'application s'ouvre
- [ ] Ajouter un établissement de test
- [ ] Créer un module de test
- [ ] Enregistrer un paiement de test
- [ ] Tester l'export Excel
- [ ] Sauvegarder data/gestion.db

---

✨ **Bienvenue dans Gestion Enseignement !**

L'application est prête à l'emploi. Bon travail ! 🎓