from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = "smooth_ultimate_elite_2026"

# הגדרות שליחת מייל - חשוב להזין פרטים אמיתיים
ADMIN_EMAIL = "lielregev1110@gmail.com"
SENDER_EMAIL = "your-gmail@gmail.com"  # האימייל שממנו נשלחת ההודעה
SENDER_PASS = "your-app-password"      # סיסמת אפליקציה מגוגל

PRODUCTS = [
    {"id": 1, "name": "BLACK OVERSIZE ELITE", "price": 189, "stock": 15, "img": "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800"},
    {"id": 2, "name": "VOID CARGO TECH", "price": 349, "stock": 8, "img": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=800"},
    {"id": 3, "name": "PREMIUM LEATHER", "price": 599, "stock": 5, "img": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=800"}
]

COUPONS = {"SMOOTH20": 0.20, "VIP100": 100} # אחוזים או סכום קבוע

@app.route('/')
def index():
    user = session.get('user', None)
    return render_template('index.html', products=PRODUCTS, user=user)

@app.route('/apply_coupon', methods=['POST'])
def apply_coupon():
    code = request.json.get('code', '').upper()
    discount = COUPONS.get(code, 0)
    return jsonify({"success": discount > 0, "discount": discount})

@app.route('/complete_order', methods=['POST'])
def complete_order():
    data = request.json
    # לוגיקת שליחת המייל
    msg = MIMEMultipart()
    msg['Subject'] = f"הזמנה חדשה ב-SMOOTH: {data['name']}"
    body = f"שם: {data['name']}\nכתובת: {data['address']}\nפריטים: {data['items']}\nסה\"כ: {data['total']} ש\"ח"
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASS)
        server.send_message(msg)
        server.quit()
        return jsonify({"success": True})
    except:
        return jsonify({"success": False}), 500

@app.route('/login_google')
def login_google():
    session['user'] = {"name": "VIP Guest", "points": 500}
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)