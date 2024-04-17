from odoo import api, fields, models


class Stage(models.Model):
    _inherit = "crm.stage"

    color = fields.Integer(string="Color")
    stage_selection = fields.Selection([
        ('new', 'New'),
        ('open', 'Open'),
        ('lost', 'lost'),
        ('won', 'Won'),
    ], string='Enquiry State', default='new', required=True)
