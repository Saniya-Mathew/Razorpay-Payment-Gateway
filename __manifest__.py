{
    'name': "Payment Provider: Razorpay V25",
    'version': '1.0',
    'category': 'Accounting/Payment Providers',
    'type': 'module',
    'depends': ['payment','website'],
    'summary': "A payment provider covering India.",
    'description': " ",
    'data': [
        'data/auto_invoice.xml',
        'data/payment_method_razorpay.xml',
        'data/payment_provider_data.xml',
        'views/payment_provider_views.xml',
        'views/payment_razorpay_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'razorpay_payment/static/src/js/razorpay_v25.js'
        ],
    },
    'license': 'LGPL-3',
    'installable': True,
}

