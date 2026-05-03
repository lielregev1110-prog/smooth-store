from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = "smooth_elite_exclusive_2026"

# רשימת מוצרים עם דירוגים וקטגוריות
PRODUCTS = [
    {"id": 1, "name": "SMOOTH BLACK OVERSIZE", "price": 189, "image": "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800", "rating": 5, "reviews": 124},
    {"id": 2, "name": "CARGO TECH PANTS", "price": 349, "image": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=800", "rating": 4, "reviews": 89},
    {"id": 3, "name": "URBAN LEATHER JACKET", "price": 599, "image": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=800", "rating": 5, "reviews": 45},
    {"id": 4, "name": "SIGNATURE HOODIE", "price": 280, "image": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=800", "rating": 5, "reviews": 210}
]

def send_order_email(data):
    sender_email = "your-email@gmail.com" 
    sender_password = "your-app-password" 
    receiver_email = "lielregev1110@gmail.com"

    msg = MIMEMultipart()
    msg['Subject'] = f"הזמנה חדשה ב-SMOOTH מ-{data['name']}"
    
    body = f"""
    התקבלה הזמנה חדשה!
    שם הלקוח: {data['name']}
    אימייל: {data['email']}
    עיר: {data['city']}
    כתובת: {data['address']}
    
    פריטים: {data['items']}
    סה"כ לתשלום: {data['total']} ₪
    """
    msg.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True
    except: return False

@app.route('/')
def home():
    user = session.get('user')
    return render_template('index.html', products=PRODUCTS, user=user)

@app.route('/login_google')
def login_google():
    session['user'] = {"name": "אורח VIP", "email": "customer@example.com"}
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/checkout', methods=['POST'])
def checkout():
    data = request.json
    if send_order_email(data):
        return jsonify({"status": "success"})
    return jsonify({"status": "error"})

if __name__ == '__main__':
    app.run(debug=True)