from flask import Flask, render_template_string, session, redirect, url_for, request
import razorpay

app = Flask(__name__)
app.secret_key = 'your_secret_key'

razorpay_client = razorpay.Client(auth=("YOUR_RAZORPAY_KEY_ID", "YOUR_RAZORPAY_KEY_SECRET"))

@app.route("/")
def home():
    return "<h1>Snackallo Home</h1><p><a href='/shop'>Shop</a></p>"

@app.route("/shop")
def shop():
    return "<h2>Products coming soon...</h2>"

if __name__ == "__main__":
    app.run()
