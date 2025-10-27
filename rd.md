Résumé global du système
Le système sert de cahier de gestion numérique pour enseignants :

Liste les modules (cours) à gérer

Permet de saisir le volume horaire (CM, TD, TP)

Calcule automatiquement montants et soldes

Suit l’historique des paiements

Architecture technique
Côté utilisateur	Côté serveur	Base de données
HTML/CSS/JavaScript	Flask (Python)	MS Access (.accdb)
Formulaires web	Gestion logique	Tables: Modules, Paiements
Tableaux de suivi	Calculs automatisés	Requêtes, relations
Les principales entités à gérer
1. Table MODULES
ID	Nom	École	Niveau	TarifHoraire	HeuresCM	HeuresTD	HeuresTP
1	Maths	Paris	L2	45	20	10	0
2	Physique	Lyon	M1	50	15	5	10
2. Table PAIEMENTS
ID	ModuleID	Date	Montant	Type
1	1	15/10/2024	500	Avance
2	2	20/10/2024	1125	Total
Fonctionnalités principales
Ajouter/modifier un module

Calcul automatique des totaux (heures, montant total, soldes)

Enregistrer les paiements (avance, solde)

Tableaux de bord synthétiques affichant tous les modules et soldes

Interface utilisateur (Web)
Page accueil : tableau général (module, école, heures, montant, avances, soldes)

Formulaire d’ajout : nom du module, volume horaire, tarif, etc.

Boutons : Ajouter, Modifier, Supprimer, Exporter (PDF/Excel)

Saisie des paiements et mise à jour immédiate des soldes

Comportements automatiques
Calcul : total_heures = heures_CM + heures_TD + heures_TP

Calcul : montant_total = total_heures × tarif_horaire

Calcul : solde_restant = montant_total - sommes des avances reçues

Plans UML recommandés
Diagramme de cas d’utilisation
Acteurs : Enseignant

Cas principaux :

Ajouter un module

Modifier un module

Saisir paiement

Générer rapport/export

Consulter synthèse

Diagramme de classes (exemple simplifié)
Classe	Attributs	Méthodes
Module	id, nom, école, niveau, tarif_horaire, heures	calculer_montant_total()
Paiement	id, module_id, date, montant, type	
Relations :

Un Module possède plusieurs Paiements

Diagramme de séquence
Processus "Ajout de module" : Interface → Flask → Base Access → Mise à jour Interface

Processus "Saisie paiement" : Interface → Flask → Base Access → Recalcul → Interface

Avantages
Simple et personnalisable

Calculs automatisés (pas d’erreur humaine)

Pas d’internet requis, confidentialité assurée

Données exportables facilement

Premiers pas
Démarrer l’application depuis le navigateur

Ajouter les modules et heures

Saisir les paiements reçus

Consulter et exporter les synthèses

Pour la partie UML, il est recommandé de :

Dessiner un diagramme de cas d’utilisation (enseignant, modules, paiements)

Proposer un diagramme de classes simple (Module, Paiement)

En option : compléter avec diagramme de séquence si nécessaire

Cette structure permet d’avoir un système clair, facilement évolutif et gérable par un utilisateur non technique.

 **diagramme de classes UML complet pour ce système**
 Plan UML : Diagramme de classes
text
┌────────────────────┐
│    Enseignant      │
├────────────────────┤
│+ id: int           │
│+ nom: string       │
│+ email: string     │
└───────┬────────────┘
        │
        │ 1..*
        │
┌───────▼────────────┐
│     Module         │
├────────────────────┤
│+ id: int           │
│+ nom: string       │
│+ ecole: string     │
│+ niveau: string    │
│+ tarifHoraire: float │
│+ heuresCM: int     │
│+ heuresTD: int     │
│+ heuresTP: int     │
│+ totalHeures():int │
│+ montantTotal():float │
└───────┬────────────┘
        │
        │ 1..*
        │
┌───────▼────────────┐
│    Paiement        │
├────────────────────┤
│+ id: int           │
│+ date: date        │
│+ montant: float    │
│+ type: string      │
│+ moduleId: int     │
└────────────────────┘
Explications essentielles
Enseignant : Peut gérer plusieurs Modules.

Module : Appartient à un enseignant, correspond à un cours spécifique, contient les informations sur les volumes horaires, le tarif, etc.

Paiement : Associé à un Module, représente soit une avance soit un paiement total.

Les méthodes comme totalHeures() et montantTotal() sont utilisées pour l’automatisation des calculs.


