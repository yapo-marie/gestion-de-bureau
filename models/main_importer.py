from odoo import models, api, fields, _
from odoo.exceptions import UserError

class MainImporter(models.AbstractModel):
    _name = 'main.importer'
    _description = "Logique de transfert final vers Odoo"

    def action_validate_and_transfer(self):
        """ Bouton pour transformer le transit en données réelles Odoo """

        product_obj = self.env['product.product']
        stock_staging = self.env['staging.stock'].search([('state', '=', 'draft')])

        if not stock_staging:
            raise UserError(_("Aucune donnée en attente de validation dans la zone de transit."))

        # 1. Création/Mise à jour des Articles
        for line in stock_staging:
            # On cherche si l'article existe déjà par sa référence
            product = product_obj.search([('default_code', '=', line.ref)], limit=1)

            if not product:
                # Création de l'article s'il n'existe pas
                product = product_obj.create({
                    'name': line.article,
                    'default_code': line.ref,
                    'type': 'product', # Article stockable
                    'categ_id': self.env.ref('product.product_category_all').id,
                })

            # 2. Ajustement du Stock (Initialisation)
            # On utilise le 'stock_final' du fichier Excel pour forcer la quantité en magasin
            location_id = self.env['stock.warehouse'].search([], limit=1).lot_stock_id

            if location_id:
                self.env['stock.quant'].with_context(inventory_mode=True).create({
                    'product_id': product.id,
                    'location_id': location_id.id,
                    'inventory_quantity': line.stock_final,
                }).action_apply_inventory()

            # Marquer la ligne de transit comme traitée
            line.state = 'done'

        return {
            'effect': {
                'fadeout': 'slow',
                'message': _("Transfert réussi ! Les articles et stocks ont été mis à jour."),
                'type': 'rainbow_man',
            }
        }
