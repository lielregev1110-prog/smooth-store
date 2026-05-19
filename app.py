from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# נתוני דמי של קבוצות בליגת IFL
MOCK_CLUBS = [
    {"name": "Tel Aviv Elite", "rank": 1, "points": 45, "form": ["W", "W", "W", "D", "W"], "streamers": 3, "avg_score": 8.2},
    {"name": "Haifa Predators", "rank": 2, "points": 41, "form": ["W", "L", "W", "W", "W"], "streamers": 1, "avg_score": 7.9},
    {"name": "Jerusalem Knights", "rank": 3, "points": 38, "form": ["D", "W", "L", "W", "L"], "streamers": 4, "avg_score": 7.6},
    {"name": "Beer Sheva Vipers", "rank": 4, "points": 32, "form": ["L", "W", "W", "L", "D"], "streamers": 0, "avg_score": 7.1}
]

# שחקנים חופשיים שמחפשים קבוצה בליגה (Recruitment Center)
MOCK_FREE_AGENTS = [
    {"name": "Roy_ST_99", "position": "ST", "rating": 89, "value": "₪12.5M", "discord": "RoyST#1234"},
    {"name": "Ben_CDM_Elite", "position": "CDM", "rating": 87, "value": "₪9.0M", "discord": "BenCDM#5678"},
    {"name": "Gal_GK_Wall", "position": "GK", "rating": 91, "value": "₪15.0M", "discord": "GalGK#9999"}
]

@app.route('/')
def home():
    return render_template('index.html', clubs=MOCK_CLUBS, free_agents=MOCK_FREE_AGENTS)

@app.route('/api/clubs')
def get_clubs():
    return jsonify(MOCK_CLUBS)

@app.route('/api/recruit', methods=['POST'])
def register_free_agent():
    data = request.json
    # כאן בעתיד נשמור לבסיס הנתונים
    new_agent = {
        "name": data.get("name"),
        "position": data.get("position"),
        "rating": int(data.get("rating", 80)),
        "value": f"₪{int(data.get('rating', 80)) * 0.15:.1f}M",
        "discord": data.get("discord")
    }
    MOCK_FREE_AGENTS.append(new_agent)
    return jsonify({"success": True, "agent": new_agent})

if __name__ == '__main__':
    app.run(debug=True)