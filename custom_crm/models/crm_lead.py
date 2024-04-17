from odoo import api, fields, models, _
from odoo.exceptions import UserError


class CrmLead(models.Model):
    _inherit = "crm.lead"

    priority_id = fields.Many2many('crm.priority', string="Priority")

    def action_approve_lead(self):
        for rec in self:
            won_stage_id = self.env['crm.stage'].search([('stage_selection', '=', 'won')])
            rec.stage_id = won_stage_id.id

    def action_sale_quotations_new(self):
        if not self.stage_id.stage_selection == "won":
            raise UserError(_("Please approve the opportunity or change the state to won"))
        return super(CrmLead, self).action_sale_quotations_new()
