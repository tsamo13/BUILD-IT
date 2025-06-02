from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/post_project", methods=["POST"])
def post_project():
    data = request.json
    project = {
        "id": len(projects) + 1,
        "title": data["title"],
        "description": data["description"],
        "owner": data["owner"],
        "assigned_to": None
    }
    projects.append(project)
    return jsonify({"status": "created", "project": project}), 201

@app.route("/projects", methods=["GET"])
def list_projects():
    return jsonify(projects)

@app.route("/apply/<int:project_id>", methods=["POST"])
def apply_to_project(project_id):
    company = request.json.get("company")
    if project_id > len(projects):
        return jsonify({"error": "Invalid project ID"}), 404
    applications.setdefault(project_id, []).append(company)
    return jsonify({"status": "application received", "company": company})

@app.route("/select/<int:project_id>/<company>", methods=["POST"])
def assign_project(project_id, company):
    if project_id > len(projects):
        return jsonify({"error": "Invalid project ID"}), 404
    projects[project_id - 1]["assigned_to"] = company
    return jsonify({"status": "project assigned", "to": company})

if __name__ == "__main__":
    app.run(debug=True)
