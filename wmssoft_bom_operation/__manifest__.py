# -*- coding: utf-8 -*-
#############################################################################
#
#    WMSSOFT
#
#    Copyright (C) 2020-2020 WMSSOFT (<https://www.wmssoft.com.au/>).
#
#############################################################################
{
    "name": "WMSSoft Bom Outsource Operation",

    "summary": """
        Simplify your Outsourcing using Operations instead of Products.""",

    "description": """
         Simplify your BOMs to specify the creation of Outsourcing Operations instead of creating sub BOMs.
    """,

    "author": "WMSSoft Pty Ltd",
    "company": "WMSSoft Pty Ltd",
    "maintainer": "WMSSoft Pty Ltd",
    "website": "https://www.wmssoft.com.au/",
    "license": "OPL-1",
    "category": "Manufacturing",
    "version": "15.0.0.1",
    "depends": ["mrp", "stock", "mrp_account_enterprise", "sale_stock"],
    "images": ['static/description/automatic_outsourcing.gif'],
    "data": [
            "reports/mrp_cost_structure_view.xml",
            "reports/mrp_report_bom_structure.xml",
            "views/mrp_workcenter_view.xml",
            "views/mrp_view.xml",
            "views/res_config_settings_view.xml",
    ],
    'assets': {
        'web.assets_backend': [
            'wmssoft_bom_operation/static/src/js/mrp_bom_report.js',
        ],
    },
    "installable": True,
    "auto_install": False,
}