from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from flask import session
import psycopg2
import psycopg2.extras


app = Flask(__name__)
app.secret_key = 'some_secret_key'  # για flash

#συνδεση στην βαση
def get_db_connection():
    return mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='crews',
        port=3306
        
    )

@app.route('/')
def home():
    return render_template('home.html')


#εδω ξεκιναει το search------------------------

# Search form με επιλογές από βάση
@app.route('/search_form', methods=['GET'])
def search_form():
    conn = get_db_connection()
    cur = conn.cursor()

    query = "SELECT DISTINCT workshop_type FROM Workshop"
    cur.execute(query)
    workshop_types = cur.fetchall()
    conn.close()

    return render_template('search.html', workshops=None, workshop_types=workshop_types)

#αφου πατησω search εμφανιση διαθεσιμων συνεργειων
@app.route('/search', methods=['POST'])
def search():
    location = request.form['location']
    workshop_type = request.form['type']

    conn = get_db_connection()
    cur = conn.cursor()

    query = """
        SELECT w.user_id, u.name, w.description, w.location
        FROM Workshop w
        JOIN my_user u ON w.user_id = u.id
        WHERE LOWER(w.workshop_type) = LOWER(%s)
        AND LOWER(w.location) = LOWER(%s)
        AND w.available = TRUE
    """
    cur.execute(query, (workshop_type, location))
    results = cur.fetchall()
    conn.close()

    return render_template('results.html', workshops=results)

#αφου πατησω choose workshop εμφανιση στοιχειων του
@app.route('/choose', methods=['POST'])
def choose():
    workshop_id = request.form['workshop_id']

    conn = get_db_connection()
    cur = conn.cursor()

    query = """
        SELECT w.description, w.workshop_type, w.location, u.name
        FROM Workshop w
        JOIN my_user u ON w.user_id = u.id
        WHERE w.user_id = %s
    """
    cur.execute(query, (workshop_id,))
    workshop = cur.fetchone()
    conn.close()

    if workshop:
        return render_template('workshop_details.html', workshop=workshop)
    else:
        return "No workshops found.", 404

#αφου πατησω apply αποστολη request απο κατασκευαστικη σε συνεργειο
@app.route('/apply', methods=['POST'])
def apply():
    construction_name = request.form.get('name')
    construction_id = request.form.get('construction_id')  # Αυτό το παίρνεις από το form
    email = request.form.get('email')
    project_title = request.form.get('project_title')

    # Δημιουργία σύνδεσης
    conn = get_db_connection()
    cur = conn.cursor()

    # Εισαγωγή στο request table
    cur.execute("""
        INSERT INTO Request (construction_id, project_title, email, text)
        VALUES (%s, %s, %s, %s)
    """, (
        construction_id,
        project_title,
        email,
        f"Request from {construction_name} to collab for the project: '{project_title}'"
    ))

    conn.commit()
    conn.close()

    return f"Your request for the prject: '{project_title}' was succesfully submitted!"


#εδω τελειωνει το search------------------------------------




#εδω ξεκινα το pending projects----------------------------------
@app.route('/Pending', methods=['GET','POST'])
def Pending():

    conn = get_db_connection()
    cur = conn.cursor()

    query = """
        SELECT p.name, p.information, p.construction_type, p.start_date, p.location
        FROM Project p
        WHERE p.status = 'pending'
    """
    cur.execute(query)
    Pending = cur.fetchall()
    conn.close()

    return render_template('Pending.html', Pending=Pending)


@app.route('/submit_cost', methods=['POST'])
def submit_cost():
    estimated_cost = request.form['estimated_cost']
    project_name = request.form['project_name']  # Αυτό πρέπει να το περάσεις στο hidden input
    construction_id = session.get('user_id')  # Logged in user

    conn = get_db_connection()
    cur = conn.cursor()

    # Πάρε citizen_id από το project
    cur.execute("SELECT citizen_id FROM Project WHERE name = %s", (project_name,))
    result = cur.fetchone()
    if result:
        citizen_id = result[0]

        # Κάνε insert στο Appointment
        insert_query = """
            INSERT INTO Appointment (construction_id, citizen_id, estimated_cost)
            VALUES (%s, %s, %s)
        """
        cur.execute(insert_query, (construction_id, citizen_id, estimated_cost))
        conn.commit()

    conn.close()
    return f"Your Appointment for the project: '{project_name}' was succesfully submitted!"

