from odoo import api, fields, models

class Meter(models.Model):
    _name = 'meter_model'
    _description = 'Meter Model'
    _order = 'sequence'

    name = fields.Char(string="Description")
    price = fields.Float(string="Price")
    sequence = fields.Integer(default=1)
    account_analytic_account_id = fields.Many2one('account.analytic.account')
    meter_id = fields.Many2one('meter_model', string="Meter")
    date = fields.Date(string="Date")
    quantity = fields.Float(string="Quantity")
    usage = fields.Char(string="Usage")
    description = fields.Text(string="Description")
