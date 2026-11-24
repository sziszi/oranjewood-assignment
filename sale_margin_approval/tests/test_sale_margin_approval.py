# Copyright 2026 Oranjewood
# License OPL-1 (Odoo Proprietary License v1.0), see the LICENSE file.

from odoo.exceptions import UserError
from odoo.fields import Command
from odoo.tests import HttpCase, tagged
from odoo.tests.common import JsonRpcException
from odoo.tools import mute_logger

from odoo.addons.sale.tests.common import SaleCommon


class SaleMarginApprovalCommon(SaleCommon):
    @classmethod
    def _create_quotation(cls, tax_rate, price_unit=100.0):
        tax = cls.env["account.tax"].create(
            {
                "name": f"Test sales tax {tax_rate}%",
                "amount_type": "percent",
                "amount": tax_rate,
                "type_tax_use": "sale",
            }
        )
        return cls.env["sale.order"].create(
            {
                "partner_id": cls.partner.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": cls.consumable_product.id,
                            "product_uom_qty": 1.0,
                            "price_unit": price_unit,
                            "tax_id": [Command.set(tax.ids)],
                        }
                    )
                ],
            }
        )


@tagged("post_install", "-at_install")
class TestSaleMarginApproval(SaleMarginApprovalCommon):
    def test_margin_percentage_and_threshold(self):
        order = self._create_quotation(10.0)
        self.assertEqual(order.margin_percentage, 10.0)
        self.assertFalse(order.requires_manager_approval)
        order.order_line.tax_id = [Command.clear()]
        self.assertEqual(order.margin_percentage, 0.0)
        self.assertTrue(order.requires_manager_approval)

    def test_margin_percentage_rounding(self):
        # 10% tax on 1000.04 is rounded to 100.00, a raw margin of 9.9996%:
        # it is shown as 10.00, so it must not be flagged.
        order = self._create_quotation(10.0, price_unit=1000.04)
        self.assertEqual(order.margin_percentage, 10.0)
        self.assertFalse(order.requires_manager_approval)
        order = self._create_quotation(9.99)
        self.assertEqual(order.margin_percentage, 9.99)
        self.assertTrue(order.requires_manager_approval)

    def test_margin_percentage_without_untaxed_amount(self):
        self.assertEqual(self.empty_order.margin_percentage, 0.0)
        self.assertTrue(self.empty_order.requires_manager_approval)

    def test_request_manager_approval(self):
        order = self._create_quotation(9.0)
        order.action_request_manager_approval()
        self.assertEqual(order.state, "sent")
        self.assertTrue(
            any(
                "Manager approval requested for low margin order." in body
                for body in order.message_ids.mapped("body")
            )
        )
        # A sent quotation can be requested again, a confirmed order cannot.
        order.action_request_manager_approval()
        order.action_confirm()
        with self.assertRaises(UserError):
            order.action_request_manager_approval()
        with self.assertRaises(UserError):
            self._create_quotation(21.0).action_request_manager_approval()


@tagged("post_install", "-at_install")
class TestSaleMarginInfoRoute(HttpCase, SaleMarginApprovalCommon):
    def test_margin_info_route(self):
        order = self._create_quotation(9.0)
        url = f"/my/orders/{order.id}/margin_info"
        self.authenticate(None, None)
        result = self.make_jsonrpc_request(
            url, {"access_token": order._portal_ensure_token()}
        )
        self.assertEqual(
            result, {"margin_percentage": 9.0, "requires_manager_approval": True}
        )
        with mute_logger("odoo.http"), self.assertRaises(JsonRpcException):
            self.make_jsonrpc_request(url, {"access_token": "invalid"})
