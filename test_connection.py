"""
Script de test pour vérifier la connexion MySQL avec PyMySQL
Utilisez ce script pour tester votre configuration avant le déploiement
"""
import pymysql
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env si disponible
load_dotenv()

def test_connection():
    """Test la connexion à la base de données MySQL"""
    
    # Configuration
    config = {
        'host': os.environ.get('MYSQL_HOST', 'localhost'),
        'user': os.environ.get('MYSQL_USER', 'root'),
        'password': os.environ.get('MYSQL_PASSWORD', ''),
        'database': os.environ.get('MYSQL_DB', 'gestion_enseignement'),
        'port': int(os.environ.get('MYSQL_PORT', 3306))
    }
    
    print("🔍 Test de connexion MySQL avec PyMySQL")
    print(f"📍 Host: {config['host']}")
    print(f"👤 User: {config['user']}")
    print(f"🗄️  Database: {config['database']}")
    print(f"🔌 Port: {config['port']}")
    print("-" * 50)
    
    try:
        # Tentative de connexion
        print("⏳ Connexion en cours...")
        connection = pymysql.connect(**config)
        print("✅ Connexion réussie!")
        
        # Test d'une requête simple
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"📊 Version MySQL: {version[0]}")
        
        # Vérifier les tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"📋 Tables trouvées: {len(tables)}")
        for table in tables:
            print(f"   - {table[0]}")
        
        cursor.close()
        connection.close()
        print("\n✅ Tous les tests sont passés!")
        return True
        
    except pymysql.Error as e:
        print(f"\n❌ Erreur de connexion: {e}")
        print("\n💡 Vérifiez:")
        print("   1. Les variables d'environnement sont correctes")
        print("   2. Le serveur MySQL est démarré")
        print("   3. L'utilisateur a les permissions nécessaires")
        print("   4. Le pare-feu autorise la connexion")
        return False
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        return False

if __name__ == "__main__":
    test_connection()