from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import smtplib

app = Flask(__name__)
app.secret_key = "smooth_elite_exclusive_2026"

# מאגר מוצרים מורחב עם מלאי וקטגוריות
PRODUCTS = [
    {"id": 1, "name": "BLACK OVERSIZE", "price": 189, "stock": 10, "category": "Shirts", "rating": 5, "image": "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800"},
    {"id": 2, "name": "CARGO TECH", "price": 349, "stock": 5, "category": "Pants", "rating": 4, "image": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=800"},
    {"id": 3, "name": "LEATHER JACKET", "price": 599, "stock": 2, "category": "Outerwear", "rating": 5, "image": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=800"},
    {"id": 4, "name": "SIGNATURE HOODIE", "price": 280, "stock": 0, "category": "Shirts", "rating": 5, "image": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=800"}
]

@app.route('/')
def home():
    user = session.get('user')
    search_query = request.args.get('search', '').lower()
    filtered_products = [p for p in PRODUCTS if search_query in p['name'].lower()] if search_query else PRODUCTS
    return render_template('index.html', products=filtered_products, user=user)

@app.route('/apply_coupon', methods=['POST'])
def apply_coupon():
    code = request.json.get('code')
    if code == "SMOOTH20": return jsonify({"discount": 0.20})
    return jsonify({"error": "קוד לא תקין"}), 400

@app.route('/login_google')
def login_google():
    # כאן צריך להטמיע Google OAuth. לבינתיים, זה מחבר אותך אוטומטית:
    session['user'] = {"name": "אורח VIP", "email": "liel@smooth.com", "points": 150}
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/checkout', methods=['POST'])
def checkout():
    # לוגיקת שליחת המייל (כמו בקוד הקודם)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)