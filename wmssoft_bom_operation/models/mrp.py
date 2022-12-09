# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    outsource_po_ids = fields.Many2many('purchase.order', string='Outsourced PO', compute='_compute_outsource_po')
    outsource_po_count = fields.Integer(string='Outsourced PO Count', compute='_compute_outsource_po')

    def _compute_outsource_po(self):
        for production in self:
            production.outsource_po_ids = self.env['purchase.order'].search([('origin', '=', production.name), ('is_outsource_operation', '=', True)])
            production.outsource_po_count = len(production.outsource_po_ids)

    def action_confirm(self):
        res = super(MrpProduction, self).action_confirm()
        for workorder in self.workorder_ids:
            if workorder.operation_id.is_outsource_operation:
                partner_id = workorder.operation_id.partner_id
                self.env['purchase.order'].create({'origin': workorder.production_id.name,'is_outsource_operation': True, 'partner_id': partner_id.id, 'workorder_id': workorder.id})     
        return res


    def action_view_purchase_outsource_orders(self):
        self.ensure_one()
        purchase_order_ids = self.outsource_po_ids.ids
        action = {
            'res_model': 'purchase.order',
            'type': 'ir.actions.act_window',
        }
        if len(purchase_order_ids) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': purchase_order_ids[0],
            })
        else:
            action.update({
                'name': _("Purchase Order generated from %s", self.name),
                'domain': [('id', 'in', purchase_order_ids)],
                'view_mode': 'tree,form',
            })
        return action