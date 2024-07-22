from odoo import models,fields,api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    position = fields.Many2one("employee_commision",string="job possition")
    commision = fields.Float(string = "Commision")
    commision_location = fields.Selection(string ="where to commision?",
        selection = [
            ('sale_order','Sale Order'),
            ('confirm_invoice','Confirm Invoice')],
        help="choose form where you want to get commision...",required=True)
    
    @api.onchange('position')
    def _onchange_product_id(self):
        if self.position:        
            self.commision = self.position.employee_commision
