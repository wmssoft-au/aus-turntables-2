# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class StockMove(models.Model):
    _inherit = 'stock.move'

    is_outsource_move = fields.Boolean('Outsourced Move', default=False)