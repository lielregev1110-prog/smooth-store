import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import random
from flask import Flask, render_template, jsonify, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "ifl_zone_ultra_secret_2026_premium"

# קוד פאנל ניהול ראשי של ליאל
ADMIN_CODE = "IFL2024"

# הגדרות שרת מייל (עבור עדכון חוקים) - שים כאן את הסיסמה מצילום המסך שלך!
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your-email@gmail.com"
SENDER_PASSWORD = "your-app-password-from-screenshot" # ה-App Password שאתה מייצר בצילום מסך

# בסיס נתונים בזיכרון השרת (הכל נקי, שחקנים ירשמו מחדש)
USERS = {}
CLUBS = {
    "Tel Aviv Elite": {"logo": "🏆", "points": 0, "played": 0, "wins": 0, "draws": 0, "losses": 0, "manager": None},
    "Haifa Predators": {"logo": "⚡", "points": 0, "played": 0, "wins": 0, "draws": 0, "losses": 0, "manager": None},
    "Jerusalem Knights": {"logo": "🛡️", "points": 0, "played": 0, "wins": 0, "draws": 0, "losses": 0, "manager": None},
    "Beer Sheva Vipers": {"logo": "🐍", "points": 0, "played": 0, "wins": 0, "draws": 0, "losses": 0, "manager": None}
}

FIXTURES = []
TRANSFERS = [] # בקשות העברה פעילות
BANS = {} # {"username": datetime_until}
NOTIFICATIONS = {} # {"username": [{"text": "...", "type": "..."}]}

LEAGUE_RULES = {
    "content": "<h1>חוקי ליגת IFL הרשמית</h1><p>נא לשמור על משחק הוגן ותרבות דיבור.</p>",
    "updated_by": "מערכת",
    "updated_at": "2026-05-19",
    "history": []
}

def add_notification(username, text):
    if username not in NOTIFICATIONS:
        NOTIFICATIONS[username] = []
    NOTIFICATIONS[username].append({"text": text, "time": datetime.now().strftime("%H:%M")})

def send_bulk_email(subject, html_content):
    try:
        msg = MIMEText(html_content, "html", "utf-8")
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        # שליחה לכל מי שיש לו מייל רשום (בדוגמה זו נדגים את החיבור לשרת)
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        # בלולאה אמיתית נאסוף את המיילים של כל המשתמשים הרשומים
        server.quit()
    except Exception as e:
        print(f"Email send error (Configure SMTP settings to activate): {e}")

# הגנת באנים עם טיימר בלייב
@app.before_request
def check_player_ban():
    if 'user' in session:
        user = session['user']
        if user in BANS:
            remaining = BANS[user] - datetime.now()
            if remaining.total_seconds() > 0:
                seconds = int(remaining.total_seconds())
                return f"""
                <body style="background:#030712; color:white; font-family:sans-serif; text-align:center; padding-top:120px; dir:rtl;">
                    <div style="max-w:500px; margin:0 auto; background:#0f172a; padding:40px; border-radius:24px; border:1px solid #ef4444; box-shadow: 0 0 30px rgba(239,68,68,0.2);">
                        <h1 style="color:#ef4444; font-size:42px; margin-bottom:10px;">🚫 נחסמת מהאתר!</h1>
                        <p style="font-size:18px; color:#94a3b8;">הנהלת הליגה השעתה אותך זמנית מהמערכת.</p>
                        <div id="countdown" style="font-size:72px; font-weight:bold; color:#f59e0b; margin:30px 0; font-family:monospace;">{seconds}</div>
                        <p style="color:#64748b; text-align:center; font-size:14px;">האתר יתרענן אוטומטית כשתסתיים החסימה.</p>
                    </div>
                    <script>
                        let timeLeft = {seconds};
                        const interval = setInterval(() => {{
                            timeLeft--;
                            document.getElementById('countdown').innerText = timeLeft;
                            if(timeLeft <= 0) {{ clearInterval(interval); location.reload(); }}
                        }}, 1000);
                    </script>
                </body>
                """
            else:
                del BANS[user]

@app.route('/')
def index():
    user_data = USERS.get(session.get('user'))
    return render_template('index.html', clubs=CLUBS, users=USERS, fixtures=FIXTURES, rules=LEAGUE_RULES, current_user=user_data, notifications=NOTIFICATIONS.get(session.get('user'), []), transfers=TRANSFERS)

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    club = request.form.get('club')
    if username and username not in USERS:
        USERS[username] = {
            "username": username,
            "password": request.form.get('password'),
            "ea_id": request.form.get('ea_id'),
            "club": club,
            "pos": request.form.get('pos'),
            "role": "player", # ברירת מחדל שחקן רגיל
            "rating": 85,
            "score": 5.0, # ציון
            "goals": 0, "assists": 0, "motm": 0,
            "performance_history": [85, 85, 85]
        }
        session['user'] = username
    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    u, p = request.form.get('username'), request.form.get('password')
    if u in USERS and USERS[u]['password'] == p:
        session['user'] = u
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

