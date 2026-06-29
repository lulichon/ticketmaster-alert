from flask import Flask, render_template_string
import json
from datetime import datetime

app = Flask(__name__)

HTML = """
<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Ticketmaster Alert</title>
  <meta http-equiv="refresh" content="30">
  <style>
    body { font-family: Arial; background:#111; color:#eee; padding:30px; }
    .card { background:#1e1e1e; padding:20px; border-radius:14px; margin-bottom:15px; }
    .ok { color:#4ade80; }
    .ko { color:#f87171; }
    .wait { color:#facc15; }
    a { color:#93c5fd; }
  </style>
</head>
<body>
  <h1>🎟 Ticketmaster Alert</h1>

  {% for name, item in state.items() %}
    <div class="card">
      <h2>{{ name }}</h2>
      <p>Statut :
        {% if item.available %}
          <span class="ok">Billets détectés</span>
        {% elif item.status == "queue" %}
          <span class="wait">File d’attente Ticketmaster</span>
        {% else %}
          <span class="ko">Indisponible</span>
        {% endif %}
      </p>
      <p>Dernière vérification : <strong>{{ item.last_checked }}</strong></p>
      <p><a href="{{ item.url }}" target="_blank">Ouvrir Ticketmaster</a></p>
    </div>
  {% endfor %}
</body>
</html>
"""

@app.route("/")
def home():
    try:
        with open("state.json", "r") as f:
            state = json.load(f)
    except:
        state = {}

    return render_template_string(HTML, state=state)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
