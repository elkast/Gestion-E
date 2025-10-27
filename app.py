from flask import Flask, render_template, request, redirect, url_for, flash, send_file, g
import pymysql
import pandas as pd
from io import BytesIO
import datetime
import xlsxwriter
import os

app = Flask(__name__)

# Configuration MySQL
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', '')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'gestion_enseignement')
app.config['MYSQL_PORT'] = int(os.environ.get('MYSQL_PORT', 3306))
app.secret_key = os.environ.get('SECRET_KEY', 'votre_cle_secrete_ici')


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

# Page d'accueil - Tableau de bord
@app.route('/')
def tableau_de_bord():
    try:
        db = get_db()
        curseur = db.cursor()
    except Exception as e:
        error_msg = "La base de données n'est pas accessible. Veuillez configurer les variables d'environnement MySQL dans Railway."
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Configuration Requise</title>
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }}
                .error {{ background: #fee; border: 2px solid #c33; padding: 20px; border-radius: 5px; }}
                .info {{ background: #eff; border: 2px solid #36c; padding: 20px; border-radius: 5px; margin-top: 20px; }}
                h1 {{ color: #c33; }}
                code {{ background: #f5f5f5; padding: 2px 5px; border-radius: 3px; }}
            </style>
        </head>
        <body>
            <div class="error">
                <h1>⚠️ Configuration MySQL Requise</h1>
                <p>{error_msg}</p>
                <p><strong>Erreur:</strong> {str(e)}</p>
            </div>
            <div class="info">
                <h2>📋 Étapes de Configuration</h2>
                <ol>
                    <li>Dans Railway Dashboard, cliquez sur <strong>+ New</strong></li>
                    <li>Sélectionnez <strong>Database → MySQL</strong></li>
                    <li>Railway configurera automatiquement les variables d'environnement</li>
                    <li>Connectez-vous à MySQL et importez <code>database.sql</code></li>
                    <li>Redéployez cette application</li>
                </ol>
                <h3>Variables Requises:</h3>
                <ul>
                    <li><code>MYSQL_HOST</code></li>
                    <li><code>MYSQL_USER</code></li>
                    <li><code>MYSQL_PASSWORD</code></li>
                    <li><code>MYSQL_DB</code></li>
                    <li><code>MYSQL_PORT</code></li>
                    <li><code>SECRET_KEY</code></li>
                </ul>
            </div>
        </body>
        </html>
        """, 503

    # Récupération des modules avec calculs
    curseur.execute("""
        SELECT m.*, e.nom as nom_ecole,
               COALESCE(SUM(p.montant), 0) as montant_percu,
               (m.montant_total - COALESCE(SUM(p.montant), 0)) as reste_a_payer
        FROM modules m
        LEFT JOIN ecoles e ON m.ecole_id = e.id
        LEFT JOIN paiements p ON m.id = p.module_id
        GROUP BY m.id
        ORDER BY m.created_at DESC
    """)
    modules = curseur.fetchall()

    # Calcul des totaux globaux
    total_chiffre_affaires = sum(module['montant_total'] for module in modules)
    total_percu = sum(module['montant_percu'] for module in modules)
    total_reste = total_chiffre_affaires - total_percu

    curseur.close()

    return render_template('index.html',
                         modules=modules,
                         total_ca=total_chiffre_affaires,
                         total_percu=total_percu,
                         total_reste=total_reste)


#====================================================             ==============================================================================

# Gestion des établissements
@app.route('/ecoles')
def gestion_ecoles():
    db = get_db()
    curseur = db.cursor()

    # Récupération des établissements avec montants totaux
    curseur.execute("""
        SELECT e.*,
               COALESCE(SUM(m.montant_total), 0) as montant_total_ecole
        FROM ecoles e
        LEFT JOIN modules m ON e.id = m.ecole_id
        GROUP BY e.id
        ORDER BY e.nom
    """)
    ecoles = curseur.fetchall()

    # Pour chaque école, récupérer les montants par niveau
    for ecole in ecoles:
        curseur.execute("""
            SELECT niveau, COALESCE(SUM(montant_total), 0) as montant_total_niveau
            FROM modules
            WHERE ecole_id = %s
            GROUP BY niveau
            ORDER BY niveau
        """, (ecole['id'],))
        ecole['montants_par_niveau'] = curseur.fetchall()

    curseur.close()
    return render_template('ecoles.html', ecoles=ecoles)

# États Financiers par École
@app.route('/finances-ecoles')
def finances_ecoles():
    trier_par = request.args.get('sort_by', 'nom_ecole')
    ordre = request.args.get('order', 'asc')
    recherche = request.args.get('search', '').strip()
    page = int(request.args.get('page', 1))
    par_page = 5

    # Valider trier_par
    tris_autorises = ['nom_ecole', 'total_du', 'total_percu', 'reste_a_payer']
    if trier_par not in tris_autorises:
        trier_par = 'nom_ecole'

    # Déterminer la direction de l'ordre
    ordre_sql = 'ASC' if ordre == 'asc' else 'DESC'

    db = get_db()
    curseur = db.cursor()

    # Base query with filtering
    base_query = """
        FROM ecoles e
        LEFT JOIN modules m ON e.id = m.ecole_id
        LEFT JOIN paiements p ON m.id = p.module_id
    """

    # Condition de filtrage
    clause_where = ""
    parametres = []
    if recherche:
        clause_where = "WHERE e.nom LIKE %s"
        parametres.append(f"%{recherche}%")

    # Compter les enregistrements totaux pour la pagination
    requete_compte = f"SELECT COUNT(DISTINCT e.id) {base_query} {clause_where}"
    curseur.execute(requete_compte, parametres)
    enregistrements_totaux = curseur.fetchone()['COUNT(DISTINCT e.id)']
    pages_totales = (enregistrements_totaux + par_page - 1) // par_page

    # Requête principale avec agrégation, filtrage, tri et pagination
    requete_principale = f"""
        SELECT e.nom as nom_ecole,
               COALESCE(SUM(m.montant_total), 0) as total_du,
               COALESCE(SUM(p.montant), 0) as total_percu,
               (COALESCE(SUM(m.montant_total), 0) - COALESCE(SUM(p.montant), 0)) as reste_a_payer
        {base_query}
        {clause_where}
        GROUP BY e.id, e.nom
        ORDER BY {trier_par} {ordre_sql}
        LIMIT %s OFFSET %s
    """
    parametres.extend([par_page, (page - 1) * par_page])
    curseur.execute(requete_principale, parametres)
    finances_ecoles = curseur.fetchall()

    curseur.close()
    return render_template('finances_ecoles.html',
                           finances_ecoles=finances_ecoles,
                           sort_by=trier_par,
                           order=ordre,
                           search=recherche,
                           page=page,
                           total_pages=pages_totales)


#=================================================================            =====================================================================
# Ajouter un établissement
@app.route('/ajouter-ecole', methods=['GET', 'POST'])
def ajouter_ecole():
    db = get_db()
    curseur = db.cursor()
    if request.method == 'POST':
        nom = request.form['nom']
        type_etablissement = request.form['type_etablissement']
        ville = request.form['ville']
        contact = request.form['contact']
        telephone = request.form.get('telephone', '')
        volume_cm = float(request.form.get('volume_cm', 0))
        volume_td = float(request.form.get('volume_td', 0))
        volume_tp = float(request.form.get('volume_tp', 0))

        curseur.execute("""
            INSERT INTO ecoles (nom, type_etablissement, ville, contact, telephone, volume_cm, volume_td, volume_tp)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (nom, type_etablissement, ville, contact, telephone, volume_cm, volume_td, volume_tp))
        db.commit()
        curseur.close()

        flash('Établissement ajouté avec succès!', 'success')
        return redirect('/ecoles')
    else:
        # Requête GET : afficher le formulaire pour modifier ou ajouter
        return redirect('/ecoles')



#==========================================================                   ===============================================================================
# Modifier un établissement
@app.route('/edit-ecole/<int:ecole_id>', methods=['GET', 'POST'])
def edit_ecole(ecole_id):
    db = get_db()
    curseur = db.cursor()
    if request.method == 'POST':
        nom = request.form['nom']
        type_etablissement = request.form['type_etablissement']
        ville = request.form['ville']
        contact = request.form['contact']
        telephone = request.form.get('telephone', '')
        volume_cm = float(request.form.get('volume_cm', 0))
        volume_td = float(request.form.get('volume_td', 0))
        volume_tp = float(request.form.get('volume_tp', 0))

        curseur.execute("""
            UPDATE ecoles SET nom=%s, type_etablissement=%s, ville=%s, contact=%s, telephone=%s, volume_cm=%s, volume_td=%s, volume_tp=%s
            WHERE id=%s
        """, (nom, type_etablissement, ville, contact, telephone, volume_cm, volume_td, volume_tp, ecole_id))
        db.commit()

        # Mettre à jour tous les modules de cette école avec les nouveaux volumes
        curseur.execute("UPDATE modules SET volume_cm = %s, volume_td = %s, volume_tp = %s, volume_total = %s, montant_total = volume_total * montant_heure WHERE ecole_id = %s", (volume_cm, volume_td, volume_tp, volume_cm + volume_td + volume_tp, ecole_id))
        db.commit()

        curseur.close()

        flash('Établissement modifié avec succès!', 'success')
        return redirect('/ecoles')
    else:
        curseur.execute("SELECT * FROM ecoles WHERE id = %s", (ecole_id,))
        ecole = curseur.fetchone()
        curseur.close()
        if ecole:
            return render_template('edit_ecole.html', ecole=ecole)
        else:
            flash('Établissement non trouvé.', 'danger')
            return redirect('/ecoles')

#=============================================================             =====================================================================
# Supprimer un établissement
@app.route('/delete-ecole/<int:ecole_id>')
def delete_ecole(ecole_id):
    db = get_db()
    curseur = db.cursor()
    curseur.execute("DELETE FROM ecoles WHERE id = %s", (ecole_id,))
    db.commit()
    curseur.close()
    flash('Établissement supprimé avec succès!', 'success')
    return redirect('/ecoles')

# Gestion des volumes par niveau pour une école
@app.route('/ecole/<int:ecole_id>/volumes-niveau', methods=['GET', 'POST'])
def gestion_volumes_niveau(ecole_id):
    db = get_db()
    curseur = db.cursor()

    if request.method == 'POST':
        # Récupérer tous les modules de l'école
        curseur.execute("SELECT id, nom_module FROM modules WHERE ecole_id = %s", (ecole_id,))
        modules = curseur.fetchall()

        for module in modules:
            module_id = module['id']
            volume_cm = float(request.form.get(f'volume_cm_{module_id}', 0))
            volume_td = float(request.form.get(f'volume_td_{module_id}', 0))
            volume_tp = float(request.form.get(f'volume_tp_{module_id}', 0))
            volume_total = volume_cm + volume_td + volume_tp

            # Mettre à jour le module
            curseur.execute("""
                UPDATE modules SET volume_cm = %s, volume_td = %s, volume_tp = %s, volume_total = %s, montant_total = volume_total * montant_heure
                WHERE id = %s
            """, (volume_cm, volume_td, volume_tp, volume_total, module_id))

        db.commit()
        flash('Volumes des modules mis à jour avec succès!', 'success')
        return redirect(f'/ecole/{ecole_id}/volumes-niveau')

    # Récupération de l'école
    curseur.execute("SELECT * FROM ecoles WHERE id = %s", (ecole_id,))
    ecole = curseur.fetchone()

    # Récupération des modules groupés par niveau
    curseur.execute("""
        SELECT * FROM modules WHERE ecole_id = %s ORDER BY niveau, nom_module
    """, (ecole_id,))
    modules = curseur.fetchall()
    curseur.close()

    # Grouper les modules par niveau
    modules_par_niveau = {}
    niveaux = ['Licence 1', 'Licence 2', 'Licence 3', 'Master 1', 'Master 2', 'Doctorat']
    for niveau in niveaux:
        modules_par_niveau[niveau] = [m for m in modules if m['niveau'] == niveau]

    return render_template('gestion_volumes_niveau.html', ecole=ecole, niveaux=niveaux, modules_par_niveau=modules_par_niveau)

# Gestion des volumes par niveau - Interface standalone
@app.route('/gestion-volumes-niveau')
def gestion_volumes_niveau_standalone():
    db = get_db()
    curseur = db.cursor()
    curseur.execute("SELECT id, nom FROM ecoles ORDER BY nom")
    ecoles = curseur.fetchall()
    curseur.close()
    return render_template('gestion_volumes_niveau_standalone.html', ecoles=ecoles)

# Page d'export
@app.route('/export')
def export_page():
    return render_template('export.html')


#================================================             ==================================================================
# Modifier un module
@app.route('/edit-module/<int:module_id>', methods=['GET', 'POST'])
def edit_module(module_id):
    db = get_db()
    cur = db.cursor()

    if request.method == 'POST':
        # Récupération des données
        nom_module = request.form['nom_module']
        ecole_id = request.form['ecole_id']
        niveau = request.form['niveau']
        volume_cm = float(request.form.get('volume_cm', 0))
        volume_td = float(request.form.get('volume_td', 0))
        volume_tp = float(request.form.get('volume_tp', 0))
        montant_heure = float(request.form['montant_heure'])
        annee_universitaire = request.form['annee_universitaire']

        # Gestion de l'établissement
        if ecole_id == 'new':
            # Ajouter un nouvel établissement
            new_ecole_nom = request.form.get('new_ecole_nom')
            new_ecole_type = request.form.get('new_ecole_type')
            new_ecole_ville = request.form.get('new_ecole_ville')
            new_ecole_contact = request.form.get('new_ecole_contact')

            if new_ecole_nom:
                cur.execute("""
                    INSERT INTO ecoles (nom, type_etablissement, ville, contact)
                    VALUES (%s, %s, %s, %s)
                """, (new_ecole_nom, new_ecole_type, new_ecole_ville, new_ecole_contact))
                db.commit()
                ecole_id = cur.lastrowid
            else:
                flash('Nom de l\'établissement requis pour un nouvel ajout.', 'danger')
                return redirect(f'/edit-module/{module_id}')

        # Calculs automatiques
        volume_total = float(volume_cm) + float(volume_td) + float(volume_tp)
        montant_total = volume_total * montant_heure

        # Mise à jour du module
        cur.execute("""
            UPDATE modules SET
            nom_module = %s, ecole_id = %s, niveau = %s, volume_cm = %s, volume_td = %s, volume_tp = %s,
            volume_total = %s, montant_heure = %s, montant_total = %s, annee_universitaire = %s
            WHERE id = %s
        """, (nom_module, ecole_id, niveau, volume_cm, volume_td, volume_tp,
              volume_total, montant_heure, montant_total, annee_universitaire, module_id))

        db.commit()

        # Mettre à jour les volumes par niveau pour l'école
        cur.execute("""
            SELECT SUM(volume_cm) as total_cm, SUM(volume_td) as total_td, SUM(volume_tp) as total_tp
            FROM modules
            WHERE ecole_id = %s AND niveau = %s
        """, (ecole_id, niveau))
        totals = cur.fetchone()

        # Vérifier si l'entrée existe
        cur.execute("SELECT id FROM ecole_niveau_volumes WHERE ecole_id = %s AND niveau = %s", (ecole_id, niveau))
        existing = cur.fetchone()

        if existing:
            cur.execute("""
                UPDATE ecole_niveau_volumes SET volume_cm = %s, volume_td = %s, volume_tp = %s
                WHERE ecole_id = %s AND niveau = %s
            """, (totals['total_cm'] or 0, totals['total_td'] or 0, totals['total_tp'] or 0, ecole_id, niveau))
        else:
            cur.execute("""
                INSERT INTO ecole_niveau_volumes (ecole_id, niveau, volume_cm, volume_td, volume_tp)
                VALUES (%s, %s, %s, %s, %s)
            """, (ecole_id, niveau, totals['total_cm'] or 0, totals['total_td'] or 0, totals['total_tp'] or 0))

        db.commit()
        flash('Module modifié avec succès!', 'success')
        return redirect('/')

    # Récupération du module existant
    cur.execute("SELECT * FROM modules WHERE id = %s", (module_id,))
    module = cur.fetchone()

    # Récupération des établissements pour le formulaire
    cur.execute("SELECT * FROM ecoles ORDER BY nom")
    ecoles = cur.fetchall()
    cur.close()

    return render_template('edit_module.html', module=module, ecoles=ecoles)

# Supprimer un module
@app.route('/delete-module/<int:module_id>')
def delete_module(module_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM modules WHERE id = %s", (module_id,))
    db.commit()
    cur.close()
    flash('Module supprimé avec succès!', 'success')
    return redirect('/')

# Détails d'un module
@app.route('/module/<int:module_id>')
def module_details(module_id):
    db = get_db()
    cur = db.cursor()

    # Récupération du module
    cur.execute("""
        SELECT m.*, e.nom as ecole_nom
        FROM modules m
        LEFT JOIN ecoles e ON m.ecole_id = e.id
        WHERE m.id = %s
    """, (module_id,))
    module = cur.fetchone()

    # Récupération des paiements
    cur.execute("SELECT * FROM paiements WHERE module_id = %s ORDER BY date_paiement", (module_id,))
    paiements = cur.fetchall()

    cur.close()
    return render_template('module_details.html', module=module, paiements=paiements)

# Ajouter un module
@app.route('/ajouter-module', methods=['GET', 'POST'])
def ajouter_module():
    db = get_db()
    cur = db.cursor()

    if request.method == 'POST':
        # Récupération des données
        nom_module = request.form['nom_module']
        ecole_id = request.form['ecole_id']
        niveau = request.form['niveau']
        volume_cm = float(request.form.get('volume_cm', 0))
        volume_td = float(request.form.get('volume_td', 0))
        volume_tp = float(request.form.get('volume_tp', 0))
        montant_heure = float(request.form['montant_heure'])
        annee_universitaire = request.form['annee_universitaire']

        # Gestion de l'établissement
        if ecole_id == 'new':
            # Ajouter un nouvel établissement
            new_ecole_nom = request.form.get('new_ecole_nom')
            new_ecole_type = request.form.get('new_ecole_type')
            new_ecole_ville = request.form.get('new_ecole_ville')
            new_ecole_contact = request.form.get('new_ecole_contact')

            if new_ecole_nom:
                cur.execute("""
                    INSERT INTO ecoles (nom, type_etablissement, ville, contact)
                    VALUES (%s, %s, %s, %s)
                """, (new_ecole_nom, new_ecole_type, new_ecole_ville, new_ecole_contact))
                db.commit()
                ecole_id = cur.lastrowid  # Récupérer l'ID de l'établissement nouvellement créé
            else:
                flash('Nom de l\'établissement requis pour un nouvel ajout.', 'danger')
                return redirect('/ajouter-module')

        # Calculs automatiques
        volume_total = volume_cm + volume_td + volume_tp
        montant_total = volume_total * montant_heure

        # Insertion du module
        cur.execute("""
            INSERT INTO modules
            (nom_module, ecole_id, niveau, volume_cm, volume_td, volume_tp,
             volume_total, montant_heure, montant_total, annee_universitaire)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (nom_module, ecole_id, niveau, volume_cm, volume_td, volume_tp,
              volume_total, montant_heure, montant_total, annee_universitaire))

        db.commit()
        flash('Module ajouté avec succès!', 'success')
        return redirect('/')

    # Récupération des établissements pour le formulaire
    cur.execute("SELECT * FROM ecoles ORDER BY nom")
    ecoles = cur.fetchall()
    cur.close()

    return render_template('ajouter_module.html', ecoles=ecoles)

# Gestion des paiements
@app.route('/module/<int:module_id>/paiements')
def gestion_paiements(module_id):
    db = get_db()
    cur = db.cursor()
    
    # Récupération du module
    cur.execute("""
        SELECT m.*, e.nom as ecole_nom 
        FROM modules m 
        LEFT JOIN ecoles e ON m.ecole_id = e.id 
        WHERE m.id = %s
    """, (module_id,))
    module = cur.fetchone()
    
    # Récupération des paiements
    cur.execute("SELECT * FROM paiements WHERE module_id = %s ORDER BY date_paiement", (module_id,))
    paiements = cur.fetchall()
    
    cur.close()
    return render_template('paiements.html', module=module, paiements=paiements)

# Ajouter un paiement
@app.route('/ajouter-paiement', methods=['POST'])
def ajouter_paiement():
    module_id = request.form['module_id']
    montant = float(request.form['montant'])
    type_paiement = request.form['type_paiement']
    reference = request.form['reference']

    db = get_db()
    cur = db.cursor()

    # Calculer le total des paiements pour le module
    cur.execute("SELECT SUM(montant) as total_percu FROM paiements WHERE module_id = %s", (module_id,))
    result = cur.fetchone()
    total_percu = result['total_percu'] if result['total_percu'] else 0
    # Obtenir le montant total du module
    cur.execute("SELECT montant_total FROM modules WHERE id = %s", (module_id,))
    module = cur.fetchone()
    montant_total = module['montant_total'] if module else 0

    # Calculer le nouveau total après ce paiement
    new_total_percu = float(total_percu) + montant

    # Vérifier si le nouveau paiement dépasse le montant total
    if new_total_percu > montant_total:
        flash('Le montant total des paiements ne peut pas dépasser le montant total du module.', 'danger')
        return redirect(f'/module/{module_id}/paiements')

    # Déterminer le statut automatiquement
    if new_total_percu == montant_total:
        statut = 'complet'
    elif new_total_percu < montant_total:
        statut = 'partiel'
    else:
        statut = 'excédent'  # Surpaiement

    cur.execute("""
        INSERT INTO paiements (module_id, montant, type_paiement, reference, date_paiement, statut)
        VALUES (%s, %s, %s, %s, CURDATE(), %s)
    """, (module_id, montant, type_paiement, reference, statut))

    db.commit()
    cur.close()

    flash('Paiement enregistré avec succès!', 'success')
    return redirect(f'/module/{module_id}/paiements')

# Modifier un paiement
@app.route('/edit-paiement/<int:paiement_id>', methods=['GET', 'POST'])
def edit_paiement(paiement_id):
    db = get_db()
    cur = db.cursor()
    if request.method == 'POST':
        montant = float(request.form['montant'])
        type_paiement = request.form['type_paiement']
        reference = request.form['reference']
        date_paiement = request.form['date_paiement']
        module_id = request.form['module_id']

        # Calculer le total des paiements en excluant le paiement actuel
        cur.execute("SELECT SUM(montant) as total_percu FROM paiements WHERE module_id = %s AND id != %s", (module_id, paiement_id))
        result = cur.fetchone()
        total_percu = result['total_percu'] if result['total_percu'] else 0

        # Obtenir le montant total du module
        cur.execute("SELECT montant_total FROM modules WHERE id = %s", (module_id,))
        module = cur.fetchone()
        montant_total = module['montant_total'] if module else 0

        # Calculer le nouveau total après la mise à jour de ce paiement
        new_total_percu = float(total_percu) + montant

        # Déterminer le statut automatiquement
        if new_total_percu == montant_total:
            statut = 'complet'
        elif new_total_percu < montant_total:
            statut = 'partiel'
        else:
            statut = 'excédent'  # Surpaiement

        cur.execute("""
            UPDATE paiements SET montant=%s, type_paiement=%s, reference=%s, date_paiement=%s, statut=%s
            WHERE id=%s
        """, (montant, type_paiement, reference, date_paiement, statut, paiement_id))
        db.commit()
        cur.close()

        flash('Paiement modifié avec succès!', 'success')
        return redirect(f'/module/{module_id}/paiements')
    else:
        cur.execute("SELECT * FROM paiements WHERE id = %s", (paiement_id,))
        paiement = cur.fetchone()
        cur.close()
        if paiement:
            return render_template('edit_paiement.html', paiement=paiement)
        else:
            flash('Paiement non trouvé.', 'danger')
            return redirect('/')

#===================================================          ======================================================================
# Supprimer un paiement
@app.route('/delete-paiement/<int:paiement_id>')
def delete_paiement(paiement_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT module_id FROM paiements WHERE id = %s", (paiement_id,))
    paiement = cur.fetchone()
    if paiement:
        module_id = paiement['module_id']
        cur.execute("DELETE FROM paiements WHERE id = %s", (paiement_id,))
        db.commit()
        cur.close()
        flash('Paiement supprimé avec succès!', 'success')
        return redirect(f'/module/{module_id}/paiements')
    else:
        cur.close()
        flash('Paiement non trouvé.', 'danger')
        return redirect('/')

#=============================================================================================================================================
#=============================================================================================================================================
#=============================================================================================================================================

#=============================================================================================================================================
# Export Excel
@app.route('/export/excel')
def export_excel():
    db = get_db()
    cur = db.cursor()
    
    # Récupération des données complètes
    cur.execute("""
        SELECT m.nom_module, e.nom as ecole, m.niveau, 
               m.volume_cm, m.volume_td, m.volume_tp, m.volume_total,
               m.montant_heure, m.montant_total,
               COALESCE(SUM(p.montant), 0) as montant_percu,
               (m.montant_total - COALESCE(SUM(p.montant), 0)) as reste_a_payer,
               m.annee_universitaire
        FROM modules m
        LEFT JOIN ecoles e ON m.ecole_id = e.id
        LEFT JOIN paiements p ON m.id = p.module_id
        GROUP BY m.nom_module, e.nom, m.niveau, m.volume_cm, m.volume_td, m.volume_tp, m.volume_total,
                 m.montant_heure, m.montant_total, m.annee_universitaire
    """)
    data = cur.fetchall()
    cur.close()
    
    # Conversion en DataFrame pandas
    df = pd.DataFrame(data)
    
    # Création du fichier Excel en mémoire
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Modules', index=False)
        
        # Formatage
        workbook = writer.book
        worksheet = writer.sheets['Modules']
        
        # Format monétaire
        money_format = workbook.add_format({'num_format': '#,##0 FCFA'})
        worksheet.set_column('H:J', 15, money_format)
        
    output.seek(0)
    
    return send_file(output, 
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                     as_attachment=True,
                     download_name=f'export_enseignement_{datetime.datetime.now().strftime("%Y%m%d")}.xlsx')

# Export PDF (version simplifiée)
@app.route('/export/pdf')
def export_pdf():
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
    import io
    
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        SELECT m.nom_module, e.nom as ecole, m.niveau, m.montant_total,
               COALESCE(SUM(p.montant), 0) as montant_percu
        FROM modules m
        LEFT JOIN ecoles e ON m.ecole_id = e.id
        LEFT JOIN paiements p ON m.id = p.module_id
        GROUP BY m.id
    """)
    data = cur.fetchall()
    cur.close()
    
    
    #================================================              ==============================================================================
    # Création du PDF en mémoire
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # En-tête
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, "Rapport d'Enseignement")
    p.drawString(100, 730, f"Date : {datetime.datetime.now().strftime('%d/%m/%Y')}")
    
    # Contenu
    y = 700
    p.setFont("Helvetica", 10)
    
    for module in data:
        if y < 100:  # Nouvelle page si nécessaire
            p.showPage()
            y = 750
        
        p.drawString(100, y, f"{module['nom_module']} - {module['ecole']}")
        p.drawString(400, y, f"{module['montant_total']:,.0f} FCFA")
        y -= 20
    
    p.save()
    buffer.seek(0)
    
    return send_file(buffer, 
                     mimetype='application/pdf',
                     as_attachment=True,
                     download_name=f'rapport_enseignement_{datetime.datetime.now().strftime("%Y%m%d")}.pdf')

@app.route('/add-sample-data')
def add_sample_data():
    db = get_db()
    cur = db.cursor()

    # Insert school
    cur.execute("INSERT INTO ecoles (nom, type_etablissement, ville, contact, telephone) VALUES (%s, %s, %s, %s, %s)", ('Ecole A', 'Université', 'Ville A', 'Contact A', '123456'))
    ecole_id = cur.lastrowid

    # Insert module
    cur.execute("INSERT INTO modules (nom_module, ecole_id, niveau, volume_cm, volume_td, volume_tp, volume_total, montant_heure, montant_total, annee_universitaire) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", ('Module 1', ecole_id, 'L1', 10, 5, 5, 20, 5000, 100000, '2023-2024'))
    module_id = cur.lastrowid

    # Insert payment
    cur.execute("INSERT INTO paiements (module_id, montant, type_paiement, reference, date_paiement, statut) VALUES (%s, %s, %s, %s, CURDATE(), %s)", (module_id, 50000, 'Virement', 'REF1', 'partiel'))

    db.commit()
    cur.close()

    return "Sample data added"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)