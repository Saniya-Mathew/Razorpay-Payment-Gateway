from odoo import models, fields,_
from urllib.parse import urlencode
from odoo.exceptions import RedirectWarning, ValidationError
from odoo.http import request
from odoo.addons.payment_razorpay import const
from odoo.addons.payment_razorpay_oauth import const as oauth_const
from odoo.addons.payment_razorpay_oauth.controllers.onboarding import RazorpayController



class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[('razorpay_v25', "Razorpay_v25")],ondelete={'razorpay_v25': 'set default'})
    razorpay_key_id = fields.Char(string="Razorpay Key Id")
    razorpay_key_secret = fields.Char(string="Razorpay Key Secret")
    razorpay_webhook_secret = fields.Char(string="Razorpay Webhook Secret")


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