from odoo import api, fields, models, _

class Building(models.Model):
    _inherit = 'account.account.tag'

    applicability = fields.Selection(selection_add=[('properties', 'Properties')], ondelete={'properties': 'cascade'}, default='properties')

class Property(models.Model):
    _inherit = 'account.analytic.account'

    name = fields.Char(string="Property" , required=True)
    published = fields.Boolean(string="Published", default=False)
    building_id = fields.Many2one('account.account.tag', string="Building", domain="[('applicability', '=', 'properties')]")
    address = fields.Text(string="Address")
    property_sale = fields.Selection([
        ('Rent', 'Rent'), 
        ('Sale', 'Sale')], string='Sale or Rent', default='Rent')   
    sale_price = fields.Float(string="Sale Price")
    property_type = fields.Selection([
        ('Apartment', 'Apartment'), 
        ('House', 'House'), 
        ('Studio', 'Studio'), 
        ('Office', 'Office'), 
        ('Commercial space', 'Commercial space'), 
        ('Warehouse', 'Warehouse'), 
        ('Land', 'Land'), 
        ('Garage', 'Garage'), 
        ('Room', 'Room')
    ], string='Property Type')    
    property_image = fields.Binary("Property Image")
    website_description = fields.Text(string="Description")
    property_images = fields.Many2many('ir.attachment', 'analytic_account_attachment_rel', 'analytic_account_id', 'attachment_id', string="Property Images")
    property__document = fields.Many2many('ir.attachment', 'account_analytic_account_attachment_rel', 'account_id', 'attachment_id', string="Property Attachments")
    property_meter_reading = fields.One2many('meter_model', 'account_analytic_account_id', string='Meter Readings')
    product_created = fields.Boolean(string='Product Created', default=False)
    count_product = fields.Integer(compute='_compute_count_product', string='Product Count')
    sequence_id = fields.Char(
        string="Sequence Number",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _("New"),
        help="sequence Number",
    )

    @api.model
    def _get_default_plan_id(self):
        plan = self.env['account.analytic.plan'].search([('name', '=', 'Properties')], limit=1)
        return plan.id

    plan_id = fields.Many2one('account.analytic.plan', string='Plan', required=True, default=_get_default_plan_id)

    @api.depends('product_created') 
    def _compute_count_product(self):
        for record in self:
            if record.product_created:
                record.product_count = self.env['product.template'].search_count([('product_sequence', '=', record.sequence_id)])
            else:
                record.count_product = 0

    @api.model_create_multi
    def create(self, vals_list):
        products = self.env['product.template']
        for vals in vals_list:
            if vals.get("sequence_id", "New") == "New":
                vals["sequence_id"] = self.env["ir.sequence"].next_by_code("account.analytic.account") or _("New")
            
            if vals.get('property_sale') == 'Sale':
                product_vals = {
                    'name': vals.get('name'),
                    'product_sequence': vals.get('sequence_id'),
                    'list_price' : vals.get('sale_price')
                }
                products.create(product_vals)
                vals['product_created'] = True 
        
        return super().create(vals_list)
    
    def write(self, vals):
        products = self.env['product.template']
        for record in self:
            if 'property_sale' in vals and vals['property_sale'] == 'Sale' and not record.product_created:
                product_vals = {
                    'name': vals.get('name'),
                    'product_sequence': vals.get('sequence_id'),
                    'list_price' : vals.get('sale_price')
                }
                products.create(product_vals)
                vals['product_created'] = True  
            elif record.product_created:
                product = products.search([('product_sequence', '=', record.sequence_id)], limit=1)
                if product:
                    product_vals = {
                        'name': vals.get('name', record.name),
                        'list_price': vals.get('sale_price', record.sale_price),
                    }
                    product.write(product_vals)
        
        return super().write(vals)

    def action_view_product(self):
        self.ensure_one() 

        product = self.env['product.template'].search([('product_sequence', '=', self.sequence_id)], limit=1)

        if  product:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Product',
                'res_model': 'product.template',
                'view_mode': 'form',
                'res_id': product.id,
                'target': 'current',  
            }

    @api.depends('product_created')
    def _compute_count_product(self):
        for record in self:
            if record.product_created:
                record.count_product = self.env['product.template'].search_count([('product_sequence', '=', record.sequence_id)])
            else:
                record.count_product = 0
