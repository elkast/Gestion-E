"""
Blueprint principal - Tableau de bord et gestion des modules.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, g
import pandas as pd
from io import BytesIO
import datetime
import xlsxwriter
from database.connexion import obtenir_db

bp_principal = Blueprint('principal', __name__)


@bp_principal.route('/')
def tableau_de_bord():
    """Page d'accueil - Tableau de bord avec statistiques."""
    db = obtenir_db()
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

    return render_template('principal/index.html',
                         modules=modules,
                         total_ca=total_chiffre_affaires,
                         total_percu=total_percu,
                         total_reste=total_reste)


@bp_principal.route('/module/<int:module_id>')
def details_module(module_id):
    """Affiche les détails d'un module spécifique."""
    db = obtenir_db()
    curseur = db.cursor()

    # Récupération du module
    curseur.execute("""
        SELECT m.*, e.nom as nom_ecole
        FROM modules m
        LEFT JOIN ecoles e ON m.ecole_id = e.id
        WHERE m.id = %s
    """, (module_id,))
    module = curseur.fetchone()

    # Récupération des paiements
    curseur.execute("SELECT * FROM paiements WHERE module_id = %s ORDER BY date_paiement", (module_id,))
    paiements = curseur.fetchall()

    curseur.close()
    return render_template('modules/details.html', module=module, paiements=paiements)


@bp_principal.route('/ajouter-module', methods=['GET', 'POST'])
def ajouter_module():
    """Ajoute un nouveau module d'enseignement."""
    db = obtenir_db()
    curseur = db.cursor()

    if request.method == 'POST':
        # Récupération des données du formulaire
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
            nouveau_nom_ecole = request.form.get('nouveau_nom_ecole')
            nouveau_type_ecole = request.form.get('nouveau_type_ecole')
            nouvelle_ville_ecole = request.form.get('nouvelle_ville_ecole')
            nouveau_contact_ecole = request.form.get('nouveau_contact_ecole')

            if nouveau_nom_ecole:
                placeholder = '?' if g.est_sqlite else '%s'
                curseur.execute(f"""
                    INSERT INTO ecoles (nom, type_etablissement, ville, contact)
                    VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder})
                """, (nouveau_nom_ecole, nouveau_type_ecole, nouvelle_ville_ecole, nouveau_contact_ecole))
                db.commit()
                ecole_id = curseur.lastrowid
            else:
                flash('Nom de l\'établissement requis pour un nouvel ajout.', 'danger')
                return redirect('/ajouter-module')

        # Calculs automatiques
        volume_total = volume_cm + volume_td + volume_tp
        montant_total = (volume_cm * tarif_cm) + (volume_td * tarif_td) + (volume_tp * tarif_tp)
        montant_heure = montant_total / volume_total if volume_total > 0 else 0
        
        # Insertion du module
        placeholder = '?' if g.est_sqlite else '%s'
        curseur.execute(f"""
            INSERT INTO modules
            (nom_module, ecole_id, niveau, volume_cm, volume_td, volume_tp,
             tarif_cm, tarif_td, tarif_tp, volume_total, montant_heure, montant_total, annee_universitaire)
            VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, 
                    {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})
        """, (nom_module, ecole_id, niveau, volume_cm, volume_td, volume_tp,
              tarif_cm, tarif_td, tarif_tp, volume_total, montant_heure, montant_total, annee_universitaire))

        db.commit()
        flash('Module ajouté avec succès !', 'success')
        return redirect('/')

    # Récupération des établissements pour le formulaire
    curseur.execute("SELECT * FROM ecoles ORDER BY nom")
    ecoles = curseur.fetchall()
    curseur.close()

    return render_template('modules/ajouter.html', ecoles=ecoles)


