# import razorpay_payment
# from odoo.custom_addons import razorpay_payment
from odoo import http
from odoo.http import request

class RazorpayController(http.Controller):

    @http.route(['/payment/razorpay/checkout'], type='http', auth='public', website=True)
    def razorpay_checkout(self, **kwargs):
        order = request.env['sale.order'].sudo().browse(int(kwargs.get('order_id')))
        acquirer = request.env['payment.acquirer'].sudo().search([('provider', '=', 'razorpay_v25')], limit=1)
        # client = razorpay_payment.Client(auth=(acquirer.razorpay_key_id, acquirer.razorpay_key_secret))

        razorpay_order = client.order.create({
            "amount": int(order.amount_total * 100),
            "currency": "INR",
            "receipt": str(order.name),
            "payment_capture": 1
        })

        values = {
            'key_id': acquirer.razorpay_key_id,
            'order_id': razorpay_order['id'],
            'amount': int(order.amount_total * 100),
            'order': order,
        }
        return request.render('razorpay_payment.razorpay_template', values)

    @http.route(['/payment/razorpay/return'], type='http', auth='public', csrf=False)
    def razorpay_return(self, **post):
        return request.redirect('/payment/success')