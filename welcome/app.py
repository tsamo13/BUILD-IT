from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Σύνδεση στη βάση MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="databases_project",
    port=3306
)
cursor = db.cursor()

# Δημιουργία λογαριασμού (Αρχική σελίδα)
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form["surname"]
        email = request.form["email"]
        password = request.form["password"]
        phone = request.form["phone"]
        address = request.form["address"]
        user_type = request.form["user_type"]
        info = request.form["information"]

        try:
            # Εισαγωγή στον πίνακα User
            cursor.execute("""
                INSERT INTO User (name, email, password, phone_number, address)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, email, password, phone, address))
            db.commit()

            user_id = cursor.lastrowid
            print(f"✅ Νέα εγγραφή στον πίνακα User: ID={user_id}, Email={email}, Όνομα={name}")

            # Εισαγωγή στον πίνακα τύπου
            if user_type == "Citizen":
                cursor.execute("INSERT INTO Citizen (user_id) VALUES (%s)", (user_id,))
            elif user_type == "Construction":
                cursor.execute("""
                    INSERT INTO Construction (user_id, description, location, available)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, info, address, True))
            elif user_type == "Workshop":
                cursor.execute("""
                    INSERT INTO Workshop (user_id, workshop_type, description, location, available)
                    VALUES (%s, %s, %s, %s, %s)
                """, (user_id, info, info, address, True))

            db.commit()

            # 🔁 Redirect ανάλογα με τον τύπο χρήστη
            if user_type == "Citizen":
                return redirect("/citizen")
            elif user_type == "Workshop":
                return redirect("/workshop")
            elif user_type == "Construction":
                return redirect("/welcome")  # ✅ Construction πάει στο welcome
            else:
                return redirect("/welcome")  # fallback

        except mysql.connector.Error as err:
            return f"<h3>Σφάλμα κατά την εγγραφή: {err}</h3>"

    return render_template("create_account.html")


# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        try:
            cursor.execute("""
                SELECT id, name FROM User
                WHERE email = %s AND password = %s
            """, (email, password))
            row = cursor.fetchone()

            if row:
                user_id, name = row

                # Έλεγχος τύπου χρήστη
                cursor.execute("SELECT user_id FROM Citizen WHERE user_id = %s", (user_id,)) # type: ignore
                if cursor.fetchone():
                    return redirect("/citizen")

                cursor.execute("SELECT user_id FROM Workshop WHERE user_id = %s", (user_id,)) # type: ignore
                if cursor.fetchone():
                    return redirect("/workshop")

                cursor.execute("SELECT user_id FROM Construction WHERE user_id = %s", (user_id,)) # type: ignore
                if cursor.fetchone():
                    return redirect("/welcome")  # ✅ Construction => welcome

                return "<h3>Ο χρήστης δεν ανήκει σε αναγνωρισμένο τύπο.</h3>"

            else:
                return "<h3>Λάθος email ή κωδικός.</h3>"

        except mysql.connector.Error as err:
            return f"<h3>Σφάλμα βάσης: {err}</h3>"

    return render_template("login.html")


# Σελίδες για κάθε τύπο χρήστη
@app.route("/welcome")
def welcome():
    return render_template("index.html")  # ✅ Construction homepage

@app.route("/citizen")
def citizen_home():
    return render_template("citizen_home.html")

@app.route("/workshop")
def workshop_home():
    return render_template("workshop_home.html")

@app.route("/construction")
def construction_home():
    return render_template("construction_home.html")  # optional, αν θελήσεις custom

@app.route("/citizen/notifications")
def citizen_notifications():
    return render_template("citizen_notifications.html")

if __name__ == "__main__":
    app.run(debug=True)
