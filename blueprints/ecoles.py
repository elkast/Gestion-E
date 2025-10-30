from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from .db import get_db

schools_bp = Blueprint('schools', __name__)

# Gestion des établissements
@schools_bp.route('/ecoles')
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
@schools_bp.route('/finances-ecoles')
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

# Ajouter un établissement
@schools_bp.route('/ajouter-ecole', methods=['GET', 'POST'])
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

# Modifier un établissement
@schools_bp.route('/edit-ecole/<int:ecole_id>', methods=['GET', 'POST'])
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
        curseur.execute("UPDATE modules SET volume_cm = %s, volume_td = %s, volume_tp = %s, volume_total = %s, montant_total = (volume_cm * tarif_cm) + (volume_td * tarif_td) + (volume_tp * tarif_tp) WHERE ecole_id = %s", (volume_cm, volume_td, volume_tp, volume_cm + volume_td + volume_tp, ecole_id))
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

# Supprimer un établissement
@schools_bp.route('/delete-ecole/<int:ecole_id>')
def delete_ecole(ecole_id):
    db = get_db()
    curseur = db.cursor()
    curseur.execute("DELETE FROM ecoles WHERE id = %s", (ecole_id,))
    db.commit()
    curseur.close()
    flash('Établissement supprimé avec succès!', 'success')
    return redirect('/ecoles')

# Gestion des volumes par niveau pour une école
@schools_bp.route('/ecole/<int:ecole_id>/volumes-niveau', methods=['GET', 'POST'])
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
                UPDATE modules SET volume_cm = %s, volume_td = %s, volume_tp = %s, volume_total = %s, montant_total = (volume_cm * tarif_cm) + (volume_td * tarif_td) + (volume_tp * tarif_tp)
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
@schools_bp.route('/gestion-volumes-niveau')
def gestion_volumes_niveau_standalone():
    db = get_db()
    curseur = db.cursor()
    curseur.execute("SELECT id, nom FROM ecoles ORDER BY nom")
    ecoles = curseur.fetchall()
    curseur.close()
    return render_template('gestion_volumes_niveau_standalone.html', ecoles=ecoles)
