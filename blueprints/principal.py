from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, g
import pandas as pd
from io import BytesIO
import datetime
import xlsxwriter
from .db import get_db

principal_bp = Blueprint('principal', __name__)

# Page d'accueil - Tableau de bord
@principal_bp.route('/')
def tableau_de_bord():
    db = get_db()
    curseur = db.cursor()

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

# Détails d'un module
@principal_bp.route('/module/<int:module_id>')
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
@principal_bp.route('/ajouter-module', methods=['GET', 'POST'])
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
        tarif_cm = float(request.form.get('tarif_cm', 0))
        tarif_td = float(request.form.get('tarif_td', 0))
        tarif_tp = float(request.form.get('tarif_tp', 0))
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
                    VALUES (?, ?, ?, ?)
                """ if g.is_sqlite else """
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
        montant_total = (volume_cm * tarif_cm) + (volume_td * tarif_td) + (volume_tp * tarif_tp)
        montant_heure = montant_total / volume_total if volume_total > 0 else 0
        
        # Insertion du module
        placeholder = '?' if g.is_sqlite else '%s'
        cur.execute(f"""
            INSERT INTO modules
            (nom_module, ecole_id, niveau, volume_cm, volume_td, volume_tp,
             tarif_cm, tarif_td, tarif_tp, volume_total, montant_heure, montant_total, annee_universitaire)
            VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, 
                    {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})
        """, (nom_module, ecole_id, niveau, volume_cm, volume_td, volume_tp,
              tarif_cm, tarif_td, tarif_tp, volume_total, montant_heure, montant_total, annee_universitaire))

        db.commit()
        flash('Module ajouté avec succès!', 'success')
        return redirect('/')

    # Récupération des établissements pour le formulaire
    cur.execute("SELECT * FROM ecoles ORDER BY nom")
    ecoles = cur.fetchall()
    cur.close()

    # Pré-calculer les valeurs par défaut
    volume_total = 0.0
    montant_total = 0
    montant_heure = 0

    return render_template('ajouter_module.html', ecoles=ecoles, volume_total=volume_total, montant_total=montant_total, montant_heure=montant_heure)

# Supprimer un module
@principal_bp.route('/delete-module/<int:module_id>')
def delete_module(module_id):
    db = get_db()
    cur = db.cursor()
    placeholder = '?' if g.is_sqlite else '%s'
    cur.execute(f"DELETE FROM modules WHERE id = {placeholder}", (module_id,))
    db.commit()
    cur.close()
    flash('Module supprimé avec succès!', 'success')
    return redirect('/')

