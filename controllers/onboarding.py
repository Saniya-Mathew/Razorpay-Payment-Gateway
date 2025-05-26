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
