from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Dummy product data
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

@app.route('/add-to-cart/<int:product_id>')
def add_to_cart(product_id):
    cart = session.get('cart', [])
    found = False

    for item in cart:
        if item["id"] == product_id:
            item["quantity"] += 1
            found = True
            break

    if not found:
        product = next((p for p in products if p["id"] == product_id), None)
        if product:
            cart.append({
                "id": product["id"],
                "name": product["name"],
                "price": product["price"],
                "quantity": 1
            })

    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/update-cart', methods=['POST'])
def update_cart():
    product_ids = request.form.getlist('product_ids')
    quantities = request.form.getlist('quantities')
    remove_ids = request.form.getlist('remove')

    updated_cart = []

    for i in range(len(product_ids)):
        product_id = int(product_ids[i])
        quantity = int(quantities[i])

        if str(product_id) in remove_ids:
            continue  # Skip this item if marked for removal

        for product in products:
            if product["id"] == product_id:
                updated_cart.append({
                    "id": product["id"],
                    "name": product["name"],
                    "price": product["price"],
                    "quantity": quantity
                })
                break

    session['cart'] = updated_cart
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['POST'])
def checkout():
    cart = session.get('cart', [])
    session.pop('cart', None)
    return render_template('thankyou.html', cart=cart)

if __name__ == '__main__':
    app.run(debug=True)
