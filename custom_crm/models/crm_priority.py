from odoo import api, fields, models


class CrmPrority(models.Model):
    _name = 'crm.priority'

    name = fields.Char(string="Name",required=True)
    color = fields.Integer(string="Color")
