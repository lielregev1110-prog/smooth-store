from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = "smooth_ultimate_elite_2026"

# הגדרות שליחת מייל - מעודכן עם הקוד הסודי שלך
ADMIN_EMAIL = "lielregev1110@gmail.com"
SENDER_EMAIL = "lielregev1110@gmail.com" 
SENDER_PASS = "snne swpb bodv zzjm" # הקוד שהוצאת מגוגל

PRODUCTS = [
    {"id": 1, "name": "BLACK OVERSIZE ELITE", "price": 189, "stock": 15, "img": "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800"},
    {"id": 2, "name": "VOID CARGO TECH", "price": 349, "stock": 8, "img": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=800"},
    {"id": 3, "name": "PREMIUM LEATHER", "price": 599, "stock": 5, "img": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=800"}
]

COUPONS = {"SMOOTH20": 0.20, "ELITE10": 0.10}

@app.route('/')
def index():
    return render_template('index.html', products=PRODUCTS)

@app.route('/apply_coupon', methods=['POST'])
def apply_coupon():
    code = request.json.get('code', '').upper()
    discount = COUPONS.get(code, 0)
    return jsonify({"success": discount > 0, "discount": discount})

@app.route('/complete_order', methods=['POST'])
def complete_order():
    data = request.json
    msg = MIMEMultipart()
    msg['Subject'] = f"הזמנה חדשה ב-SMOOTH: {data['name']}"
    msg['From'] = SENDER_EMAIL
    msg['To'] = ADMIN_EMAIL
    
    body = f"הזמנה חדשה הגיעה!\n\nשם הלקוח: {data['name']}\nכתובת: {data['address']}\nפריטים: {data['items']}\nסה\"כ לתשלום: {data['total']}"
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        # התחברות לשרת גוגל ושליחה
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASS)
        server.send_message(msg)
        server.quit()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)