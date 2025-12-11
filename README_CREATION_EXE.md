# Guide de Création de l'Exécutable (EXE)

## Gestion Enseignement Mr Koffi Elise

### Prérequis

- Python 3.8 ou supérieur installé
- Toutes les dépendances installées (`pip install -r requirements.txt`)
- Connexion Internet (pour télécharger PyInstaller)

---

## Méthode 1 : Utiliser le Script BAT (Windows - Recommandé)

### Étapes :

1. **Double-cliquez sur** `creer_exe.bat`
2. **Attendez** que le processus se termine (2-5 minutes)
3. **Trouvez l'exécutable** dans le dossier `Distribution/`

C'est tout ! 🎉

---

## Méthode 2 : Utiliser le Script Python

### Étapes :

```bash
python creer_exe_simple.py
```

---

## Méthode 3 : Commande Manuelle

Si vous préférez créer l'exécutable manuellement :

```bash
# Installer PyInstaller
pip install pyinstaller

# Créer l'exécutable
pyinstaller --name="GestionEnseignement" ^
    --onefile ^
    --windowed ^
    --add-data "templates;templates" ^
    --add-data "static;static" ^
    --add-data ".env;." ^
    --hidden-import=flask ^
    --hidden-import=pymysql ^
    --hidden-import=pandas ^
    --hidden-import=xlsxwriter ^
    --hidden-import=reportlab ^
    lancer_application.py
```

L'exécutable sera dans le dossier `dist/`

---

## Distribution de l'Application

### Contenu du Package à Distribuer

Le dossier `Distribution/` contient :

```
Distribution/
├── GestionEnseignement.exe    ⭐ L'application
├── LIRE_MOI.txt                📖 Guide rapide
├── README_INSTALLATION.md      📖 Guide complet
├── schema.sql                  📄 Schéma de la BD
└── data/                       📁 (vide, créé automatiquement)
```

### Étapes de Distribution

1. **Compresser** le dossier `Distribution/` en ZIP
2. **Nommer** le ZIP : `GestionEnseignement_v1.0.zip`
3. **Envoyer** le ZIP à l'utilisateur

### Instructions pour l'Utilisateur Final

L'utilisateur doit :

1. **Extraire** le ZIP
2. **Double-cliquer** sur `GestionEnseignement.exe`
3. **C'est tout !** Aucune installation requise

---

## Avantages de l'EXE

✅ **Aucune installation Python requise**
✅ **Portable** - Fonctionne sur n'importe quel PC Windows
✅ **Simple** - Un seul fichier à lancer
✅ **Autonome** - Toutes les dépendances incluses
✅ **Professionnel** - Comme une vraie application

---

## Taille de l'Exécutable

- **Taille approximative** : 80-120 MB
- **Raison** : Inclut Python + Flask + toutes les dépendances
- **C'est normal** pour une application Python standalone

---

## Problèmes Courants

### "PyInstaller n'est pas reconnu"

**Solution** : Installer PyInstaller
```bash
pip install pyinstaller
```

### "Module not found" lors de l'exécution

**Solution** : Ajouter le module manquant avec `--hidden-import`
```bash
--hidden-import=nom_du_module
```

### L'antivirus bloque l'exécutable

**Solution** : 
- C'est un faux positif courant avec PyInstaller
- Ajouter une exception dans l'antivirus
- Ou signer l'exécutable avec un certificat

### L'application ne démarre pas

**Solution** :
1. Vérifier que le dossier `data/` existe
2. Vérifier les permissions d'écriture
3. Lancer depuis l'invite de commande pour voir les erreurs

---

## Mise à Jour de l'Application

Pour créer une nouvelle version :

1. Modifier le code source
2. Relancer `creer_exe.bat`
3. Redistribuer le nouveau ZIP

---

## Personnalisation

### Changer l'Icône

1. Créer un fichier `icon.ico`
2. Modifier le script :
```bash
--icon=icon.ico
```

### Changer le Nom

Modifier dans le script :
```bash
--name="VotreNom"
```

---

## Support Technique

### Logs et Débogage

Pour voir les erreurs, lancer depuis CMD :
```bash
GestionEnseignement.exe
```

Les erreurs s'afficheront dans la console.

---

## Alternatives

### Auto-Py-To-Exe (Interface Graphique)

Pour une interface graphique :
```bash
pip install auto-py-to-exe
auto-py-to-exe
```

Puis configurer visuellement les options.

---

## Checklist Avant Distribution

- [ ] Tester l'EXE sur un PC propre
- [ ] Vérifier que toutes les fonctionnalités marchent
- [ ] Inclure LIRE_MOI.txt
- [ ] Inclure README_INSTALLATION.md
- [ ] Vérifier la taille du ZIP (< 150 MB)
- [ ] Tester l'extraction et le lancement

---

✅ **Votre application est maintenant prête pour la distribution !**