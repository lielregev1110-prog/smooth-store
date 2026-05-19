from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# נתוני מועדוני IFL
CLUBS_DATA = [
    {"rank": 1, "logo": "🏆", "name": "Tel Aviv Elite", "played": 18, "wins": 14, "draws": 3, "losses": 1, "gd": "+32", "points": 45},
    {"rank": 2, "logo": "⚡", "name": "Haifa Predators", "played": 18, "wins": 13, "draws": 2, "losses": 3, "gd": "+21", "points": 41},
    {"rank": 3, "logo": "🛡️", "name": "Jerusalem Knights", "played": 18, "wins": 11, "draws": 5, "losses": 2, "gd": "+15", "points": 38},
    {"rank": 4, "logo": "🐍", "name": "Beer Sheva Vipers", "played": 18, "wins": 10, "draws": 2, "losses": 8, "gd": "+2", "points": 32}
]

@app.route('/')
def index():
    return render_template('index.html', clubs=CLUBS_DATA)

if __name__ == '__main__':
    app.run(debug=True)