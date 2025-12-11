# 🚀 Guide de Démarrage Rapide - Gestion d'Enseignement

## ⚡ Installation en 5 Minutes

### 1️⃣ Prérequis
- Python 3.8+ installé
- Terminal/PowerShell ouvert dans le dossier du projet

### 2️⃣ Installation

```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement (Windows)
venv\Scripts\activate

# Activer l'environnement (Linux/Mac)
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### 3️⃣ Configuration

Le fichier `.env` est déjà configuré pour le mode portable (SQLite).
Pas besoin de modifier quoi que ce soit !

### 4️⃣ Lancement

```bash
python app.py
```

L'application sera accessible sur : **http://localhost:5000**

---

## 📱 Utilisation Rapide

### Créer votre premier établissement

1. Ouvrir http://localhost:5000
2. Cliquer sur "Établissements" dans le menu
3. Cliquer sur "➕ Nouvel Établissement"
4. Remplir les informations et enregistrer

### Créer votre premier module

1. Cliquer sur "Nouveau Module" dans le menu
2. Remplir les informations :
   - Nom du module
   - Sélectionner l'établissement
   - Niveau (Licence 1, Master 1, etc.)
   - Volumes horaires (CM, TD, TP)
   - Tarifs horaires
3. Les calculs se font automatiquement !
4. Cliquer sur "Enregistrer"

### Enregistrer un paiement

1. Depuis le tableau de bord, cliquer sur "💰 Paiements" pour un module
2. Cliquer sur "➕ Nouveau Paiement"
3. Entrer le montant et la référence
4. Le statut est calculé automatiquement

---

## 🔧 Résolution de Problèmes

### L'application ne démarre pas

```bash
# Vérifier que Python est installé
python --version

# Vérifier que l'environnement virtuel est activé
# Vous devriez voir (venv) au début de votre ligne de commande

# Réinstaller les dépendances
pip install -r requirements.txt --force-reinstall
```

### Erreur de base de données

```bash
# Supprimer la base de données et la recréer
del data\gestion.db  # Windows
rm data/gestion.db   # Linux/Mac

# Relancer l'application
python app.py
```

### Port 5000 déjà utilisé

Modifier le port dans `app.py` :
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Changer 5000 en 8080
```

---

## 📚 Documentation Complète

Pour plus de détails, consultez [README_COMPLET.md](README_COMPLET.md)

---

## ✅ Checklist de Vérification

- [ ] Python 3.8+ installé
- [ ] Environnement virtuel créé et activé
- [ ] Dépendances installées (`pip install -r requirements.txt`)
- [ ] Fichier `.env` présent
- [ ] Application lancée (`python app.py`)
- [ ] Navigateur ouvert sur http://localhost:5000

---

## 🎯 Prochaines Étapes

1. ✅ Créer des établissements
2. ✅ Créer des modules
3. ✅ Enregistrer des paiements
4. ✅ Consulter les états financiers
5. ✅ Exporter les données (Excel/PDF)

---

**Besoin d'aide ?** Consultez le [README_COMPLET.md](README_COMPLET.md) pour plus de détails !