#εδω τελειωνει το pending projects-------------------------------------------





#εδω ξεκιναει το my projects-------------------------------------

@app.route('/my_projects')
def my_projects():
    # Προσωρινά hardcoded, στη συνέχεια θα πάρεις το construction_id από το session
    construction_id = 1  # Π.χ. το ID της συνδεδεμένης κατασκευαστικής εταιρείας

    conn = get_db_connection()
    cur = conn.cursor()

    # Projects που είναι Active
    cur.execute("""
        SELECT p.id, p.name, p.information, p.start_date, p.location
        FROM Project p
        JOIN Appointment a ON a.citizen_id = p.citizen_id
        WHERE p.construction_id = %s AND p.status = 'Active'
    """, (construction_id,))
    active_projects = cur.fetchall()

    # Projects που είναι Completed
    cur.execute("""
        SELECT p.id, p.name, p.information, p.start_date, p.location
        FROM Project p
        JOIN Appointment a ON a.citizen_id = p.citizen_id
        WHERE p.construction_id = %s AND p.status = 'Completed'
    """, (construction_id,))
    completed_projects = cur.fetchall()

    conn.close()

    return render_template('my_projects.html',
                           active_projects=active_projects,
                           completed_projects=completed_projects)


@app.route('/license_application', methods=["GET", "POST"])
def license_application():
    if request.method == "POST":
        # Πάρε τα δεδομένα της φόρμας
        license_type = request.form["license_type"]
        start_date = request.form["start_date"]
        description = request.form["description"]
        project_id = request.form["project_id"]  # ή βάλε προσωρινά project_id = 1

        # Εισαγωγή στη βάση
        conn = get_db_connection()
        cur = conn.cursor()

        insert_query = """
            INSERT INTO License (project_id, license_type, license_description, start_date)
            VALUES (%s, %s, %s, %s)
        """
        cur.execute(insert_query, (project_id, license_type, description, start_date))
        conn.commit()
        conn.close()

        flash("Your license application was successfully submitted!", "success")
        return redirect(url_for("license_application"))

    return render_template("license_form.html")

#εδω τελειωνει το my projects---------------------------------------





#edw arxizoyn ta settings------------------------------------------
@app.route('/settings', methods=['GET','POST'])
def settings():
    id = 4  # προσωρινό id μέχρι να υλοποιήσεις login

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)  # dictionary=True για να πάρεις dict

    cur.execute("""
        SELECT name, email, phone_number, address
        FROM my_user
        WHERE id = %s        
    """, (id,))
    user = cur.fetchone()  # fetchone, γιατί επιστρέφεις μόνο ένα user

    conn.close()

    return render_template('settings.html', user=user)



@app.route('/logout')
def logout():
    return "<h2>Έγινε αποσύνδεση! (demo λειτουργία)"

#εδω τελειωνουν τα settings-------------------------------------






#εδω αρχιζουν τα notifications------------------------------------

from datetime import datetime

def to_datetime(dt):
    if dt is None:
        return datetime.min
    if isinstance(dt, datetime):
        return dt
    # Αν είναι date, κάνουμε μετατροπή σε datetime (με ώρα 00:00)
    return datetime.combine(dt, datetime.min.time())

@app.route('/notifications', methods=['GET','POST'])
def notifications():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT 
            pu.project_id,
            pr.name AS project_name,
            mu.name AS workshop_name,
            pu.message,
            pu.created_at,
            'progress' AS type
        FROM ProgressUpdate pu
        JOIN Project pr ON pu.project_id = pr.id
        JOIN Workshop w ON pu.workshop_id = w.user_id
        JOIN my_user mu ON w.user_id = mu.id
    """)
    progress_updates = cur.fetchall()

    cur.execute("""
        SELECT 
            n.id,
            NULL AS project_id,
            NULL AS project_name,
            NULL AS workshop_name,
            n.title AS message,
            n.date AS created_at,
            'notification' AS type
        FROM Notification n
        WHERE n.type IN ('Accepted', 'Rejected')
    """)
    notifications = cur.fetchall()

    cur.close()
    conn.close()

    combined = progress_updates + notifications

    # Μετατροπή ημερομηνιών σε datetime και ταξινόμηση
    combined.sort(key=lambda x: to_datetime(x['created_at']), reverse=True)

    return render_template('notifications.html', updates=combined)


#εδω τελειωνουν τα notifications-----------------------------------


if __name__ == '__main__':
    app.run(debug=True)

