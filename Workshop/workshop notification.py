# ειδοποιήσεις συνεργείων
from flask import Flask, request, jsonify

app = Flask(__name__)

# Εικονική βάση ειδοποιήσεων
notifications_db = {
    "team1": [
        {
            "id": 1,
            "project": "Επέκταση Οροφής",
            "message": "Νέο αίτημα συνεργασίας από την κατασκευαστική.",
            "status": "ΝΕΟ"
        }
    ]
}

# 🔹 Εμφάνιση ειδοποιήσεων για συνεργείο
@app.route("/notifications/<team_id>", methods=["GET"])
def get_notifications(team_id):
    notifications = notifications_db.get(team_id, [])
    return jsonify(notifications)

# 🔹 Προσθήκη νέας ειδοποίησης
@app.route("/notifications/<team_id>/add", methods=["POST"])
def add_notification(team_id):
    data = request.get_json()

    if not data or "project" not in data or "message" not in data:
        return jsonify({"error": "Missing 'project' or 'message' in request"}), 400

    new_note = {
        "id": len(notifications_db.get(team_id, [])) + 1,
        "project": data["project"],
        "message": data["message"],
        "status": "ΝΕΟ"
    }
    notifications_db.setdefault(team_id, []).append(new_note)
    return jsonify({"status": "success", "notification": new_note}), 201

# 🔹 Ενημέρωση κατάστασης ειδοποίησης (π.χ. όταν τη δει το συνεργείο)
@app.route("/notifications/<team_id>/<int:note_id>/update", methods=["POST"])
def update_notification(team_id, note_id):
    team_notes = notifications_db.get(team_id, [])
    for note in team_notes:
        if note["id"] == note_id:
            note["status"] = "ΔΙΑΒΑΣΤΗΚΕ"
            return jsonify({"status": "updated", "notification": note})
    return jsonify({"status": "not found"}), 404
from flask import render_template  # το προσθέτεις δίπλα στα imports

@app.route("/notifications/<team_id>/view", methods=["GET"])
def view_notifications(team_id):
    notifications = notifications_db.get(team_id, [])
    return render_template("workshop_notifications.html", notifications=notifications)

if __name__ == "__main__":
    app.run(debug=True)
