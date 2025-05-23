# -*- coding: utf-8 -*-
import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class RazorpayController(http.Controller):
    @http.route('/razorpay_v25/verify_payment', type='json', auth='public')
    def razorpay_payment_verification(self, reference, razorpay_payment_id):
        """Verify Razorpay payment"""
        payment = request.env['payment.transaction'].sudo().search(
            [('reference', '=', reference), ('provider_code', '=', 'razorpay_v25')], limit=1)

        if not payment:
            return {'error': f"No transaction found with reference: {reference}"}

        provider = payment.provider_id
        payment_data = provider._razorpay_make_request(f'payments/{razorpay_payment_id}', method='GET')
        _logger.info("Razorpay payment data: %s", payment_data)

        if payment_data.get('status') == 'captured':
            # ✅ Use order_id in the reference
            print(payment_data)
            order_id = payment_data.get('description') or 'unknown'
            print(order_id)
            payment.provider_reference = f"razorpay V25-{order_id}"
            payment._set_done()
            return {'success': True}
        else:
            _logger.warning(
                f"Payment {razorpay_payment_id} status is {payment_data.get('status')}, not captured"
            )
            return {'warning': f"Payment status: {payment_data.get('status')}"}


# reference = notification_data.get('txnid').split('_')[0]
# tx = self.search([('reference', '=', reference)])
# if tx.state == 'done' and not tx.invoice_ids:
#     order = tx.sale_order_ids
#     print(order)
#     invoice = self.env['account.move'].sudo().create({
#         'move_type': 'out_invoice',
#         'partner_id': tx.partner_id.id,
#         'invoice_date': fields.Date.today(),
#         'invoice_line_ids': [fields.Command.create
#             ({
#                 'product_id': line.product_id.id,
#                 'name': line.name,
#                 'quantity': line.product_uom_qty,
#                 'price_unit': line.price_unit,
#             })for line in order.order_line
#         ],
#     })
#
#     tx.invoice_ids = [fields.Command.link(invoice.id)]
#
# return tx


# def create_invoice_from_payment(self):
#     """Create an invoice and mark it as paid"""
#     order = self.sale_order_ids[0]
#     if order.state not in ('sale', 'done'):
#         order.action_confirm()
#
#     invoice_vals = {
#         'partner_id': order.partner_id.id,
#         'move_type': 'out_invoice',
#         'ref': order.name,
#         'invoice_date': fields.Date.today(),
#         'invoice_line_ids': [
#             Command.create({
#                 'product_id': line.product_id.id,
#                 'quantity': line.product_uom_qty,
#                 'price_unit': line.price_unit,
#                 'sale_line_ids': [line.id],
#                 'name': line.name,
#             }) for line in order.order_line],
#     }
#     invoice = self.env['account.move'].sudo().create(invoice_vals)
#     invoice.action_post()
#
#     # Register payment to mark invoice as paid
#     payment = self.env['account.payment'].sudo().create({
#         'payment_type': 'inbound',
#         'partner_type': 'customer',
#         'partner_id': order.partner_id.id,
#         'amount': invoice.amount_total,
#         'currency_id': invoice.currency_id.id,
#         'journal_id': self.env['account.journal'].search(
#             [('type', '=', 'bank'), ('company_id', '=', invoice.company_id.id)], limit=1).id,
#         'payment_method_id': self.env.ref('account.account_payment_method_manual_in').id,
#         'date': fields.Date.today(),
#         'invoice_ids': [(6, 0, [invoice.id])],
#     })
#     payment.action_post()
#
#     # Reconcile payment with invoice
#     invoice.js_assign_outstanding_line(
#         payment.line_ids.filtered(lambda line: line.account_id.account_type == 'asset_receivable').id)
#
#     return invoice

# from . import models
#
# def post_init_hook(cr, registry):
#     from odoo.api import Environment
#     env = Environment(cr, SUPERUSER_ID, {})
#     env['ir.config_parameter'].set_param('sale.auto_invoice', True)

#
# 'installable': True,
# 'post_init_hook': 'post_init_hook',

# <?xml version="1.0" encoding="utf-8"?>
# <odoo>
#     <record id="sale_config_settings_auto_invoice" model="res.config.settings">
#         <field name="automatic_invoice" eval="True"/>
#     </record>
# </odoo>