# פאנל ניהול בלעדי של ליאל (קוד IFL2024)
@app.route('/admin/action', methods=['POST'])
def admin_action():
    data = request.json
    if data.get('code') != ADMIN_CODE:
        return jsonify({"success": False, "error": "קוד מנהל מערכת שגוי!"})
    
    action = data.get('action')
    target = data.get('target')
    
    if action == "ban":
        mins = int(data.get('minutes', 1))
        BANS[target] = datetime.now() + timedelta(minutes=mins)
        return jsonify({"success": True})
        
    elif action == "set_manager":
        club = data.get('club')
        if target in USERS and club in CLUBS:
            USERS[target]['role'] = "manager"
            USERS[target]['club'] = club
            CLUBS[club]['manager'] = target
            return jsonify({"success": True})
            
    elif action == "update_stats":
        if target in USERS:
            USERS[target]['rating'] = int(data.get('rating', 85))
            USERS[target]['score'] = float(data.get('score', 5.0))
            USERS[target]['performance_history'].append(int(data.get('rating', 85)))
            return jsonify({"success": True})
            
    elif action == "update_points":
        club = data.get('club')
        if club in CLUBS:
            CLUBS[club]['points'] = int(data.get('points', 0))
            return jsonify({"success": True})

    elif action == "generate_fixtures":
        # מחולל מחזורים אוטומטי חכם
        global FIXTURES
        FIXTURES = []
        club_list = list(CLUBS.keys())
        random.shuffle(club_list)
        # יצירת מחזור משחקים ראשון אוטומטי
        FIXTURES.append({"id": 1, "home": club_list[0], "away": club_list[1], "status": "קרוב", "score": "", "home_lineup": [], "away_lineup": [], "events": {}})
        FIXTURES.append({"id": 2, "home": club_list[2], "away": club_list[3], "status": "קרוב", "score": "", "home_lineup": [], "away_lineup": [], "events": {}})
        return jsonify({"success": True})

    elif action == "update_rules":
        global LEAGUE_RULES
        old_content = LEAGUE_RULES['content']
        LEAGUE_RULES['history'].append({
            "content": old_content, "updated_by": "ליאל", "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        LEAGUE_RULES['content'] = data.get('content')
        LEAGUE_RULES['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M")
        send_bulk_email("IFL ZONE - חוקי הליגה עודכנו!", f"<h2>שלום שחקן ליגה,</h2><p>חוקי הליגה עודכנו על ידי ההנהלה. אנא היכנס לאתר לבדוק.</p>")
        return jsonify({"success": True})

    return jsonify({"success": False})

# פעולות מנהלי קבוצות (ניהול שוק העברות והרכבים)
@app.route('/manager/action', methods=['POST'])
def manager_action():
    current_user = USERS.get(session.get('user'))
    if not current_user or current_user['role'] != "manager":
        return jsonify({"success": False, "error": "אינך מנהל קבוצה מורשה!"})
        
    data = request.json
    action = data.get('action')
    my_club = current_user['club']
    
    if action == "send_transfer_request":
        target = data.get('target')
        if target in USERS:
            TRANSFERS.append({"id": len(TRANSFERS)+1, "from_club": my_club, "player": target, "status": "ממתין"})
            add_notification(target, f"קיבלת הצעת העברה רשמית ממועדון {my_club}!")
            return jsonify({"success": True})
            
    elif action == "submit_lineup":
        fixture_id = int(data.get('fixture_id'))
        lineup_str = data.get('lineup_text', "")
        players = [p.strip() for p in lineup_str.split(',') if p.strip()]
        for f in FIXTURES:
            if f['id'] == fixture_id:
                if f['home'] == my_club: f['home_lineup'] = players
                if f['away'] == my_club: f['away_lineup'] = players
                return jsonify({"success": True})
                
    elif action == "report_match":
        fixture_id = int(data.get('fixture_id'))
        score = data.get('score') # "3 - 1"
        scorer = data.get('scorer')
        assistant = data.get('assistant')
        motm = data.get('motm')
        
        for f in FIXTURES:
            if f['id'] == fixture_id:
                f['score'] = score
                f['status'] = "הסתיים"
                f['events'] = {"scorer": scorer, "assistant": assistant, "motm": motm}
                # עדכון נתוני השחקנים ישירות בשרת
                if scorer in USERS: USERS[scorer]['goals'] += 1
                if assistant in USERS: USERS[assistant]['assists'] += 1
                if motm in USERS: USERS[motm]['motm'] += 1
                return jsonify({"success": True})

    return jsonify({"success": False})

@app.route('/player/accept_transfer', methods=['POST'])
def accept_transfer():
    user = session.get('user')
    transfer_id = int(request.json.get('id'))
    for t in TRANSFERS:
        if t['id'] == transfer_id and t['player'] == user:
            t['status'] = "אושר"
            USERS[user]['club'] = t['from_club']
            return jsonify({"success": True})
    return jsonify({"success": False})

if __name__ == '__main__':
    app.run(debug=True)