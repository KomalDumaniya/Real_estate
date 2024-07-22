from odoo import _,models, fields, api
from odoo.exceptions import UserError

class CommisionLine(models.Model):
    _name = 'commision_line'
    _description = 'Commision Line'
    _rec_name = 'commision_contact'

    commision_contact = fields.Many2one("res.partner", string="Contact", domain="[('commision_location', '!=', False)]")
    position = fields.Char(string="Designation(role)")
    commision = fields.Float(string="Commision(in%)")
    profit = fields.Float(string="Profit", compute="_compute_profit", store=True)
    sale_order_id = fields.Many2one("sale.order")
    invoice_id = fields.Many2one("account.move")
    status = fields.Selection(
        string="Status?",
        selection=[
            ('draft', 'Draft'),
            ('in_bill', 'In Bill')],
        readonly=True,
        default = 'draft'
    )

    @api.onchange('commision_contact')
    def _onchange_commision_contact(self):
        if self.commision_contact:
            self.position = self.commision_contact.position.employee_position
            self.commision = self.commision_contact.commision

    @api.model
    def create(self, vals):
        sale_order = self.env['sale.order'].browse(vals.get('sale_order_id'))
        if sale_order and not sale_order.order_line:
            raise UserError('Please add at least one product line before adding commission details.')
        invoice = self.env['account.move'].browse(vals.get('invoice_id'))
        if invoice and not invoice.invoice_line_ids:
            raise UserError('Please add at least one product line in the invoice before adding commission details.')
        return super(CommisionLine, self).create(vals)

    @api.depends(
        'commision_contact.commision_location',
        'sale_order_id.state',
        'sale_order_id.order_line.price_unit',
        'invoice_id.state',
        'invoice_id.invoice_line_ids.price_unit',
        'commision'
    )
    def _compute_profit(self):
        for record in self:
            total_profit = 0.0
            if record.commision_contact.commision_location == 'sale_order' and record.sale_order_id.state in ['sale', 'done']:
                for line in record.sale_order_id.order_line:
                    product_commision = (line.price_unit * record.commision) / 100
                    total_profit += product_commision
            elif record.commision_contact.commision_location == 'confirm_invoice' and record.invoice_id.state == 'posted':
                for line in record.invoice_id.invoice_line_ids:
                    product_commision = (line.price_unit * record.commision) / 100
                    total_profit += product_commision
            record.profit = total_profit

    def _action_create_bill(self):
        bills = self.env['account.move']
        for line in self:
            if line.status == "in_bill":
                raise UserError('Already billed product.')
            commission_product = self.env['product.product'].search([('name', '=', 'commission')], limit=1)
            if not commission_product:
                commission_product = self.env['product.product'].create({
                    'name': 'commission',
                    'type': 'service',
                    'default_code': 'COMM',
                    'list_price': 0.0,
                })
            if commission_product:
                bill = self.env['account.move'].create({
                    'move_type': 'in_invoice',
                    'partner_id': line.commision_contact.id,  
                    'invoice_line_ids': [(0, 0, {
                        'product_id': commission_product.id,
                        'name': commission_product.name,
                        'price_unit': line.profit,
                        'quantity': 1,
                    })],
                })
                bills |= bill  
                line.status = 'in_bill'
                
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'type': 'info',
                'title': _('Create Bill'),
                'message': _('Bills are generated.'),
                'next': {'type': 'ir.actions.act_window_close'},
            },
        }
        
    def unlink(self):
        for line in self:
            if line.status != "draft" or line.profit != 0.00:
                raise UserError('Only draft commission lines with 0.00 profit can be deleted.')
        return super(CommisionLine, self).unlink()

    def copy(self, default=None):
        raise UserError('Commission lines cannot be duplicated.')
        