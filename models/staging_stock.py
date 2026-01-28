from odoo import models, fields

class StagingStock(models.Model):
    _name = 'staging.stock'
    _description = "Transit : État des stocks"

    categorie = fields.Char(string="CATEGORIE")
    article = fields.Char(string="Article")
    ref = fields.Char(string="Ref")
    stock_initial = fields.Float(string="Stock initial")
    entrees = fields.Float(string="Entrées")
    sorties = fields.Float(string="Sorties")
    stock_final = fields.Float(string="Stock Final")
    commentaires = fields.Char(string="Commentaires")
    state = fields.Selection([('draft', 'Brouillon'), ('done', 'Importé')], default='draft')
