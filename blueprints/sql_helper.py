"""
Helper functions for SQL queries that work with both SQLite and MySQL
This module patches the cursor execute method to automatically convert placeholders
"""
from flask import g

def patch_cursor(cursor):
    """
    Patch a cursor's execute method to automatically convert MySQL placeholders to SQLite
    """
    original_execute = cursor.execute
    
    def patched_execute(query, params=None):
        # Convert MySQL placeholders to SQLite if using SQLite
        if g.get('is_sqlite', True) and '%s' in query:
            query = query.replace('%s', '?')
        
        if params:
            return original_execute(query, params)
        else:
            return original_execute(query)
    
    cursor.execute = patched_execute
    return cursor