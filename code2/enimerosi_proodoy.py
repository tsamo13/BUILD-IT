from flask import Flask, request, jsonify, render_template, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Εικονικά δεδομένα έργων (για συνεργείο)
projects_db = {
    "team1": [
        {"id": 1, "title": "Ανακαίνιση Κτιρίου Α"},
        {"id": 2, "title": "Τοποθέτηση Ηλιακών Πάνελ"},
    ]
}

MAX_MESSAGE_LENGTH = 300  # Όριο χαρακτήρων

# 🔹 Επιστροφή ενεργών έργων για συνεργείο
@app.route("/projects/<team_id>", methods=["GET"])
def get_projects(team_id):
    projects = projects_db.get(team_id, [])
    return jsonify(projects)

# 🔹 Υποβολή προόδου έργου
@app.route("/submit_progress", methods=["POST"])
def submit_progress():
    data = request.get_json()

    if not data:
        return jsonify({"status": "error", "message": "Missing or invalid JSON data"}), 400

    project_id = data.get("project_id")
    message = data.get("message")
    confirm = data.get("confirm")

    if not message or len(message.strip()) == 0:
        return jsonify({"status": "error", "message": "Το μήνυμα δεν μπορεί να είναι κενό."}), 400
    if len(message) > MAX_MESSAGE_LENGTH:
        return jsonify({"status": "error", "message": "Το μήνυμα ξεπερνά το επιτρεπτό όριο χαρακτήρων."}), 400

    if not confirm:
        return jsonify({
            "status": "preview",
            "preview": f"Προεπισκόπηση για έργο #{project_id}: {message}"
        })

    return jsonify({
        "status": "success",
        "message": "Η ενημέρωση αποστάλθηκε επιτυχώς στην κατασκευαστική."
    })

# 🔹 Αναφορά προβλήματος (με HTML φόρμα)
@app.route("/report_issue", methods=["GET", "POST"])
def report_issue():
    if request.method == "POST":
        new_date = request.form.get("new_date")
        issue_type = request.form.get("issue_type")
        issue_info = request.form.get("issue_info")

        # Εδώ γίνεται η αποθήκευση ή αποστολή (π.χ. σε βάση ή email)
        print(f"[REPORT] Νέα Ημ/νία: {new_date}, Τύπος: {issue_type}, Πληροφορίες: {issue_info}")

        return redirect(url_for("issue_submitted"))

    return render_template("report_issue.html")

# 🔹 Επιβεβαίωση μετά την υποβολή αναφοράς
@app.route("/issue_submitted")
def issue_submitted():
    return "Η αναφορά προβλήματος υποβλήθηκε επιτυχώς!"

# 🔹 Προβολή έργων που έχει δημοσιεύσει ο ιδιώτης
@app.route("/citizen_projects")
def citizen_projects():
    pending = [
        {"title": "Project1"},
        {"title": "Project2"},
        {"title": "Project3"}
    ]
    active = [
        {"title": "Project4"},
        {"title": "Project5"},
        {"title": "Project6"}
    ]
    completed = [
        {"title": "Project7"},
        {"title": "Project8"},
        {"title": "Project9"}
    ]
    return render_template("citizen_projects.html",
                           pending_projects=pending,
                           active_projects=active,
                           completed_projects=completed)
@app.route("/workshop_projects")
def workshop_projects():
    projects = [
        {"id": 1, "title": "Project1"},
        {"id": 2, "title": "Project2"},
        {"id": 3, "title": "Project3"},
        {"id": 4, "title": "Project4"},
        {"id": 5, "title": "Project5"},
        {"id": 6, "title": "Project6"},
    ]
    return render_template("workshop_projects.html", projects=projects)

if __name__ == "__main__":
    app.run(debug=True)
