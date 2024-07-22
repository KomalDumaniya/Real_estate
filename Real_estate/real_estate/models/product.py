from odoo import api, fields, models

class Product(models.Model):
    _inherit = 'product.template'

    product_sequence = fields.Char(string="Product Sequence")
