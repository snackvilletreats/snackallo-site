from flask import Flask, render_template_string, session, redirect, url_for, request
import razorpay

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Replace these with your actual Razorpay credentials
razorpay_client = razorpay.Client(auth=("YOUR_RAZORPAY_KEY_ID", "YOUR_RAZORPAY_KEY_SECRET"))

base_template = """
<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1.0'>
  <title>{{ title }}</title>
  <link rel='stylesheet' href='/static/style.css'>
</head>
<body>
  <header>
    <img src='/static/images/snackallo-logo.png' alt='Snackallo Logo' style='height:60px; vertical-align: middle;'>
    <h1 style='display:inline; margin-left:10px;'>Snackallo</h1>
    <nav>
      <a href='/'>Home</a>
      <a href='/shop'>Shop</a>
      <a href='/about'>About Us</a>
      <a href='/contact'>Contact</a>
      <a href='/faq'>FAQs</a>
      <a href='/cart'>Cart ({{ cart_count }})</a>
    </nav>
  </header>
  <main>
    {{ content | safe }}
  </main>
  <footer>
    <p>&copy; 2025 Snackville Treats LLP | snackallo.com</p>
  </footer>
</body>
</html>
"""

products = {
    'banana': {'name': 'Banana Chips', 'price': 100, 'img': 'banana-chips.jpg'},
    'mixture': {'name': 'Spicy Mixture', 'price': 80, 'img': 'mixture.jpg'},
    'achappam': {'name': 'Achappam', 'price': 120, 'img': 'achappam.jpg'},
}

@app.before_request
def make_cart():
    session.setdefault('cart', {})

def render_page(title, content):
    cart_count = sum(session['cart'].values())
    return render_template_string(base_template, title=title, content=content, cart_count=cart_count)

@app.route('/')
def home():
    content = """
    <section class='hero'>
      <h2>Pure Kerala Taste in Every Bite!</h2>
      <p>Authentic banana chips and traditional snacks made with love.</p>
      <a href='/shop' class='btn'>Shop Now</a>
    </section>
    """
    return render_page('Snackallo - Home', content)

@app.route('/shop')
def shop():
    cards = ""
    for pid, p in products.items():
        cards += f"""
        <div class='product-card'>
            <img src='/static/images/{p['img']}' alt='{p['name']}'>
            <h4>{p['name']}</h4>
            <p>₹{p['price']} / 100g</p>
            <form action='/add-to-cart' method='POST'>
                <input type='hidden' name='product_id' value='{pid}'>
                <button type='submit'>Add to Cart</button>
            </form>
        </div>"""
    content = f"""
    <h2>Shop All Products</h2>
    <div class='product-list'>
        {cards}
    </div>
    """
    return render_page('Shop - Snackallo', content)

@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    pid = request.form['product_id']
    session['cart'][pid] = session['cart'].get(pid, 0) + 1
    session.modified = True
    return redirect(url_for('cart'))

@app.route('/remove-from-cart', methods=['POST'])
def remove_from_cart():
    pid = request.form['product_id']
    if pid in session['cart']:
        session['cart'].pop(pid)
        session.modified = True
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    items = ""
    total = 0
    for pid, qty in session['cart'].items():
        p = products[pid]
        subtotal = p['price'] * qty
        total += subtotal
        items += f"""
        <li>
          <img src='/static/images/{p['img']}' alt='{p['name']}' class='cart-img'>
          {p['name']} x {qty} = ₹{subtotal}
          <form action='/remove-from-cart' method='POST' style='display:inline; margin-left:10px;'>
            <input type='hidden' name='product_id' value='{pid}'>
            <button type='submit' class='remove-btn'>Remove</button>
          </form>
        </li>
        """
    content = f"""
    <h2>Your Shopping Cart</h2>
    <ul>{items or '<li>Your cart is empty.</li>'}</ul>
    <h3>Total: ₹{total}</h3>
    {"<form action='/checkout' method='POST'>" if total > 0 else ""}
      <input type='hidden' name='amount' value='{total * 100}'>
      <button type='submit' class='btn' {'disabled' if total == 0 else ''}>Pay Now</button>
    {"</form>" if total > 0 else ""}
    """
    return render_page('Cart - Snackallo', content)

@app.route('/checkout', methods=['POST'])
def checkout():
    amount = int(request.form['amount'])
    try:
        order = razorpay_client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": '1'
        })
        session['cart'] = {}
        content = f"""
        <h2>Payment Initiated</h2>
        <p>Order ID: {order['id']}</p>
        <form>
          <script
            src='https://checkout.razorpay.com/v1/checkout.js'
            data-key='YOUR_RAZORPAY_KEY_ID'
            data-amount='{amount}'
            data-currency='INR'
            data-order_id='{order['id']}'
            data-buttontext='Pay with Razorpay'
            data-name='Snackallo'
            data-description='Snack Purchase'
            data-theme.color='#F37254'
          ></script>
        </form>
        """
        return render_page('Checkout - Snackallo', content)
    except Exception as e:
        return render_page('Payment Error', f"<h2>Payment Error</h2><p>{str(e)}</p>")

@app.route('/about')
def about():
    content = """
    <h2>About Snackallo</h2>
    <p>Snackville Treats LLP, established in 2024, brings the flavors of Kerala to every corner of India. Under the brand Snackallo, we handcraft banana chips and traditional snacks with the highest quality standards.</p>
    <h3>Our Founders</h3>
    <ul>
      <li>Mohammed Shanib - CEO</li>
      <li>Abdul Vajid SVP - Designated Partner</li>
      <li>Fayaz KV - Managing Director</li>
    </ul>
    """
    return render_page('About Us - Snackallo', content)

@app.route('/contact')
def contact():
    content = """
    <h2>Contact Us</h2>
    <p>Phone: +91-7736 944 344</p>
    <p>Email: care@snackallo.com</p>
    <form>
      <input type='text' placeholder='Your Name'><br>
      <input type='email' placeholder='Your Email'><br>
      <textarea placeholder='Your Message'></textarea><br>
      <button type='submit'>Send Message</button>
    </form>
    """
    return render_page('Contact - Snackallo', content)

@app.route('/faq')
def faq():
    content = """
    <h2>Frequently Asked Questions</h2>
    <ul>
      <li><strong>Where do you ship?</strong> We ship pan-India.</li>
      <li><strong>Are your snacks preservative-free?</strong> Yes, all our products are made fresh without preservatives.</li>
      <li><strong>Do you offer bulk/corporate orders?</strong> Yes, contact us for details.</li>
    </ul>
    """
    return render_page('FAQs - Snackallo', content)

if __name__ == '__main__':
    app.run(debug=True)
