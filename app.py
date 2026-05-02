from flask import Flask, render_template, request, jsonify
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# רשימת מוצרים משודרגת
PRODUCTS = [
    {"id": 1, "name": "SMOOTH BLACK OVERSIZE", "price": 189, "image": "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800"},
    {"id": 2, "name": "CARGO TECH PANTS", "price": 349, "image": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=800"},
    {"id": 3, "name": "URBAN LEATHER JACKET", "price": 599, "image": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=800"},
    {"id": 4, "name": "SMOOTH SIGNATURE HOODIE", "price": 280, "image": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=800"}
]

@app.route('/')
def home():
    return render_template('index.html', products=PRODUCTS)

@app.route('/checkout', methods=['POST'])
def checkout():
    data = request.json
    
    # פרטי ההזמנה מהלקוח
    customer_name = data.get('name')
    email = data.get('email')
    address = data.get('address')
    city = data.get('city')
    # בשרת אמיתי - כאן מתבצע החיבור לסליקת האשראי
    
    # בניית ההודעה לאימייל שלך
    msg_content = f"""
    הזמנה חדשה מאתר SMOOTH!
    שם הלקוח: {customer_name}
    אימייל: {email}
    עיר: {city}
    כתובת: {address}
    פריטים: {data.get('items')}
    """
    
    try:
        # הגדרות שליחת אימייל (SMTP)
        sender = "your-system-email@gmail.com" # אימייל ממנו נשלחת ההודעה
        receiver = "lielregev1110@gmail.com"
        msg = MIMEText(msg_content)
        msg['Subject'] = f"הזמנה חדשה מ-{customer_name}"
        msg['From'] = sender
        msg['To'] = receiver

        # חיבור לשרת גוגל (דורש סיסמת אפליקציה)
        # with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        #     server.login(sender, "YOUR_APP_PASSWORD")
        #     server.sendmail(sender, receiver, msg.as_string())
        
        print(f"Email sent to {receiver}!") # בדיקה בטרמינל
        return jsonify({"status": "success", "message": "ההזמנה התקבלה! אישור נשלח למנהל."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)