@bp_principal.route('/modifier-module/<int:module_id>', methods=['GET', 'POST'])
def modifier_module(module_id):
    """Modifie un module existant."""
    db = obtenir_db()
    curseur = db.cursor()

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

        # Calculs automatiques
        volume_total = volume_cm + volume_td + volume_tp
        montant_total = (volume_cm * tarif_cm) + (volume_td * tarif_td) + (volume_tp * tarif_tp)
        montant_heure = montant_total / volume_total if volume_total > 0 else 0

        # Mise à jour du module
        placeholder = '?' if g.est_sqlite else '%s'
        curseur.execute(f"""
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
        flash('Module modifié avec succès !', 'success')
        return redirect('/')

    # Récupération du module existant
    placeholder = '?' if g.est_sqlite else '%s'
    curseur.execute(f"SELECT * FROM modules WHERE id = {placeholder}", (module_id,))
    module = curseur.fetchone()

    # Récupération des établissements pour le formulaire
    curseur.execute("SELECT * FROM ecoles ORDER BY nom")
    ecoles = curseur.fetchall()
    curseur.close()

    return render_template('modules/modifier.html', module=module, ecoles=ecoles)


@bp_principal.route('/supprimer-module/<int:module_id>')
def supprimer_module(module_id):
    """Supprime un module."""
    db = obtenir_db()
    curseur = db.cursor()
    placeholder = '?' if g.est_sqlite else '%s'
    curseur.execute(f"DELETE FROM modules WHERE id = {placeholder}", (module_id,))
    db.commit()
    curseur.close()
    flash('Module supprimé avec succès !', 'success')
    return redirect('/')


@bp_principal.route('/export')
def page_export():
    """Page d'export des données."""
    return render_template('principal/export.html')


@bp_principal.route('/export/excel')
def exporter_excel():
    """Exporte les données en format Excel."""
    db = obtenir_db()
    curseur = db.cursor()
    
    # Récupération des données complètes
    curseur.execute("""
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
    donnees = curseur.fetchall()
    curseur.close()
    
    # Conversion en DataFrame pandas
    df = pd.DataFrame(donnees)
    
    # Création du fichier Excel en mémoire
    sortie = BytesIO()
    with pd.ExcelWriter(sortie, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Modules', index=False)
        
        # Formatage
        classeur = writer.book
        feuille = writer.sheets['Modules']
        
        # Format monétaire
        format_monetaire = classeur.add_format({'num_format': '#,##0 FCFA'})
        feuille.set_column('H:J', 15, format_monetaire)
        
    sortie.seek(0)
    
    return send_file(sortie, 
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                     as_attachment=True,
                     download_name=f'export_enseignement_{datetime.datetime.now().strftime("%Y%m%d")}.xlsx')


@bp_principal.route('/export/pdf')
def exporter_pdf():
    """Exporte les données en format PDF."""
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    import io
    
    db = obtenir_db()
    curseur = db.cursor()
    curseur.execute("""
        SELECT m.nom_module, e.nom as ecole, m.niveau, m.montant_total,
               COALESCE(SUM(p.montant), 0) as montant_percu
        FROM modules m
        LEFT JOIN ecoles e ON m.ecole_id = e.id
        LEFT JOIN paiements p ON m.id = p.module_id
        GROUP BY m.id
    """)
    donnees = curseur.fetchall()
    curseur.close()
    
    # Création du PDF en mémoire
    tampon = io.BytesIO()
    p = canvas.Canvas(tampon, pagesize=letter)
    
    # En-tête
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, "Rapport d'Enseignement")
    p.drawString(100, 730, f"Date : {datetime.datetime.now().strftime('%d/%m/%Y')}")
    
    # Contenu
    y = 700
    p.setFont("Helvetica", 10)
    
    for module in donnees:
        if y < 100:  # Nouvelle page si nécessaire
            p.showPage()
            y = 750
        
        p.drawString(100, y, f"{module['nom_module']} - {module['ecole']}")
        p.drawString(400, y, f"{module['montant_total']:,.0f} FCFA")
        y -= 20
    
    p.save()
    tampon.seek(0)
    
    return send_file(tampon, 
                     mimetype='application/pdf',
                     as_attachment=True,
                     download_name=f'rapport_enseignement_{datetime.datetime.now().strftime("%Y%m%d")}.pdf')