# Copyright 2026 Oranjewood
# License OPL-1 (Odoo Proprietary License v1.0), see the LICENSE file.

from odoo import _, http
from odoo.exceptions import AccessError, MissingError

from odoo.addons.sale.controllers import portal


class CustomerPortal(portal.CustomerPortal):
    @http.route(
        "/my/orders/<int:order_id>/margin_info",
        type="json",
        auth="public",
        methods=["POST"],
        website=True,
    )
    def portal_order_margin_info(self, order_id, access_token=None, **kwargs):
        try:
            order_sudo = self._document_check_access(
                "sale.order", order_id, access_token=access_token
            )
        except (AccessError, MissingError):
            raise AccessError(_("This order is not available.")) from None
        return {
            "margin_percentage": order_sudo.margin_percentage,
            "requires_manager_approval": order_sudo.requires_manager_approval,
        }
