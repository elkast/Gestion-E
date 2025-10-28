from flask import Flask
from config import Config
from blueprints.principal import principal_bp, close_db
from blueprints.ecoles import schools_bp
from blueprints.paiements import payments_bp

app = Flask(__name__)
app.config.from_object(Config)

# Enregistrer les blueprints
app.register_blueprint(principal_bp)
app.register_blueprint(schools_bp)
app.register_blueprint(payments_bp)

# Enregistrer la fonction de fermeture de la DB
app.teardown_appcontext(close_db)


from flask import g
import pymysql


def get_db():
    """Crée une connexion à la base de données"""
    if 'db' not in g:
        g.db = pymysql.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB'],
            port=app.config['MYSQL_PORT'],
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False
        )
    return g.db


@app.teardown_appcontext
def close_db(error):
    """Ferme la connexion à la base de données"""
    db = g.pop('db', None)
    if db is not None:
        db.close()


# Health check endpoint
@app.route('/health')
def health_check():
    """Endpoint de santé pour vérifier que l'application fonctionne"""
    try:
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
            "message": "Database connection failed. Check MYSQL_* environment variables in Railway."
        }, 503











if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host="127.0.0.1", port=port, debug=True)
