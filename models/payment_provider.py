import pprint
import uuid
from datetime import timedelta

import requests
from odoo import models, fields,_
from urllib.parse import urlencode
from odoo.exceptions import RedirectWarning, ValidationError
from odoo.http import request, _logger
from odoo.addons.payment_razorpay import const
from odoo.addons.payment_razorpay_oauth import const as oauth_const
from odoo.addons.payment_razorpay_oauth.controllers.onboarding import RazorpayController



class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[('razorpay_v25', "Razorpay V25")],ondelete={'razorpay_v25': 'cascade'},)
    razorpay_v25_key_id = fields.Char(string="Key Id")
    razorpay_v25_key_secret = fields.Char(string="key Secret")
    razorpay_v25_webhook_secret = fields.Char(string="Webhook Secret")


    def action_razorpay_redirect_to_oauth_url(self):
        """ Redirect to the Razorpay OAuth URL.

        Note: `self.ensure_one()`

        :return: An URL action to redirect to the Razorpay OAuth URL.
        :rtype: dict
        """
        self.ensure_one()

        if self.company_id.currency_id.name not in const.SUPPORTED_CURRENCIES:
            raise RedirectWarning(
                _(
                    "Razorpay is not available in your country; please use another payment"
                    " provider."
                ),
                self.env.ref('payment.action_payment_provider').id,
                _("Other Payment Providers"),
            )

        params = {
            'return_url': f'{self.get_base_url()}{RazorpayController.OAUTH_RETURN_URL}',
            'provider_id': self.id,
            'csrf_token': request.csrf_token(),
        }
        authorization_url = f'{oauth_const.OAUTH_URL}/authorize?{urlencode(params)}'
        return {
            'type': 'ir.actions.act_url',
            'url': authorization_url,
            'target': 'self',
        }

        # === BUSINESS METHODS - OAUTH === #
    def _razorpay_make_request(self, endpoint, payload=None, method='POST'):
        self.ensure_one()

        api_version = self.env.context.get('razorpay_api_version', 'v1')
        url = f'https://api.razorpay.com/{api_version}/{endpoint}'
        auth = (self.razorpay_v25_key_id, self.razorpay_v25_key_secret)

        try:
            if method == 'GET':
                response = requests.get(url, params=payload, auth=auth, timeout=10)
            else:
                response = requests.post(url, json=payload, auth=auth, timeout=10)

            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                _logger.exception("Invalid API request at %s with data:\n%s", url, pprint.pformat(payload))
                raise ValidationError("Razorpay: " + _(
                    "Razorpay gave us the following information: '%s'",
                    response.json().get('error', {}).get('description')
                ))
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            _logger.exception("Unable to reach endpoint at %s", url)
            raise ValidationError(
                "Razorpay: " + _("Could not establish the connection to the API.")
            )
        return response.json()

