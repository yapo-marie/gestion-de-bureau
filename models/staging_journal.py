from odoo import models, fields

class StagingJournal(models.Model):
    _name = 'staging.journal'
    _description = "Transit : Journal entrées et sorties"

    personne = fields.Char(string="Nom Saisie")
    article = fields.Char(string="Articles")
    date_entree = fields.Date(string="Date Entrée")
    qte_entree = fields.Float(string="Qté Entrée")
    prix_unitaire = fields.Float(string="Prix Unitaire HT")
    date_sortie = fields.Date(string="Date Sortie")
    qte_sortie = fields.Float(string="Qté Sortie")
    demandeur = fields.Char(string="Demandeur")
    service = fields.Char(string="Service/Agence")
    ref_article = fields.Char(string="Réf Article")
    state = fields.Selection([('draft', 'Brouillon'), ('done', 'Importé')], default='draft')
