"""
WSGI configuration for PythonAnywhere deployment
"""
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/sossou/projet_mr_koffi'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables for production
os.environ['USE_SQLITE'] = 'False'  # Use MySQL on PythonAnywhere
os.environ['FLASK_DEBUG'] = 'False'

# Import the Flask app
from app import app as application