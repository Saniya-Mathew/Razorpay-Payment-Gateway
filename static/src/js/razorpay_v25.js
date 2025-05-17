<odoo>
  <template id="razorpay_template" name="Razorpay Checkout">
    <form id="razorpay-form">
      <script src="https://checkout.razorpay.com/v1/checkout.js"
              data-key="${key_id}"
              data-amount="${amount}"
              data-currency="INR"
              data-order_id="${order_id}"
              data-buttontext="Pay Now"
              data-name="Odoo Store"
              data-description="Order Payment"
              data-theme.color="#3399cc">
      </script>
    </form>
  </template>
</odoo>