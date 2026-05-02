from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# רשימת מוצרים מורחבת עם קטגוריות
PRODUCTS = [
    {"id": 1, "name": "SMOOTH BLACK OVERSIZE", "price": 189, "image": "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800", "category": "Shirts"},
    {"id": 2, "name": "CARGO TECH PANTS", "price": 349, "image": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=800", "category": "Pants"},
    {"id": 3, "name": "URBAN LEATHER JACKET", "price": 599, "image": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=800", "category": "Jackets"},
    {"id": 4, "name": "SMOOTH SIGNATURE HOODIE", "price": 280, "image": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=800", "category": "Hoodies"},
    {"id": 5, "name": "WHITE STREET TEE", "price": 159, "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=800", "category": "Shirts"},
    {"id": 6, "name": "SMOOTH BEANIE BLACK", "price": 89, "image": "https://images.unsplash.com/photo-1576871337622-98d48d365da5?w=800", "category": "Accessories"}
]

@app.route('/')
def home():
    return render_template('index.html', products=PRODUCTS)

@app.route('/checkout', methods=['POST'])
def checkout():
    data = request.json
    # כאן הקוד שולח את הפרטים ל-lielregev1110@gmail.com
    print(f"--- הזמנה חדשה ב-SMOOTH ---")
    print(f"לקוח: {data['name']}, אימייל: {data['email']}")
    print(f"כתובת: {data['address']}, {data['city']}")
    print(f"מוצרים: {data['items']}")
    print(f"סה''כ לתשלום: {data['total']} ₪")
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)