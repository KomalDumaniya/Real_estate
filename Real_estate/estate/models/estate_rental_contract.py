from odoo import models,fields,api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    property = fields.Many2one("account.analytic.account",string="Property",required = True)
    commision_line_id = fields.One2many("commision_line","sale_order_id",string="Commision Details")
    total_profit = fields.Float(compute="_compute_total_profit")

    @api.depends('commision_line_id.profit')
    def _compute_total_profit(self):
        for order in self:
            total_profit = sum(line.profit for line in order.commision_line_id)
            order.total_profit = total_profit

    def action_commision_details(self):
        for line in self:   
            commision_id = self.env['commision_line'].search([('sale_order_id', '=', line.id)])
            return {
                    'type': 'ir.actions.act_window',
                    'name': 'commision line',
                    'view_mode': 'list',
                    'res_model': 'commision_line',
                    'domain': [('id', 'in', commision_id.ids)],
                    'target': 'current',
                }

    @api.onchange('property')
    def _onchange_property_add(self):
        for order in self:
            property_product = self.env['product.template'].search([('product_sequence', '=', order.property.sequence_id)])
            if property_product:
                if order.order_line:
                    order.order_line=[(5, 0, 0)]
                order_line_vals = {
                    'product_id': property_product.product_variant_id.id,
                    'price_unit': property_product.list_price,
                    'product_uom_qty': 1.0,
                    'order_id': order.id,
                    }
                order.write({'order_line': [(0, 0, order_line_vals)]})

class AccountMove(models.Model):
    _inherit = 'account.move'

    commision_line_ids = fields.One2many('commision_line',"invoice_id",string='Commission Lines')
    property = fields.Many2one("account.analytic.account",string="Property",required = True)
