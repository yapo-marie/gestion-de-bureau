from odoo import models, fields

class StagingArticle(models.Model):
    _name = 'staging.article'
    _description = "Transit : Base de données articles"

    designation = fields.Char(string="Désignation")
    ref = fields.Char(string="Référence")
    prix_unitaire = fields.Float(string="Prix Unitaire")
    state = fields.Selection([('draft', 'Brouillon'), ('done', 'Importé')], default='draft')
