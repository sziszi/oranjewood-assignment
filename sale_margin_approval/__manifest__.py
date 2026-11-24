# Copyright 2026 Oranjewood
# License OPL-1 (Odoo Proprietary License v1.0), see the LICENSE file.
{
    "name": "Sale Margin Approval",
    "summary": "Margin percentage, manager approval request and portal margin info",
    "version": "17.0.1.2.0",
    "category": "Sales/Sales",
    "author": "Oranjewood",
    "license": "OPL-1",
    "installable": True,
    "depends": ["sale"],
    "data": [
        "views/sale_order_views.xml",
        "views/sale_portal_templates.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "sale_margin_approval/static/src/js/sale_margin_info.js",
        ],
    },
}
