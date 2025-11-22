from flask import Flask, request, render_template_string, redirect, flash
import random

app = Flask(__name__)
app.secret_key = "secret_santa_secret"

participants = []
assignments = {}

index_html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Secret Santa Admin</title>
<style>
body { font-family: Arial, sans-serif; margin: 30px; background-color: #f9f9f9; }
h1 { color: #4CAF50; }
input, button { padding: 10px; margin: 5px 0; }
ul { margin-top: 10px; }
li.success { color: green; }
li.error { color: red; }
</style>
</head>
<body>
<h1>Secret Santa - Admin</h1>

<form method="POST">
    <input type="text" name="name" placeholder="Enter participant name">
    <button type="submit">Add Participant</button>
</form>

<h3>Participants:</h3>
<ul>
{% for p in participants %}
<li>{{ p }}</li>
{% endfor %}
</ul>

<form action="/generate" method="POST">
    <button type="submit">Generate Secret Santa</button>
</form>

{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        <ul>
        {% for category, message in messages %}
            <li class="{{ category }}">{{ message }}</li>
        {% endfor %}
        </ul>
    {% endif %}
{% endwith %}
</body>
</html>
"""

check_html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Check Secret Santa</title>
<style>
body { font-family: Arial, sans-serif; margin: 30px; background-color: #f2f2f2; }
h1 { color: #e91e63; }
input, button { padding: 10px; margin: 5px 0; }
li.success { color: green; }
li.error { color: red; }
</style>
</head>
<body>
<h1>Check Your Secret Santa</h1>

<form method="POST">
    <input type="text" name="name" placeholder="Enter your name">
    <button type="submit">See Your Gift</button>
</form>

{% if name %}
<p>Hello {{ name }}! You should gift: <strong>{{ assigned }}</strong></p>
{% endif %}

{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        <ul>
        {% for category, message in messages %}
            <li class="{{ category }}">{{ message }}</li>
        {% endfor %}
        </ul>
    {% endif %}
{% endwith %}

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    global participants
    if request.method == "POST":
        name = request.form.get("name").strip()
        if name and name not in participants:
            participants.append(name)
        elif name in participants:
            flash("Participant already added!", "error")
    return render_template_string(index_html, participants=participants)

@app.route("/generate", methods=["POST"])
def generate():
    global participants, assignments
    if len(participants) < 2:
        flash("Add at least 2 participants before generating!", "error")
        return redirect("/")
    
    shuffled = participants.copy()
    random.shuffle(shuffled)
    for i, giver in enumerate(participants):
        receiver = shuffled[i]
        if giver == receiver:
            shuffled[i], shuffled[(i+1) % len(shuffled)] = shuffled[(i+1) % len(shuffled)], shuffled[i]
            receiver = shuffled[i]
        assignments[giver] = receiver

    flash("Secret Santa assignments generated! Participants can now check their gift.", "success")
    return redirect("/check")

@app.route("/check", methods=["GET", "POST"])
def check():
    name = None
    assigned = None
    if request.method == "POST":
        name_input = request.form.get("name").strip()
        if name_input in assignments:
            name = name_input
            assigned = assignments[name]
        else:
            flash("Name not found. Check spelling!", "error")
    return render_template_string(check_html, name=name, assigned=assigned)

if __name__ == "__main__":
    app.run(debug=True)

