class ProjectDeletionSystem:
    def __init__(self):
        # έργο -> {"status": "Pending" ή "Αναλήφθηκε", "owner": user}
        self.projects = {
            "project_1": {"status": "Pending", "owner": "user123"},
            "project_2": {"status": "Αναλήφθηκε", "owner": "user123"}
        }

    def delete_project_flow(self, user, project_name):
        print(f"\n[INFO] Ο χρήστης {user} επιχειρεί να διαγράψει το έργο {project_name}.")

        # Έλεγχος αν το έργο υπάρχει
        project = self.projects.get(project_name)
        if not project:
            print("Σφάλμα: Το έργο δεν βρέθηκε.")
            return

        # Έλεγχος αν ο χρήστης είναι ο ιδιοκτήτης
        if project["owner"] != user:
            print("Σφάλμα: Δεν έχετε δικαίωμα διαγραφής του έργου.")
            return

        # Έλεγχος κατάστασης έργου
        if project["status"] != "Pending":
            # Εναλλακτική ροή 1
            print("Το έργο δεν βρίσκεται πλέον σε κατάσταση 'Pending'.")
            print("Ακύρωση: Δεν μπορεί να διαγραφεί λόγω αλλαγής κατάστασης.")
            return "Alternative Flow 1"

        # Προεπισκόπηση και επιβεβαίωση διαγραφής
        print(f"Προεπισκόπηση διαγραφής του έργου '{project_name}'...")
        confirm = input("Επιβεβαιώνετε διαγραφή; (ναι/όχι): ").strip().lower()

        if confirm == "όχι":
            # Εναλλακτική ροή 2
            print("Η διαδικασία διαγραφής ακυρώθηκε από τον χρήστη.")
            return "Alternative Flow 2"

        # Ολοκλήρωση διαγραφής
        del self.projects[project_name]
        print("Το έργο διαγράφηκε επιτυχώς.")
        return "Basic Flow"

# Παράδειγμα χρήσης
system = ProjectDeletionSystem()

# 1. Βασική ροή
system.delete_project_flow("user123", "project_1")

# 2. Εναλλακτική ροή 1: έργο δεν είναι πλέον Pending
system.delete_project_flow("user123", "project_2")

# 3. Εναλλακτική ροή 2: ο χρήστης ακυρώνει την ενέργεια (π.χ. πατάει "όχι")
# Δοκίμασε να τρέξεις την παρακάτω γραμμή και να απαντήσεις "όχι" όταν ερωτηθείς
# system.delete_project_flow("user123", "project_1")
