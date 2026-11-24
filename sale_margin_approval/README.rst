====================
Sale Margin Approval
====================

This module adds a margin check to sales quotations.

- **Margin Percentage**: (Total - Untaxed Amount) / Untaxed Amount x 100, rounded to two
  decimals. An order without untaxed amount shows 0%.
- **Requires Manager Approval**: set when the margin percentage is below 10%. The form
  shows both values in red.
- **Request Manager Approval**: a button on quotations below 10%. It logs an internal note
  in the chatter and marks a draft quotation as sent. Confirmed and cancelled orders are
  left unchanged.
- **Show Margin Info**: a button next to the print button on the customer portal. It loads
  both values from ``/my/orders/<id>/margin_info`` (JSON-RPC) and shows them in a
  collapsible panel.

**Table of contents**

.. contents::
   :local:

Usage
=====

#. Create a quotation with one product of 100 before tax and a 9% tax. The Margin
   Information section shows 9.00 in red and the approval flag is set.
#. Click **Request Manager Approval**: a note is logged in the chatter and the quotation
   is marked as sent.
#. Change the tax to 10%: the margin shows 10.00, the flag is cleared and the button is
   hidden.
#. Open the order on the customer portal and click **Show Margin Info** next to the print
   button.

The route can also be called directly with the order's access token::

    curl -X POST -H "Content-Type: application/json" \
      -d '{"jsonrpc": "2.0", "method": "call", "params": {"access_token": "<token>"}}' \
      http://localhost:8069/my/orders/<order id>/margin_info

Known issues / Roadmap
======================

- The percentage follows the specification: it compares the total with and without
  taxes, so it equals the tax rate of the order and does not use product cost.
- The module only requests an approval. Granting it and blocking the confirmation are not
  part of the specification.

Credits
=======

Authors
-------

- Oranjewood

Contributors
------------

- Oranjewood

  - Palcza Szilard

License
-------

Odoo Proprietary License v1.0 (OPL-1), see the ``LICENSE`` and ``COPYRIGHT`` files.
