from odoo import models,fields

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    property = fields.Many2one('account.analytic.account',string= "Property Type")