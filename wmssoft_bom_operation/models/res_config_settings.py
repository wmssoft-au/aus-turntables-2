# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    lead_time_variance = fields.Float('Lead Time Variance', default=0.0, config_parameter='wmssoft_bom_operation.lead_time_variance')