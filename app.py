from flask import Flask, request, render_template, redirect, flash
import random

app = Flask(__name__)
app.secret_key = "secret_santa_secret"

participants = []
assignments = {}

@app.route("/", methods=["GET", "POST"])
def index():
    global participants
    if request.method == "POST":
        name = request.form.get("name").strip()
        if name and name not in participants:
            participants.append(name)
        elif name in participants:
            flash("Participant already added!", "error")
    return render_template("index.html", participants=participants)

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
    return render_template("check.html", name=name, assigned=assigned)

if __name__ == "__main__":
    app.run(debug=True)


