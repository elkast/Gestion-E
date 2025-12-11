"""
Blueprint paiements - Gestion des paiements des modules.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from database.connexion import obtenir_db

bp_paiements = Blueprint('paiements', __name__, url_prefix='/paiements')


@bp_paiements.route('/module/<int:module_id>')
def liste_paiements(module_id):
    """Affiche les paiements d'un module."""
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
    
    # Calculer le total perçu
    curseur.execute("SELECT SUM(montant) as total_percu FROM paiements WHERE module_id = %s", (module_id,))
    resultat = curseur.fetchone()
    total_percu = resultat['total_percu'] if resultat['total_percu'] else 0
    
    # Calculer le reste à payer
    reste_a_payer = module['montant_total'] - float(total_percu)
    
    # Récupération des paiements
    curseur.execute("SELECT * FROM paiements WHERE module_id = %s ORDER BY date_paiement DESC", (module_id,))
    paiements = curseur.fetchall()
    
    curseur.close()
    return render_template('paiements/liste.html', 
                         module=module, 
                         paiements=paiements,
                         total_percu=total_percu,
                         reste_a_payer=reste_a_payer)


@bp_paiements.route('/ajouter', methods=['POST'])
def ajouter_paiement():
    """Ajoute un nouveau paiement."""
    module_id = request.form['module_id']
    montant = float(request.form['montant'])
    type_paiement = request.form['type_paiement']
    reference = request.form.get('reference', '').strip()

    db = obtenir_db()
    curseur = db.cursor()

    # Calculer le total des paiements pour le module
    curseur.execute("SELECT SUM(montant) as total_percu FROM paiements WHERE module_id = %s", (module_id,))
    resultat = curseur.fetchone()
    total_percu = resultat['total_percu'] if resultat['total_percu'] else 0
    
    # Obtenir le montant total du module
    curseur.execute("SELECT montant_total FROM modules WHERE id = %s", (module_id,))
    module = curseur.fetchone()
    montant_total = module['montant_total'] if module else 0

    # Calculer le reste à payer
    reste_a_payer = montant_total - float(total_percu)

    # Vérifier si le montant dépasse ce qui reste à payer
    if montant > reste_a_payer:
        flash(f'Le montant ne peut pas dépasser le reste à payer ({reste_a_payer:,.0f} FCFA).', 'danger')
        return redirect(f'/paiements/module/{module_id}')

    # Calculer le nouveau total après ce paiement
    nouveau_total_percu = float(total_percu) + montant

    # Déterminer le statut automatiquement
    if nouveau_total_percu >= montant_total:
        statut = 'complet'
    else:
        statut = 'partiel'

    # Générer une référence automatique si non fournie
    if not reference:
        import datetime
        curseur.execute("SELECT COUNT(*) as count FROM paiements WHERE module_id = %s", (module_id,))
        count = curseur.fetchone()['count']
        reference = f"PAY-{module_id}-{count + 1}-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

    placeholder = '?' if g.est_sqlite else '%s'
    curseur.execute(f"""
        INSERT INTO paiements (module_id, montant, type_paiement, reference, date_paiement, statut)
        VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, DATE('now'), {placeholder})
    """ if g.est_sqlite else f"""
        INSERT INTO paiements (module_id, montant, type_paiement, reference, date_paiement, statut)
        VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, CURDATE(), {placeholder})
    """, (module_id, montant, type_paiement, reference, statut))

    db.commit()
    curseur.close()

    flash('Paiement enregistré avec succès !', 'success')
    return redirect(f'/paiements/module/{module_id}')


@bp_paiements.route('/modifier/<int:paiement_id>', methods=['GET', 'POST'])
def modifier_paiement(paiement_id):
    """Modifie un paiement existant."""
    db = obtenir_db()
    curseur = db.cursor()
    
    if request.method == 'POST':
        montant = float(request.form['montant'])
        type_paiement = request.form['type_paiement']
        reference = request.form['reference']
        date_paiement = request.form['date_paiement']
        module_id = request.form['module_id']

        # Calculer le total des paiements en excluant le paiement actuel
        curseur.execute("SELECT SUM(montant) as total_percu FROM paiements WHERE module_id = %s AND id != %s", 
                       (module_id, paiement_id))
        resultat = curseur.fetchone()
        total_percu = resultat['total_percu'] if resultat['total_percu'] else 0

        # Obtenir le montant total du module
        curseur.execute("SELECT montant_total FROM modules WHERE id = %s", (module_id,))
        module = curseur.fetchone()
        montant_total = module['montant_total'] if module else 0

        # Calculer le nouveau total après la mise à jour de ce paiement
        nouveau_total_percu = float(total_percu) + montant

        # Déterminer le statut automatiquement
        if nouveau_total_percu == montant_total:
            statut = 'complet'
        elif nouveau_total_percu < montant_total:
            statut = 'partiel'
        else:
            statut = 'excédent'

        placeholder = '?' if g.est_sqlite else '%s'
        curseur.execute(f"""
            UPDATE paiements 
            SET montant={placeholder}, type_paiement={placeholder}, reference={placeholder}, 
                date_paiement={placeholder}, statut={placeholder}
            WHERE id={placeholder}
        """, (montant, type_paiement, reference, date_paiement, statut, paiement_id))
        db.commit()
        curseur.close()

        flash('Paiement modifié avec succès !', 'success')
        return redirect(f'/paiements/module/{module_id}')
    
    curseur.execute("SELECT * FROM paiements WHERE id = %s", (paiement_id,))
    paiement = curseur.fetchone()
    curseur.close()
    
    if paiement:
        return render_template('paiements/modifier.html', paiement=paiement)
    else:
        flash('Paiement non trouvé.', 'danger')
        return redirect('/')


@bp_paiements.route('/supprimer/<int:paiement_id>')
def supprimer_paiement(paiement_id):
    """Supprime un paiement."""
    db = obtenir_db()
    curseur = db.cursor()
    curseur.execute("SELECT module_id FROM paiements WHERE id = %s", (paiement_id,))
    paiement = curseur.fetchone()
    
    if paiement:
        module_id = paiement['module_id']
        placeholder = '?' if g.est_sqlite else '%s'
        curseur.execute(f"DELETE FROM paiements WHERE id = {placeholder}", (paiement_id,))
        db.commit()
        curseur.close()
        flash('Paiement supprimé avec succès !', 'success')
        return redirect(f'/paiements/module/{module_id}')
    else:
        curseur.close()
        flash('Paiement non trouvé.', 'danger')
        return redirect('/')