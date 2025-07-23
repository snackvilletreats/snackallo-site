from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'

products = [
    {"id": 1, "name": "Banana Chips", "price": 100, "image": "banana-chips.jpg"},
    {"id": 2, "name": "Mixture", "price": 80, "image": "mixture.jpg"},
    {"id": 3, "name": "Achappam", "price": 120, "image": "achappam.jpg"},
]

def find_product(product_id):
    return next((p for p in products if p['id'] == product_id), None)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/shop')
def shop():
    return render_template('shop.html', products=products)

@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    return render_template('cart.html', cart=cart)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    try:
        product_id = int(request.form['product_id'])
        quantity = int(request.form.get('quantity', 1))
        if quantity < 1:
            quantity = 1
    except (ValueError, KeyError):
        return redirect(url_for('shop'))

    product = find_product(product_id)
    if not product:
        return redirect(url_for('shop'))

    cart = session.get('cart', [])

    # Update quantity if product exists
    for item in cart:
        if item['id'] == product_id:
            item['quantity'] += quantity
            break
    else:
        cart.append({
            'id': product['id'],
            'name': product['name'],
            'price': product['price'],
            'quantity': quantity
        })

    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/update_quantity', methods=['POST'])
def update_quantity():
    product_id = int(request.form['product_id'])
    quantity = int(request.form['quantity'])
    cart = session.get('cart', [])
    for item in cart:
        if item['id'] == product_id:
            if quantity > 0:
                item['quantity'] = quantity
            else:
                cart.remove(item)
            break
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    product_id = int(request.form['product_id'])
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != product_id]
    session['cart'] = cart
    return redirect(url_for('cart'))

if __name__ == '__main__':
    app.run(debug=True)
