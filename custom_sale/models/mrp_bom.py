from odoo import _, models, fields, api
from odoo.exceptions import UserError


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting_for_approval', 'Waiting For Approval'),
        ('approve', 'Approved'),
        ('create_po', 'RFQ Created'),
        ('compenonets_purchased', 'Components Purchased'),
        ('reject', 'Rejected'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    # partner_id = fields.Many2one('res.partner', string="Vendor")
    po_id = fields.Many2one('purchase.order', string="Purchase Order")
    design_id = fields.Many2one('work.order.design', string="Work Design")

    def submit_for_approval(self):
        if not self.bom_line_ids:
            raise UserError("Please add components")
        self.state = "waiting_for_approval"

    def action_approve(self):
        self.state = "approve"

    def action_reject(self):
        self.state = "reject"

    def create_rfq(self):
        list = [(5, 0, 0)]
        for x in self.bom_line_ids:
            val = {
                'product_id': x.product_id.id,
                'product_qty': x.product_qty * self.design_id.quantity,
                'product_uom_id': x.product_uom_id.id,
            }
            list.append((0, 0, val))

        view_id = self.env.ref('purchase_requisition.view_purchase_requisition_form').id
        context = {
            # 'default_partner_id': self.partner_id.id,
            'default_line_ids': list,
            "default_bom_id": self.id,
            'state': 'draft'

        }
        self.state = "create_po"
        return {
            'type': 'ir.actions.act_window',
            'name': 'Purcahse RFQ',
            'view_mode': 'tree',
            'view_type': 'form',
            'res_model': 'purchase.requisition',
            'view_id': view_id,
            'views': [(view_id, 'form')],
            'target': 'current',
            'context': context
        }
