1. Create a quotation with one product of 100 before tax and a 9% tax. The Margin
   Information section shows 9.00 in red and the approval flag is set.
2. Click **Request Manager Approval**: a note is logged in the chatter and the quotation
   is marked as sent.
3. Change the tax to 10%: the margin shows 10.00, the flag is cleared and the button is
   hidden.
4. Open the order on the customer portal and click **Show Margin Info** next to the
   print button.

The route can also be called directly with the order's access token:

```
curl -X POST -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "call", "params": {"access_token": "<token>"}}' \
  http://localhost:8069/my/orders/<order id>/margin_info
```
