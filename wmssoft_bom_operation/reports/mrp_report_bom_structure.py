# -*- coding: utf-8 -*-

import json

from odoo import api, models, _
from odoo.tools import float_round



class ReportBomStructure(models.AbstractModel):
    _inherit = 'report.mrp.report_bom_structure'

    def _get_bom(self, bom_id=False, product_id=False, line_qty=False, line_id=False, level=False):
        res = super(ReportBomStructure, self)._get_bom(bom_id, product_id, line_qty, line_id, level)
        bom = self.env['mrp.bom'].browse(bom_id)
        custom_operation_cost = self._get_custom_operation_cost(bom, 0)
        res['total'] += sum([op['total'] for op in custom_operation_cost])
        res['custom_operation_cost'] = custom_operation_cost
        res['custom_operations_time'] = sum([op['duration_expected'] for op in custom_operation_cost])
        res['custom_operations_cost_total'] = sum([op['total'] for op in custom_operation_cost])
        return res


    def _get_custom_operation_cost(self, bom, level):
        custom_operation_cost = []
        for operation_id in bom.operation_ids.filtered(lambda x: x.is_outsource_operation):
            name = operation_id.name
            if operation_id.partner_id.name:
                name = operation_id.name + ' - ' + operation_id.partner_id.name
            custom_operation_cost.append({
                'level': level or 0,
                'name': name,
                'duration_expected': operation_id.lead_time,
                'total': operation_id.estimated_cost,
            })
        return custom_operation_cost


    def _get_sub_lines(self, bom, product_id, line_qty, line_id, level, child_bom_ids, unfolded):
        data = self._get_bom(bom_id=bom.id, product_id=product_id, line_qty=line_qty, line_id=line_id, level=level)
        bom_lines = data['components']
        lines = []
        for bom_line in bom_lines:
            lines.append({
                'name': bom_line['prod_name'],
                'type': 'bom',
                'quantity': bom_line['prod_qty'],
                'uom': bom_line['prod_uom'],
                'prod_cost': bom_line['prod_cost'],
                'bom_cost': bom_line['total'],
                'level': bom_line['level'],
                'code': bom_line['code'],
                'child_bom': bom_line['child_bom'],
                'prod_id': bom_line['prod_id']
            })
            if bom_line['child_bom'] and (unfolded or bom_line['child_bom'] in child_bom_ids):
                line = self.env['mrp.bom.line'].browse(bom_line['line_id'])
                lines += (self._get_sub_lines(line.child_bom_id, line.product_id.id, bom_line['prod_qty'], line, level + 1, child_bom_ids, unfolded))
        if data['operations']:
            lines.append({
                'name': _('Operations'),
                'type': 'operation',
                'quantity': data['operations_time'],
                'uom': _('minutes'),
                'bom_cost': data['operations_cost'],
                'level': level,
            })
            for operation in data['operations']:
                if unfolded or 'operation-' + str(bom.id) in child_bom_ids:
                    lines.append({
                        'name': operation['name'],
                        'type': 'operation',
                        'quantity': operation['duration_expected'],
                        'uom': _('minutes'),
                        'bom_cost': operation['total'],
                        'level': level + 1,
                    })
        # ---------------------Start
        if data['custom_operation_cost']:
            lines.append({
                'name': _('Operation Cost'),
                'type': 'operation',
                'quantity': data['duration_expected'],
                'uom': _('days'),
                'bom_cost': data['custom_operation_cost']['total'],
                'level': level,
            })
            for operation in data['custom_operation_cost']:
                if unfolded or 'operation-' + str(bom.id) in child_bom_ids:
                    lines.append({
                        'name': operation['name'],
                        'type': 'operation',
                        'quantity': operation['duration_expected'],
                        'uom': _('days'),
                        'bom_cost': operation['total'],
                        'level': level + 1,
                    })
        # ---------------------End
        if data['byproducts']:
                lines.append({
                    'name': _('Byproducts'),
                    'type': 'byproduct',
                    'uom': False,
                    'quantity': data['byproducts_total'],
                    'bom_cost': data['byproducts_cost'],
                    'level': level,
                })
                for byproduct in data['byproducts']:
                    if unfolded or 'byproduct-' + str(bom.id) in child_bom_ids:
                        lines.append({
                            'name': byproduct['product_name'],
                            'type': 'byproduct',
                            'quantity': byproduct['product_qty'],
                            'uom': byproduct['product_uom'],
                            'prod_cost': byproduct['product_cost'],
                            'bom_cost': byproduct['bom_cost'],
                            'level': level + 1,
                        })
        return lines

    @api.model
    def get_custom_operations(self, product_id=False, bom_id=False, qty=0, level=0):
        bom = self.env['mrp.bom'].browse(bom_id)
        product = self.env['product.product'].browse(product_id)
        lines = self._get_custom_operation_cost(bom, level)
        values = {
            'bom_id': bom_id,
            'currency': self.env.company.currency_id,
            'operations': lines,
            'extra_column_count': self._get_extra_column_count(),
        }
        return self.env.ref('wmssoft_bom_operation.report_mrp_operation_cost_line')._render({'data': values})