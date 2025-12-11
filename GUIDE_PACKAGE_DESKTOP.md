# Guide de Packaging - Application Desktop

## Pour Envoyer l'Application à Quelqu'un

### Étape 1 : Préparer le Package

Créez un dossier ZIP contenant les fichiers suivants :

```
GestionEnseignement_MrKoffi/
├── lancer_application.bat          ⭐ LANCEUR PRINCIPAL
├── lancer_application.py
├── installer_dependances.bat
├── app.py
├── configuration.py
├── requirements.txt
├── schema.sql
├── .env
├── README_INSTALLATION.md          ⭐ GUIDE UTILISATEUR
├── blueprints/
│   ├── __init__.py
│   ├── db.py
│   ├── ecoles.py
│   ├── paiements.py
│   └── principal.py
├── database/
│   ├── __init__.py
│   └── connexion.py
├── static/
│   └── css/
│       └── style.css
└── templates/
    ├── ecoles/
    ├── modules/
    ├── paiements/
    └── principal/
```

### Étape 2 : Instructions pour l'Utilisateur Final

Incluez ces instructions dans le README :

1. **Installer Python 3.8+** depuis https://www.python.org/
   - ⚠️ IMPORTANT : Cocher "Add Python to PATH"

2. **Extraire le ZIP** dans un dossier

3. **Double-cliquer sur `lancer_application.bat`**
   - Les dépendances s'installeront automatiquement
   - L'application s'ouvrira dans le navigateur

### Étape 3 : Données

- Les données sont dans `data/gestion.db`
- Ce fichier se crée automatiquement au premier lancement
- **Sauvegarder ce fichier** = sauvegarder toutes les données

## Avantages de cette Solution

✅ **Portable** : Fonctionne sur n'importe quel PC Windows avec Python
✅ **Autonome** : Base de données SQLite intégrée
✅ **Simple** : Un seul fichier à lancer
✅ **Léger** : Pas de serveur externe nécessaire
✅ **Sécurisé** : Données stockées localement

## Alternative : Créer un Exécutable (Optionnel)

Pour créer un `.exe` qui ne nécessite pas Python :

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --add-data "templates;templates" --add-data "static;static" lancer_application.py
```

L'exécutable sera dans le dossier `dist/`

## Support Technique

### Problèmes Courants

**"Python n'est pas reconnu"**
→ Python n'est pas installé ou pas dans le PATH
→ Réinstaller Python en cochant "Add to PATH"

**"Module flask not found"**
→ Lancer `installer_dependances.bat`

**"Port 5000 déjà utilisé"**
→ Un autre programme utilise le port
→ Fermer les autres applications ou redémarrer

### Logs et Débogage

Les erreurs s'affichent dans la console Windows
Gardez la fenêtre ouverte pour voir les messages

---

## Checklist avant Envoi

- [ ] Tester l'application sur un PC propre
- [ ] Vérifier que tous les fichiers sont inclus
- [ ] Inclure le README_INSTALLATION.md
- [ ] Tester le lanceur .bat
- [ ] Vérifier que .env est configuré en mode portable
- [ ] S'assurer que data/ est vide (pas de données personnelles)