import base64
import pandas as pd
import io
from odoo import models, fields, _
from odoo.exceptions import UserError

class ExcelImportWizard(models.TransientModel):
    _name = 'excel.import.wizard'
    _description = "Assistant d'importation"

    excel_file = fields.Binary(string="Fichier Excel", required=True)

    def action_import(self):
        data = base64.b64decode(self.excel_file)
        try:
            df_dict = pd.read_excel(io.BytesIO(data), sheet_name=None)
        except Exception as e:
            raise UserError(_("Erreur de lecture : %s") % e)

        # Nettoyage
        self.env['staging.article'].search([]).unlink()
        self.env['staging.journal'].search([]).unlink()
        self.env['staging.stock'].search([]).unlink()

        # FEUILLE 1
        s1 = df_dict.get('1.Base de donnée articles')
        if s1 is not None:
            for _, row in s1.iterrows():
                if pd.notna(row.get('Ref')):
                    self.env['staging.article'].create({
                        'designation': row.get('6'),
                        'ref': str(row.get('Ref')),
                        'prix_unitaire': row.get('Prix unitaire', 0.0),
                    })

        # FEUILLE 2 (Respect des en-têtes exacts du fichier)
        s2 = df_dict.get('2.Journal entrées et sorties')
        if s2 is not None:
            for _, row in s2.iterrows():
                if pd.notna(row.get('ARTICLES')):
                    self.env['staging.journal'].create({
                        'personne': row.get('nom de la personne qui saisit'),
                        'article': row.get('ARTICLES'),
                        'date_entree': row.get('Date Entrée') if pd.notna(row.get('Date Entrée')) else None,
                        'qte_entree': row.get('Qté Entrée/achat', 0.0),
                        'prix_unitaire': row.get('Prix Unitaire HT', 0.0),
                        'date_sortie': row.get('Date sortie') if pd.notna(row.get('Date sortie')) else None,
                        'qte_sortie': row.get('qté Sortie', 0.0),
                        'demandeur': row.get('Demandeur'),
                        'service': row.get('Serive/Agence'), # Faute de frappe conservée du fichier
                        'ref_article': str(row.get('Ref Arcticle', '')),
                    })

        # FEUILLE 3
        s3 = df_dict.get('3.Etat ds stocks en débt de pér')
        if s3 is not None:
            for _, row in s3.iterrows():
                if pd.notna(row.get('Article')):
                    self.env['staging.stock'].create({
                        'categorie': row.get('CATEGORIE'),
                        'article': row.get('Article'),
                        'ref': str(row.get('Ref', '')),
                        'stock_initial': row.get('Stock initial', 0.0),
                        'entrees': row.get('Entrées', 0.0),
                        'sorties': row.get('Sorties', 0.0),
                        'stock_final': row.get('Stock Final', 0.0),
                        'commentaires': row.get('Commentaires'),
                    })
        return {'type': 'ir.actions.act_window_close'}
