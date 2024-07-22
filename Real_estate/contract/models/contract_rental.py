from odoo import models,fields , api

class Property(models.Model):
    _inherit = 'account.analytic.account'

    rental_contracts = fields.Many2many('sale.order',string="contracts",compute="_compute_rental_contracts")
    total_property = fields.Integer(string="Total property",required=True)
    count_property = fields.Integer(compute='_compute_count_property', string='Available Property Count')

    @api.depends('sequence_id')
    def _compute_rental_contracts(self):
        for record in self:
            sale_orders = self.env['sale.order'].search([('property.sequence_id', '=', record.sequence_id)])
            record.rental_contracts = sale_orders

    @api.depends('total_property', 'rental_contracts')
    def _compute_count_property(self):
        for record in self:
            record.count_property = record.total_property - len(record.rental_contracts)

    def action_view_property(self):
        pass
