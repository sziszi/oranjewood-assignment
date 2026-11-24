# Copyright 2026 Oranjewood
# License OPL-1 (Odoo Proprietary License v1.0), see the LICENSE file.

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_round


class SaleOrder(models.Model):
    _inherit = "sale.order"

    margin_percentage = fields.Float(
        compute="_compute_margin_percentage",
        digits=(16, 2),
        help="(Total - Untaxed Amount) / Untaxed Amount x 100.",
    )
    requires_manager_approval = fields.Boolean(
        compute="_compute_margin_percentage",
        help="Set when the margin percentage is below 10%.",
    )

    @api.depends("amount_total", "amount_untaxed")
    def _compute_margin_percentage(self):
        for order in self:
            margin = order.amount_untaxed and (
                (order.amount_total - order.amount_untaxed) / order.amount_untaxed * 100
            )
            order.margin_percentage = float_round(margin, precision_digits=2)
            order.requires_manager_approval = (
                float_compare(order.margin_percentage, 10.0, precision_digits=2) < 0
            )

    def action_request_manager_approval(self):
        self.ensure_one()
        if self.state not in ("draft", "sent") or not self.requires_manager_approval:
            raise UserError(
                _("Only quotations below the approval threshold need a request.")
            )
        if self.state == "draft":
            self.action_quotation_sent()
        self.message_post(
            body=_("Manager approval requested for low margin order."),
            subtype_xmlid="mail.mt_note",
        )
        return True
