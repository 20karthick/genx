from odoo import models, fields, _
from odoo.exceptions import UserError

PURCHASE_REQUISITION_STATES = [
    ('draft', 'Draft'),
    ('ongoing', 'Ongoing'),
    ('in_progress', 'Confirmed'),
    ('waiting_for_approval', 'Waiting For Approval'),
    ('first_level_approval', 'First Level Approval'),
    ('second_level_approval', 'Second Level Approval'),
    ('create_cheque', 'Cheque Created'),
    ('submt_cheque_for_approval', 'Submit Cheque For Approve'),
    ('cheque_approves','Cheque Approved'),
    ('open', 'Bid Selection'),
    ('done', 'Closed'),
    ('cancel', 'Cancelled')
]


class PurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'

    state = fields.Selection(PURCHASE_REQUISITION_STATES,
                             'Status', tracking=True, required=True,
                             copy=False, default='draft')
    state_blanket_order = fields.Selection(PURCHASE_REQUISITION_STATES, compute='_set_state')
    bom_id = fields.Many2one('mrp.bom', string="MDN")
    total_amount = fields.Float(string="Total Amount",readonly=True)

    def button_send_to_approve(self):
        self.state = 'waiting_for_approval'

    def first_level_approve(self):
        self.state = "first_level_approval"

    def second_level_approve(self):
        self.state = "second_level_approval"

    def action_in_progress(self):
        self.ensure_one()
        if not self.line_ids:
            raise UserError(_("You cannot confirm agreement '%s' because there is no product line.", self.name))
        if not self.vendor_id:
            raise UserError(_("Please select vendor/supplier"))
        if self.type_id.quantity_copy and self.vendor_id:
            for requisition_line in self.line_ids:
                if requisition_line.price_unit <= 0.0:
                    raise UserError(_('You cannot confirm the blanket order without price.'))
                if requisition_line.product_qty <= 0.0:
                    raise UserError(_('You cannot confirm the blanket order without quantity.'))
                requisition_line.create_supplier_info()
            self.write({'state': 'in_progress'})
        # Set the sequence number regarding the requisition type
        if self.name == 'New':
            self.name = self.env['ir.sequence'].with_company(self.company_id).next_by_code(
                'purchase.requisition.blanket.order')

    def create_cheque(self):
        amount = 0
        for line in self.line_ids:
            amount += line.product_qty * line.price_unit
        self.total_amount = amount
        self.state = 'create_cheque'

    def submit_cheque_approve(self):
        self.state = 'submt_cheque_for_approval'

    def cheque_approved(self):
        self.state = 'cheque_approves'




class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def action_mdn_done(self):
        self.requisition_id.bom_id.state = "compenonets_purchased"