# Modifier un module
@principal_bp.route('/edit-module/<int:module_id>', methods=['GET', 'POST'])
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
        tarif_cm = float(request.form.get('tarif_cm', 0))
        tarif_td = float(request.form.get('tarif_td', 0))
        tarif_tp = float(request.form.get('tarif_tp', 0))
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
        volume_total = volume_cm + volume_td + volume_tp
        montant_total = (volume_cm * tarif_cm) + (volume_td * tarif_td) + (volume_tp * tarif_tp)
        montant_heure = montant_total / volume_total if volume_total > 0 else 0

        # Mise à jour du module
        placeholder = '?' if g.is_sqlite else '%s'
        cur.execute(f"""
            UPDATE modules SET
            nom_module = {placeholder}, ecole_id = {placeholder}, niveau = {placeholder}, 
            volume_cm = {placeholder}, volume_td = {placeholder}, volume_tp = {placeholder},
            tarif_cm = {placeholder}, tarif_td = {placeholder}, tarif_tp = {placeholder}, 
            volume_total = {placeholder}, montant_heure = {placeholder}, montant_total = {placeholder}, 
            annee_universitaire = {placeholder}
            WHERE id = {placeholder}
        """, (nom_module, ecole_id, niveau, volume_cm, volume_td, volume_tp,
              tarif_cm, tarif_td, tarif_tp, volume_total, montant_heure, montant_total, annee_universitaire, module_id))

        db.commit()

        # Mettre à jour les volumes par niveau pour l'école
        placeholder = '?' if g.is_sqlite else '%s'
        cur.execute(f"""
            SELECT SUM(volume_cm) as total_cm, SUM(volume_td) as total_td, SUM(volume_tp) as total_tp
            FROM modules
            WHERE ecole_id = {placeholder} AND niveau = {placeholder}
        """, (ecole_id, niveau))
        totals = cur.fetchone()

        # Vérifier si l'entrée existe
        placeholder = '?' if g.is_sqlite else '%s'
        cur.execute(f"SELECT id FROM ecole_niveau_volumes WHERE ecole_id = {placeholder} AND niveau = {placeholder}", (ecole_id, niveau))
        existing = cur.fetchone()

        if existing:
            placeholder = '?' if g.is_sqlite else '%s'
            cur.execute(f"""
                UPDATE ecole_niveau_volumes SET volume_cm = {placeholder}, volume_td = {placeholder}, volume_tp = {placeholder}
                WHERE ecole_id = {placeholder} AND niveau = {placeholder}
            """, (totals['total_cm'] or 0, totals['total_td'] or 0, totals['total_tp'] or 0, ecole_id, niveau))
        else:
            placeholder = '?' if g.is_sqlite else '%s'
            cur.execute(f"""
                INSERT INTO ecole_niveau_volumes (ecole_id, niveau, volume_cm, volume_td, volume_tp)
                VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})
            """, (ecole_id, niveau, totals['total_cm'] or 0, totals['total_td'] or 0, totals['total_tp'] or 0))

        db.commit()
        flash('Module modifié avec succès!', 'success')
        return redirect('/')

    # Récupération du module existant
    placeholder = '?' if g.is_sqlite else '%s'
    cur.execute(f"SELECT * FROM modules WHERE id = {placeholder}", (module_id,))
    module = cur.fetchone()

    # Récupération des établissements pour le formulaire
    cur.execute("SELECT * FROM ecoles ORDER BY nom")
    ecoles = cur.fetchall()
    cur.close()

    return render_template('edit_module.html', module=module, ecoles=ecoles, volume_total=module.volume_total, montant_total=module.montant_total, montant_heure=module.montant_heure)

# Function to calculate totals
def calculate_totals(volume_cm, volume_td, volume_tp, tarif_cm, tarif_td, tarif_tp):
    volume_total = volume_cm + volume_td + volume_tp
    montant_total = (volume_cm * tarif_cm) + (volume_td * tarif_td) + (volume_tp * tarif_tp)
    montant_heure = montant_total / volume_total if volume_total > 0 else 0
    return volume_total, montant_total, montant_heure

# Page d'export
@principal_bp.route('/export')
def export_page():
    return render_template('export.html')

# Export Excel
@principal_bp.route('/export/excel')
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
@principal_bp.route('/export/pdf')
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

@principal_bp.route('/add-module', methods=['GET', 'POST'])
def add_module():
    db = get_db()
    cur = db.cursor()

    if request.method == 'POST':
        # Récupération des données
        nom = request.form['nom']
        ecole = request.form['ecole']
        niveau = request.form['niveau']
        tarif_cm = float(request.form.get('tarif_cm', 0))
        tarif_td = float(request.form.get('tarif_td', 0))
        tarif_tp = float(request.form.get('tarif_tp', 0))
        heures_cm = float(request.form.get('heures_cm', 0))
        heures_td = float(request.form.get('heures_td', 0))
        heures_tp = float(request.form.get('heures_tp', 0))

        # Calcul du montant total
        montant_total = (heures_cm * tarif_cm) + (heures_td * tarif_td) + (heures_tp * tarif_tp)
        volume_total = heures_cm + heures_td + heures_tp
        montant_heure = montant_total / volume_total if volume_total > 0 else 0

        # Insertion du module (simplifié pour cette route)
        cur.execute("""
            INSERT INTO modules
            (nom_module, ecole_id, niveau, volume_cm, volume_td, volume_tp, volume_total,
             tarif_cm, tarif_td, tarif_tp, montant_heure, montant_total, annee_universitaire)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (nom, 1, niveau, heures_cm, heures_td, heures_tp, volume_total,
              tarif_cm, tarif_td, tarif_tp, montant_heure, montant_total, '2023-2024'))

        db.commit()
        flash('Module ajouté avec succès!', 'success')
        return redirect('/')

    cur.close()
    return render_template('add_module.html')

@principal_bp.route('/add-sample-data')
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
