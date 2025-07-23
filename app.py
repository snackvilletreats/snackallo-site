from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'

products = [
    {"id": 1, "name": "Banana Chips", "price": 100, "image": "banana-chips.jpg"},
    {"id": 2, "name": "Mixture", "price": 80, "image": "mixture.jpg"},
    {"id": 3, "name": "Achappam", "price": 120, "image": "achappam.jpg"}
]

@app.route('/')
def home():
    return render_template('index.html', products=products)

@app.route('/shop')
def shop():
    return render_template('shop.html', products=products)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    return render_template('cart.html', cart=cart)

@app.route('/add-to-cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    cart = session.get('cart', [])
    for item in cart:
        if item["id"] == product_id:
            item["quantity"] += quantity
            break
    else:
        product = next((p for p in products if p["id"] == product_id), None)
        if product:
            cart.append({**product, "quantity": quantity})
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/update-quantity', methods=['POST'])
def update_quantity():
    product_id = int(request.form['id'])
    action = request.form['action']
    cart = session.get('cart', [])
    for item in cart:
        if item["id"] == product_id:
            if action == "increase":
                item["quantity"] += 1
            elif action == "decrease":
                item["quantity"] -= 1
                if item["quantity"] <= 0:
                    cart.remove(item)
            break
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/remove-from-cart', methods=['POST'])
def remove_from_cart():
    product_id = int(request.form['id'])
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != product_id]
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['POST'])
def checkout():
    cart = session.get('cart', [])
    session.pop('cart', None)
    return render_template('thankyou.html', cart=cart)

if __name__ == '__main__':
    app.run(debug=True)
