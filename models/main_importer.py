from odoo import models, api

class MainImporter(models.AbstractModel):
    _name = 'main.importer'
    _description = "Logique de transfert final"

    def action_final_validation(self):
        # Cette méthode contiendra la logique pour transformer le texte en Many2one
        pass
