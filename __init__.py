from odoo import SUPERUSER_ID
from . import models
from . import controllers

# def pre_init_hook(cr, registry):
#     from odoo.api import Environment
#     env = Environment(cr, SUPERUSER_ID, {})
#     env['ir.config_parameter'].set_param('sale.auto_invoice', True)
