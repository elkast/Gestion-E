from flask import Flask
from config import Config
from blueprints.principal import principal_bp
from blueprints.ecoles import schools_bp
from blueprints.paiements import payments_bp
from blueprints.db import init_app

# --- Initialisation de Flask et de la DB ---
app = Flask(__name__)
app.config.from_object(Config)

# Initialiser la gestion de la DB
init_app(app)

# Enregistrer les blueprints
app.register_blueprint(principal_bp)
app.register_blueprint(schools_bp)
app.register_blueprint(payments_bp)

# Health check endpoint
@app.route('/health')
def health_check():
    """Endpoint de santé pour vérifier que l'application fonctionne"""
    try:
        from blueprints.db import get_db
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        return {
            "status": "healthy",
            "database": "connected",
            "message": "Application is running correctly"
        }, 200
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "message": "Database connection failed. Check MySQL configuration."
        }, 503

if __name__ == '__main__':
    # Pour le développement local uniquement
    app.run(host='0.0.0.0', port=5000, debug=True)