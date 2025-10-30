from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from .db import get_db

payments_bp = Blueprint('payments', __name__)

# Gestion des paiements
@payments_bp.route('/module/<int:module_id>/paiements')
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
@payments_bp.route('/ajouter-paiement', methods=['POST'])
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
@payments_bp.route('/edit-paiement/<int:paiement_id>', methods=['GET', 'POST'])
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

# Supprimer un paiement
@payments_bp.route('/delete-paiement/<int:paiement_id>')
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
