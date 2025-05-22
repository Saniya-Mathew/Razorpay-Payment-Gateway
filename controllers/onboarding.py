# -*- coding: utf-8 -*-
import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

class RazorpayController(http.Controller):
    @http.route('/razorpay_v25/verify_payment', type='json', auth='public')
    def razorpay_payment_verification(self, reference, razorpay_payment_id):
        """This function check the state and verify the state of razorpay"""
        payment = request.env['payment.transaction'].sudo().search(
            [('reference', '=', reference)], limit=1)
        if payment:
            provider = payment.provider_id
            payment_data = provider._razorpay_make_request(f'payments/{razorpay_payment_id}',method='GET')
            print(payment_data)
            if payment_data.get('status') == 'captured':
                payment._set_done()
                return {'success': True}
            else:
                _logger.warning(
                    f"Payment {razorpay_payment_id} status is {payment_data.get('status')}, not captured"
                )
                return {'warning': f"Payment status: {payment_data.get('status')}"}
        return {'error': f"No transaction found with reference: {reference}"}