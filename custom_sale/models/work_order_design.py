# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from datetime import date
from odoo.exceptions import UserError


class WorkOrderDesign(models.Model):
    _name = "work.order.design"

    name = fields.Char(string="Sequence Number", readonly=True, required=True,
                       copy=False, default='NEW')
    product_id = fields.Many2one('product.product', string="Product")
    date = fields.Datetime(string="Date", default=date.today())
    sales_person = fields.Many2one('res.users', string="Sale Person")
    partner_id = fields.Many2one('res.partner', string="Customer")
    operation_ids = fields.One2many('work.order.design.lines', 'design_id', 'Operations')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting_for_approval', 'Waiting For Approval'),
        ('approve', 'Approved'),
        ('mdn', 'MDN'),
        ('reject', 'Rejected'),
        ('cancel', 'Cancel')
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    sale_id = fields.Many2one('sale.order', string="Origin")
    mdn_id = fields.Many2one('mrp.bom', string="MDN")
    quantity = fields.Float(string="Quantity")

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('work.order.design')
        result = super(WorkOrderDesign, self).create(vals)
        return result

    def sent_production_head(self):
        for rec in self:
            if not rec.operation_ids:
                raise UserError("Please add product design/operations")
            rec.state = "waiting_for_approval"

    def approve_design(self):
        for rec in self:
            rec.state = "approve"

    def reject_design(self):
        for rec in self:
            rec.state = "reject"

    def cancel_design(self):
        for rec in self:
            rec.state = "cancel"

    def action_create_mdn(self):
        for rec in self:

            val = {
                'product_tmpl_id': rec.product_id.product_tmpl_id.id,
                'design_id': rec.id
            }
            bom_id = self.env['mrp.bom'].create(val)
            list = [(5, 0, 0)]
            for x in rec.operation_ids:
                val = {
                    'name': x.name,
                    'workcenter_id': x.workcenter_id.id,
                    'worksheet_type': x.worksheet_type,
                    'note': x.note,
                    'worksheet': x.worksheet,
                    'worksheet_google_slide': x.worksheet_google_slide,
                    'time_cycle_manual': x.time_cycle_manual,
                    'bom_id': bom_id.id

                }
                list.append((0, 0, val))
            bom_id.update({'operation_ids': list})
            rec.mdn_id = bom_id.id
            rec.state = 'mdn'


class WorkOrderDesignLines(models.Model):
    _name = 'work.order.design.lines'

    design_id = fields.Many2one('work.order.design')
    name = fields.Char('Operation', required=True)
    workcenter_id = fields.Many2one('mrp.workcenter', 'Work Center', required=True)
    sequence = fields.Integer(
        'Sequence', default=100,
        help="Gives the sequence order when displaying a list of routing Work Centers.")
    worksheet_type = fields.Selection([
        ('pdf', 'PDF'), ('google_slide', 'Google Slide'), ('text', 'Text')],
        string="Worksheet", default="text"
    )
    note = fields.Html('Description')
    worksheet = fields.Binary('PDF')
    worksheet_google_slide = fields.Char('Google Slide',
                                         help="Paste the url of your Google Slide. Make sure the access to the document is public.")
    time_cycle_manual = fields.Float(
        'Manual Duration', default=60,
        help="Time in minutes:"
             "- In manual mode, time used"
             "- In automatic mode, supposed first time when there aren't any work orders yet")
