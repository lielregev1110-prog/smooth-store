from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

PRODUCTS = [
    {"id": 1, "name": "SMOOTH BLACK OVERSIZE", "price": 189, "image": "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800"},
    {"id": 2, "name": "CARGO TECH PANTS", "price": 349, "image": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=800"},
    {"id": 3, "name": "URBAN LEATHER JACKET", "price": 599, "image": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=800"},
    {"id": 4, "name": "SMOOTH SIGNATURE HOODIE", "price": 280, "image": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=800"}
]

@app.route('/')
def home():
    search_query = request.args.get('search', '').lower()
    # פונקציית חיפוש: אם המשתמש חיפש משהו, נציג רק את מה שמתאים
    filtered_products = [p for p in PRODUCTS if search_query in p['name'].lower()] if search_query else PRODUCTS
    return render_template('index.html', products=filtered_products)

@app.route('/checkout', methods=['POST'])
def checkout():
    data = request.json
    # כאן נכנסת הלוגיקה ששולחת אליך את האימיילlielregev1110@gmail.com
    print(f"הזמנה חדשה התקבלה מ: {data['name']}")
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)