from odoo import http
from odoo.http import request

class Property(http.Controller):
    @http.route('/properties', type='http', auth='public', website=True)
    def properties(self, search=None):
        domain = [('published', '=', True)]
        if search:
            domain.append(('name', 'ilike', search)) 

        properties = request.env['account.analytic.account'].sudo().search(domain)
        return request.render('real_estate.properties_template', {
            'properties': properties,
            'search': search or ''
        })

    @http.route('/property/<int:property_id>', type='http', auth='public', website=True)
    def property_detail(self, property_id):
        property = request.env['account.analytic.account'].sudo().browse(property_id)
        return request.render('real_estate.property_detail_template', {
            'property': property
        })
