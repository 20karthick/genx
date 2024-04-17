from odoo import models, fields
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    state = fields.Selection(selection_add=[
        ('sent',),
        ('approved', 'Approved'),
        ('sale',),
        ('done',),
        ('cancel',),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    design_ids = fields.Many2many('work.order.design', string="Work Orders")

    def action_approve(self):
        for rec in self:
            if not rec.order_line:
                raise UserError("Please add product details")
            design_list = []
            for line in rec.order_line:
                val = {
                    'product_id': line.product_id.id,
                    'sales_person': rec.user_id.id,
                    'partner_id': rec.partner_id.id,
                    'sale_id': rec.id,
                    'quantity': line.product_uom_qty
                }
                design_id = self.env['work.order.design'].create(val)
                design_list.append(design_id.id)
            rec.design_ids = design_list
            rec.state = "approved"

    # def action_create_mdn(self):
    #     bom_ids = []
    #     for rec in self.design_ids:
    #         if rec.state != "approve":
    #             raise UserError("Work Order design is waiting for approval,please approve it.")
    #         else:
    #             val = {
    #                 'product_tmpl_id': rec.product_id.product_tmpl_id.id,
    #             }
    #             bom_id = self.env['mrp.bom'].create(val)
    #             bom_ids.append(bom_id.id)
    #             list = [(5, 0, 0)]
    #             for x in rec.operation_ids:
    #                 val = {
    #                     'name': x.name,
    #                     'workcenter_id': x.workcenter_id.id,
    #                     'worksheet_type': x.worksheet_type,
    #                     'note': x.note,
    #                     'worksheet': x.worksheet,
    #                     'worksheet_google_slide': x.worksheet_google_slide,
    #                     'time_cycle_manual': x.time_cycle_manual,
    #                     'bom_id': bom_id.id
    #
    #                 }
    #                 list.append((0, 0, val))
    #             bom_id.update({'operation_ids': list})
    #         self.mdn_ids = bom_ids
    #         self.state = 'mdn'

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for rec in self.design_ids:
            if rec.state != "mdn" and rec.mdn_id.state != "approve":
                raise UserError("Please approve and create MDN from work order design.")
            if rec.state == "mdn" and rec.mdn_id.state != "compenonets_purchased":
                raise UserError("Please purchase the mdn components.")
            for mrp in self.mrp_production_ids:
                for des in self.design_ids:
                    if mrp.product_id.id == des.product_id.id:
                        mrp.bom_id = des.mdn_id.id
        return res
