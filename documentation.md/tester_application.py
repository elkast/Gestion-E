"""
Script de test pour vérifier que l'application fonctionne correctement.
"""
import os
import sys
from pathlib import Path

# Ajouter le répertoire du projet au path
REPERTOIRE_PROJET = Path(__file__).resolve().parent
sys.path.insert(0, str(REPERTOIRE_PROJET))

def tester_imports():
    """Teste que tous les modules peuvent être importés."""
    print("🔍 Test des imports...")
    try:
        from flask import Flask
        print("  ✅ Flask importé")
        
        from configuration import obtenir_configuration
        print("  ✅ Configuration importée")
        
        from database.connexion import obtenir_db, initialiser_app
        print("  ✅ Module database importé")
        
        from blueprints.principal import bp_principal
        from blueprints.ecoles import bp_ecoles
        from blueprints.paiements import bp_paiements
        print("  ✅ Blueprints importés")
        
        return True
    except Exception as e:
        print(f"  ❌ Erreur d'import : {e}")
        return False


def tester_configuration():
    """Teste la configuration."""
    print("\n🔍 Test de la configuration...")
    try:
        from configuration import obtenir_configuration
        config = obtenir_configuration()
        print(f"  ✅ Configuration chargée : {config.__name__}")
        return True
    except Exception as e:
        print(f"  ❌ Erreur de configuration : {e}")
        return False


def tester_base_de_donnees():
    """Teste la connexion à la base de données."""
    print("\n🔍 Test de la base de données...")
    try:
        from flask import Flask
        from configuration import obtenir_configuration
        from database.connexion import initialiser_app, obtenir_db
        
        app = Flask(__name__)
        app.config.from_object(obtenir_configuration())
        initialiser_app(app)
        
        with app.app_context():
            db = obtenir_db()
            curseur = db.cursor()
            
            # Tester une requête simple
            curseur.execute("SELECT 1")
            resultat = curseur.fetchone()
            curseur.close()
            
            print("  ✅ Connexion à la base de données réussie")
            print(f"  ✅ Type de DB : {'SQLite' if app.config.get('UTILISER_SQLITE') else 'MySQL'}")
            
            # Vérifier les tables
            if app.config.get('UTILISER_SQLITE'):
                curseur = db.cursor()
                curseur.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = curseur.fetchall()
                curseur.close()
                print(f"  ✅ Tables créées : {len(tables)}")
                for table in tables:
                    print(f"     - {table['name']}")
            
            return True
    except Exception as e:
        print(f"  ❌ Erreur de base de données : {e}")
        import traceback
        traceback.print_exc()
        return False


def tester_routes():
    """Teste les routes principales."""
    print("\n🔍 Test des routes...")
    try:
        from flask import Flask
        from configuration import obtenir_configuration
        from blueprints.principal import bp_principal
        from blueprints.ecoles import bp_ecoles
        from blueprints.paiements import bp_paiements
        from database.connexion import initialiser_app
        
        app = Flask(__name__)
        app.config.from_object(obtenir_configuration())
        initialiser_app(app)
        
        app.register_blueprint(bp_principal)
        app.register_blueprint(bp_ecoles)
        app.register_blueprint(bp_paiements)
        
        with app.test_client() as client:
            # Test route principale
            response = client.get('/')
            print(f"  ✅ Route / : {response.status_code}")
            
            # Test route santé
            response = client.get('/sante')
            print(f"  ✅ Route /sante : {response.status_code}")
            
            # Test route écoles
            response = client.get('/ecoles')
            print(f"  ✅ Route /ecoles : {response.status_code}")
            
            # Test route export
            response = client.get('/export')
            print(f"  ✅ Route /export : {response.status_code}")
            
            return True
    except Exception as e:
        print(f"  ❌ Erreur de routes : {e}")
        import traceback
        traceback.print_exc()
        return False


def tester_structure_fichiers():
    """Vérifie la structure des fichiers."""
    print("\n🔍 Test de la structure des fichiers...")
    
    fichiers_requis = [
        'app.py',
        'configuration.py',
        'requirements.txt',
        '.env',
        'database/__init__.py',
        'database/connexion.py',
        'blueprints/__init__.py',
        'blueprints/principal.py',
        'blueprints/ecoles.py',
        'blueprints/paiements.py',
        'templates/principal/index.html',
        'static/css/style.css'
    ]
    
    tous_presents = True
    for fichier in fichiers_requis:
        chemin = REPERTOIRE_PROJET / fichier
        if chemin.exists():
            print(f"  ✅ {fichier}")
        else:
            print(f"  ❌ {fichier} manquant")
            tous_presents = False
    
    # Vérifier que le dossier data existe
    dossier_data = REPERTOIRE_PROJET / 'data'
    if dossier_data.exists():
        print(f"  ✅ Dossier data/ existe")
    else:
        print(f"  ⚠️  Dossier data/ sera créé automatiquement")
    
    return tous_presents


def main():
    """Fonction principale de test."""
    print("=" * 60)
    print("🧪 TEST DE L'APPLICATION GESTION D'ENSEIGNEMENT")
    print("=" * 60)
    
    resultats = []
    
    # Tests
    resultats.append(("Structure des fichiers", tester_structure_fichiers()))
    resultats.append(("Imports", tester_imports()))
    resultats.append(("Configuration", tester_configuration()))
    resultats.append(("Base de données", tester_base_de_donnees()))
    resultats.append(("Routes", tester_routes()))
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    tous_reussis = True
    for nom, resultat in resultats:
        statut = "✅ RÉUSSI" if resultat else "❌ ÉCHOUÉ"
        print(f"{nom:.<40} {statut}")
        if not resultat:
            tous_reussis = False
    
    print("=" * 60)
    
    if tous_reussis:
        print("\n🎉 TOUS LES TESTS SONT RÉUSSIS !")
        print("\n✅ L'application est prête à être utilisée.")
        print("\n📝 Pour lancer l'application :")
        print("   python app.py")
        print("\n🌐 Puis ouvrir : http://localhost:5000")
        return 0
    else:
        print("\n⚠️  CERTAINS TESTS ONT ÉCHOUÉ")
        print("\n📝 Vérifiez les erreurs ci-dessus et corrigez-les.")
        return 1


if __name__ == '__main__':
    sys.exit(main())