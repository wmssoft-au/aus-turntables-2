# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    is_outsource_operation = fields.Boolean('Outsourced Operation', default=False)
    workorder_id = fields.Many2one('mrp.workorder', 'Workorder')

    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        for order in self:
            if order.is_outsource_operation and order.workorder_id:
                if order.workorder_id.date_start:
                    raise UserError(_('You cannot confirm a purchase order for an outsource operation with a start date.'))
                order.workorder_id.write({'date_planned_start': order.date_planned}) 
                order.workorder_id._onchange_date_planned_start()   
            moves = [] 
            for line in self.order_line:
                move_vals = order.workorder_id.production_id._get_move_raw_values(line.product_id, line.product_qty, line.product_uom)
                move_vals['is_outsource_move'] = True
                moves.append((0, 0, move_vals))
            order.workorder_id.production_id.move_raw_ids = moves
        return res