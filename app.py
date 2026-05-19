from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "ifl_ultimate_secret_key_2026"

# פאנל ניהול קוד סודי
ADMIN_CODE = "IFL2024"

# בסיס נתונים זמני בזיכרון השרת
USERS = {
    "liel": {"username": "liel", "password": "123", "ea_id": "LielRegev10", "role": "player", "club": "Tel Aviv Elite", "rating": 92, "pos": "ST"},
    "manager1": {"username": "manager1", "password": "123", "ea_id": "ManagerX", "role": "manager", "club": "Tel Aviv Elite", "rating": 85, "pos": "CM"}
}

CLUBS = {
    "Tel Aviv Elite": {"manager": "manager1", "players": ["liel", "manager1"], "lineup": ["liel", "manager1"], "logo": "🏆", "points": 45},
    "Haifa Predators": {"manager": None, "players": [], "lineup": [], "logo": "⚡", "points": 41},
    "Jerusalem Knights": {"manager": None, "players": [], "lineup": [], "logo": "🛡️", "points": 38}
}

BANS = {} # מבנה: {"username": datetime_until}
TRANSFERS = [] # רשימת הצעות העברה
NOTIFICATIONS = {} # התראות לפי שם משתמש: {"username": ["msg1", "msg2"]}

# בדיקת באנים אוטומטית לפני כל בקשה לאתר
@app.before_request
def check_ban():
    if 'user' in session:
        username = session['user']
        if username in BANS:
            remaining = BANS[username] - datetime.now()
            if remaining.total_seconds() > 0:
                # חישוב הזמן שנשאר בפורמט קריא
                hours, remainder = divmod(int(remaining.total_seconds()), 3600)
                minutes, seconds = divmod(remainder, 60)
                return f"""
                <body style="background:#050811; color:white; font-family:sans-serif; text-align:center; padding-top:100px; dir:rtl;">
                    <h1 style="color:#ef4444; font-size:40px;">קיבלת באן ממערכת IFL!</h1>
                    <p style="font-size:20px; color:#9ca3af;">תוכל להיכנס חזרה לאתר בעוד:</p>
                    <div style="font-size:48px; font-weight:bold; color:#f59e0b; margin:20px 0;">
                        {hours:02d}:{minutes:02d}:{seconds:02d}
                    </div>
                    <p style="color:#6b7280; font-size:14px;">נא לשמור על חוקי הליגה בפעם הבאה.</p>
                    <script>setTimeout(function(){{ location.reload(); }}, 1000);</script>
                </body>
                """
            else:
                del BANS[username] # הבאן נגמר

@app.route('/')
def home():
    current_user = USERS.get(session.get('user'))
    user_notifications = NOTIFICATIONS.get(session.get('user'), [])
    return render_template('index.html', clubs=CLUBS, users=USERS, current_user=current_user, notifications=user_notifications)

# התחברות ורישום
@app.route('/login', methods=['POST'])
def login():
    data = request.form
    username = data.get('username')
    password = data.get('password')
    if username in USERS and USERS[username]['password'] == password:
        session['user'] = username
    return redirect(url_for('home'))

@app.route('/register', methods=['POST'])
def register():
    data = request.form
    username = data.get('username')
    if username and username not in USERS:
        USERS[username] = {
            "username": username,
            "password": data.get('password'),
            "ea_id": data.get('ea_id'),
            "role": "player",
            "club": None,
            "rating": 85,
            "pos": data.get('pos', 'ST')
        }
        session['user'] = username
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

# פאנל ניהול ראשי (IFL2024)
@app.route('/admin/action', methods=['POST'])
def admin_action():
    data = request.json
    if data.get('code') != ADMIN_CODE:
        return jsonify({"success": False, "error": "קוד ניהול שגוי!"})
    
    action = data.get('action')
    target_user = data.get('target_user')
    
    if action == "assign_manager":
        club_name = data.get('club')
        if target_user in USERS and club_name in CLUBS:
            USERS[target_user]['role'] = "manager"
            USERS[target_user]['club'] = club_name
            CLUBS[club_name]['manager'] = target_user
            if target_user not in CLUBS[club_name]['players']:
                CLUBS[club_name]['players'].append(target_user)
            return jsonify({"success": True})
            
    elif action == "ban":
        minutes = int(data.get('minutes', 5))
        BANS[target_user] = datetime.now() + timedelta(minutes=minutes)
        return jsonify({"success": True})
        
    return jsonify({"success": False})

# פעולות מנהל קבוצה (העברות והרכבים)
@app.route('/manager/action', methods=['POST'])
def manager_action():
    current_username = session.get('user')
    if not current_username or USERS[current_username]['role'] != "manager":
        return jsonify({"success": False, "error": "אינך מנהל קבוצה!"})
        
    data = request.json
    action = data.get('action')
    club_name = USERS[current_username]['club']
    
    if action == "send_transfer":
        target = data.get('target_user')
        if target in USERS:
            if target not in NOTIFICATIONS: NOTIFICATIONS[target] = []
            NOTIFICATIONS[target].append(f"קיבלת הצעה להצטרף למועדון {club_name}!")
            return jsonify({"success": True})
            
    elif action == "save_lineup":
        players_list = data.get('lineup', [])
        CLUBS[club_name]['lineup'] = players_list
        return jsonify({"success": True})
        
    return jsonify({"success": False})

if __name__ == '__main__':
    app.run(debug=True)