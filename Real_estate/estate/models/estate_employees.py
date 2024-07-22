from odoo import models,fields

class EmployeeCommision(models.Model):
    _name = 'employee_commision'
    _description = 'Employee Commision'
    _rec_name = 'employee_position'

    employee_position = fields.Char(string="Postion")
    employee_commision = fields.Float(string="Commision(in %)")