**Schéma de la base Access**
Table : Modules
Nom de la colonne	Type Access	Contraintes / Notes
ID	AutoNumber (Clé primaire)	Identifiant unique automatique
Nom	Short Text (255)	Obligatoire, nom du module
Ecole	Short Text (255)	Obligatoire, nom de l’école
Niveau	Short Text (100)	Optionnel, par exemple "Licence 2"
TarifHoraire	Currency	Obligatoire, tarif horaire du module (€/h)
HeuresCM	Number (Integer)	Heures de Cours Magistral
HeuresTD	Number (Integer)	Heures de Travaux Dirigés
HeuresTP	Number (Integer)	Heures de Travaux Pratiques
Contraintes supplémentaires :

TarifHoraire ≥ 0

HeuresCM, HeuresTD, HeuresTP ≥ 0

Table : Paiements
Nom de la colonne	Type Access	Contraintes / Notes
ID	AutoNumber (Clé primaire)	Identifiant unique automatique
ModuleID	Number (Long Integer)	Clé étrangère référencée à Modules.ID
Date	Date/Heure	Date de paiement
Montant	Currency	Montant payé, ≥ 0
Type	Short Text (50)	Exemple : "Avance", "Total", indication du type paiement
Contraintes supplémentaires :

ModuleID doit exister dans la table Modules (référentiel d’intégrité)

Montant ≥ 0

Relations
1 Module peut avoir plusieurs Paiements (relation un-à-plusieurs via ModuleID)

Clé primaire Modules.ID référencée par Paiements.ModuleID

Remarques complémentaires
Les calculs totaux (heures, montant total, soldes) sont réalisés côté application (Flask) via les données récupérées.

La base doit comporter des index sur les colonnes ID et ModuleID pour optimiser les requêtes.

La date de paiement peut être de type « Date/Heure courte ».

Utilisation de Currency pour marge de sécurité au niveau monétaire.

Ce schéma est conforme aux besoins d’une application pédagogique locale sécurisée, facilement interfacée avec Flask via un driver ODBC ou une bibliothèque compatible pour Access. La structuration est claire, normalisée et prête à évoluer selon vos besoins futurs.



**Guide d'installation local**

1. Préparer l'environnement
Installer Python 3 (version 3.8 ou supérieure recommandée).

Installer Microsoft Access ou Microsoft Access Runtime (pour pouvoir ouvrir le .accdb).

Installer un environnement virtuel Python (optionnel mais recommandé) :

bash
python -m venv env
source env/bin/activate  # Linux/macOS
env\Scripts\activate     # Windows
2. Installer les dépendances Python
Installer Flask et pyodbc (ou pypyodbc) pour connecter Flask à la base Access :

bash
pip install Flask pyodbc
Installer d'autres bibliothèques nécessaires selon votre code (exemple : qrcode, io, etc.).

3. Préparer la base de données Access
Créer ou ouvrir votre fichier .accdb avec la structure des tables décrite :

Table Modules (avec colonnes ID, Nom, Ecole, Niveau, TarifHoraire, HeuresCM, HeuresTD, HeuresTP)

Table Paiements (ID, ModuleID, Date, Montant, Type)

Vérifier que les relations sont bien configurées entre les tables (ModuleID comme clé étrangère).

4. Configurer la connexion à la base depuis Flask
Installer un driver ODBC Access (ex : Microsoft Access Driver (*.mdb, *.accdb)) sur votre machine.

Configurer la chaîne de connexion dans votre application Flask, par exemple pour Windows :

python
import pyodbc

conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=chemin_vers_votre_fichier.accdb;'
)
conn = pyodbc.connect(conn_str)
5. Déployer l'application Flask
Organiser votre application Flask avec dossiers templates (pour HTML), static (CSS/JS), et un fichier principal app.py.

Développer vos routes Flask pour :

Afficher les modules et paiements

Gérer les formulaires d'ajout/modification

Effectuer les calculs (heures totales, montants)

Lancer l’application Flask en local :

bash
flask run
Accéder à l’application via http://127.0.0.1:5000 dans votre navigateur.

6. Tester et utiliser
Ajouter votre premier module via le formulaire web.

Saisir les heures et tarif.

Entrer les paiements et vérifier le calcul automatique des soldes.

Exporter les rapports (PDF, Excel) si cette fonctionnalité est implémentée.

Conseils supplémentaires
Assurez-vous que le driver ODBC Access est compatible avec votre version Windows (32 ou 64 bits).

Mettez en place des sauvegardes régulières du fichier .accdb car il sera modifié localement.

Assurez-vous que Python ait les droits d’accès au dossier contenant la base Access.

Pour améliorer la sécurité, ne laissez pas la base en écriture accessible à tous les utilisateurs.

Ce guide assure une installation simple et complète du système localement, pour un usage indépendant sans connexion internet.