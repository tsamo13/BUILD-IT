class EvaluationSystem:
    def __init__(self):
        self.submitted_evaluations = {}  # έργο -> χρήστης

    def has_user_already_evaluated(self, user, project):
        return self.submitted_evaluations.get(project) == user

    def submit_evaluation(self, user, project, rating, comment):
        if self.has_user_already_evaluated(user, project):
            print("Σφάλμα: Η αξιολόγηση έχει ήδη υποβληθεί για αυτό το έργο.")
            return "Alternative Flow 1"

        if len(comment) > 500:
            print("Σφάλμα: Το σχόλιο υπερβαίνει το όριο χαρακτήρων (500).")
            return "Alternative Flow 3"

        self.preview_evaluation(user, project, rating, comment)

    def preview_evaluation(self, user, project, rating, comment):
        print(f"Προεπισκόπηση αξιολόγησης για το έργο {project} από τον χρήστη {user}:")
        print(f"Βαθμολογία: {rating}, Σχόλιο: {comment[:50]}...")
        proceed = input("Επιβεβαιώνετε την υποβολή; (ναι/όχι): ").lower()
        if proceed == "ναι":
            self.submitted_evaluations[project] = user
            print("Η αξιολόγηση υποβλήθηκε επιτυχώς.")
        else:
            print("Η αξιολόγηση ακυρώθηκε.")
            return "Alternative Flow 2"

# Παράδειγμα χρήσης
system = EvaluationSystem()

# Βασική ροή
user = "user123"
project = "project_A"
rating = 4
comment = "Πολύ καλό έργο, με σωστή τεκμηρίωση και υλοποίηση."

result = system.submit_evaluation(user, project, rating, comment)

# Εναλλακτική ροή 1: προσπαθεί να υποβάλει ξανά για το ίδιο έργο
system.submit_evaluation(user, project, 3, "Δεύτερη απόπειρα.")

# Εναλλακτική ροή 3: σχόλιο με πάνω από 500 χαρακτήρες
long_comment = "a" * 501
system.submit_evaluation("user456", "project_B", 5, long_comment)
