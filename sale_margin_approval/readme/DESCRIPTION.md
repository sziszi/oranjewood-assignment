This module adds a margin check to sales quotations.

- **Margin Percentage**: (Total - Untaxed Amount) / Untaxed Amount x 100, rounded to two
  decimals. An order without untaxed amount shows 0%.
- **Requires Manager Approval**: set when the margin percentage is below 10%. The form
  shows both values in red.
- **Request Manager Approval**: a button on quotations below 10%. It logs an internal
  note in the chatter and marks a draft quotation as sent. Confirmed and cancelled
  orders are left unchanged.
- **Show Margin Info**: a button next to the print button on the customer portal. It
  loads both values from `/my/orders/<id>/margin_info` (JSON-RPC) and shows them in a
  collapsible panel.
