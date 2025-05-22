#-- coding: utf-8 --
from odoo import _, fields, models
from odoo.exceptions import ValidationError
import requests
import logging
import hmac
import hashlib
from odoo.addons.payment_razorpay import const
_logger = logging.getLogger(__name__)

class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[('razorpay_v25', "Razorpay V25")],ondelete={'razorpay_v25': 'cascade'},)
    razorpay_v25_key_id = fields.Char(string="Key Id",required_if_provider='razorpay',
                                      help="Public key provided by Razorpay.")
    razorpay_v25_key_secret = fields.Char(string="key Secret", required_if_provider='razorpay',
                                          groups='base.group_system')
    razorpay_v25_webhook_secret = fields.Char(string="Webhook Secret",groups='base.group_system')

    def _razorpay_make_request(self, endpoint, payload=None, method='POST'):
        self.ensure_one()
        if not self.razorpay_v25_key_id or not self.razorpay_v25_key_secret:
            raise ValidationError(_("Razorpay credentials are missing. Please configure Key ID and Key Secret."))

        url = f"https://api.razorpay.com/v1/{endpoint}"
        auth = (self.razorpay_v25_key_id, self.razorpay_v25_key_secret)
        headers = {'Content-Type': 'application/json'}

        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, auth=auth, params=payload, timeout=10)
            else:
                response = requests.request(method, url, headers=headers, auth=auth, json=payload, timeout=10)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            error_data = response.json().get('error', {})
            msg = error_data.get('description', str(e))
            _logger.error("Razorpay API error: %s", msg)
            raise ValidationError(_("Razorpay API error: %s") % msg)
        except requests.exceptions.RequestException as e:
            _logger.error("Razorpay connection error: %s", str(e))
            raise ValidationError(_("Failed to connect to Razorpay: %s") % str(e))

        return response.json()




