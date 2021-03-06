# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)
from openerp import api, fields, models


class RmaOrder(models.Model):
    _inherit = "rma.order"

    @api.depends('rma_line_ids', 'rma_line_ids.procurement_ids')
    @api.multi
    def _compute_po_count(self):
        for rec in self:
            purchases = rec.mapped('rma_line_ids.procurement_ids.purchase_id')
            rec.po_count = len(purchases)

    @api.multi
    def _compute_origin_po_count(self):
        for rma in self:
            purchases = rma.mapped(
                'rma_line_ids.purchase_order_line_id.order_id')
            rma.origin_po_count = len(purchases)

    po_count = fields.Integer(
        compute='_compute_po_count', string='# of PO')
    origin_po_count = fields.Integer(
        compute='_compute_origin_po_count', string='# of Origin PO')

    @api.multi
    def action_view_purchase_order(self):
        action = self.env.ref('purchase.purchase_rfq')
        result = action.read()[0]
        po_ids = self.mapped('rma_line_ids.procurement_ids.purchase_id').ids
        result['domain'] = [('id', 'in', po_ids)]
        return result

    @api.multi
    def action_view_origin_purchase_order(self):
        action = self.env.ref('purchase.purchase_rfq')
        result = action.read()[0]
        po_ids = self.mapped(
            'rma_line_ids.purchase_order_line_id.order_id').ids
        result['domain'] = [('id', 'in', po_ids)]
        return result
