from flask import Flask, render_template, session, redirect, url_for, request
import razorpay

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a strong secret key

razorpay_client = razorpay.Client(auth=("YOUR_RAZORPAY_KEY_ID", "YOUR_RAZORPAY_KEY_SECRET"))

products = {
    'banana': {'name': 'Banana Chips', 'price': 100, 'img': 'banana-chips.jpg'},
    'mixture': {'name': 'Spicy Mixture', 'price': 80, 'img': 'mixture.jpg'},
    'achappam': {'name': 'Achappam', 'price': 120, 'img': 'achappam.jpg'},
}

@app.before_request
def make_cart():
    session.setdefault('cart', {})

@app.context_processor
def inject_cart_count():
    return dict(cart_count=sum(session.get('cart', {}).values()))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/shop')
def shop():
    return render_template('shop.html', products=products)

@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    pid = request.form['product_id']
    cart = session['cart']
    cart[pid] = cart.get(pid, 0) + 1
    session.modified = True
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    cart_items = []
    total = 0
    for pid, qty in cart.items():
        p = products.get(pid)
        if p:
            subtotal = p['price'] * qty
            total += subtotal
            cart_items.append({'id': pid, 'name': p['name'], 'price': p['price'], 'qty': qty, 'subtotal': subtotal})
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/update-cart', methods=['POST'])
def update_cart():
    pid = request.form['product_id']
    action = request.form['action']
    cart = session.get('cart', {})
    if pid in cart:
        if action == 'remove':
            cart.pop(pid)
        elif action == 'decrease':
            cart[pid] -= 1
            if cart[pid] <= 0:
                cart.pop(pid)
        elif action == 'increase':
            cart[pid] += 1
    session.modified = True
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['POST'])
def checkout():
    amount = int(float(request.form['amount']) * 100)  # in paise
    order = razorpay_client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": '1'
    })
    session['cart'] = {}  # clear cart
    return render_template('checkout.html', order=order, amount=amount)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

if __name__ == '__main__':
    app.run(debug=True)
