"""
Application Flask - Gestion d'Enseignement Mr Koffi Elise
Application portable et professionnelle pour la gestion des établissements,
modules d'enseignement et paiements.
"""
from flask import Flask
from configuration import obtenir_configuration
from blueprints.principal import bp_principal
from blueprints.ecoles import bp_ecoles
from blueprints.paiements import bp_paiements
from database.connexion import initialiser_app

# Initialisation de Flask
app = Flask(__name__)
app.config.from_object(obtenir_configuration())

# Initialiser la gestion de la base de données
initialiser_app(app)

# Enregistrer les blueprints
app.register_blueprint(bp_principal)
app.register_blueprint(bp_ecoles)
app.register_blueprint(bp_paiements)


@app.route('/sante')
def verification_sante():
    """Endpoint de santé pour vérifier que l'application fonctionne."""
    try:
        from database.connexion import obtenir_db
        db = obtenir_db()
        curseur = db.cursor()
        curseur.execute("SELECT 1")
        curseur.close()
        return {
            "statut": "sain",
            "base_de_donnees": "connectée",
            "message": "L'application fonctionne correctement"
        }, 200
    except Exception as e:
        return {
            "statut": "malsain",
            "base_de_donnees": "déconnectée",
            "erreur": str(e),
            "message": "Échec de la connexion à la base de données"
        }, 503


if __name__ == '__main__':
    # Pour le développement local uniquement
    app.run(debug=True, host='0.0.0.0', port=5000)