# TODO: Implement Separate Hourly Rates for Teaching Modules

## Tasks
- [x] Update database schema: Add columns `tarif_cm`, `tarif_td`, `tarif_tp` to `modules` table (FLOAT, default 0)
- [x] Update `templates/ajouter_module.html`: Add input fields for tarif_cm, tarif_td, tarif_tp
- [x] Update `templates/edit_module.html`: Add input fields for tarif_cm, tarif_td, tarif_tp
- [x] Update `blueprints/principal.py`:
  - [x] In `ajouter_module`: Change calculation to montant_total = (volume_cm * tarif_cm) + (volume_td * tarif_td) + (volume_tp * tarif_tp)
  - [x] Update INSERT query to include tarif_cm, tarif_td, tarif_tp
  - [x] In `edit_module`: Same changes for UPDATE query and calculation
- [x] Update `blueprints/ecoles.py`:
  - [x] In `gestion_volumes_niveau`: Update montant_total calculation when updating modules
  - [x] In `edit_ecole`: Update montant_total when updating school volumes
- [ ] Test the new functionality: Add a new module, edit existing, check calculations
