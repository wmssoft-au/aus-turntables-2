# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class MrpRoutingWorkcenter(models.Model):
    _inherit = 'mrp.routing.workcenter'

    is_outsource_operation = fields.Boolean('Outsourced Operation', default=False)
    partner_id = fields.Many2one('res.partner', 'Partner')
    lead_time = fields.Float('Estimated Lead Time', default=0.0)
    estimated_cost = fields.Float('Estimated Cost', default=0.0)
    lead_time_variance = fields.Float('Lead Time Variance', default=0.0)
    outsource_uom_id = fields.Many2one('uom.uom', 'Outsource UoM', default=lambda self: self.env.ref('uom.product_uom_day'))

    @api.onchange('lead_time', 'lead_time_variance')
    def _onchange_lead_time(self):
        if self.lead_time:
            lead_time_variance = float(self.env['ir.config_parameter'].sudo().get_param('wmssoft_bom_operation.lead_time_variance'))
            self.time_cycle_manual = self.lead_time * lead_time_variance if lead_time_variance else 0.0