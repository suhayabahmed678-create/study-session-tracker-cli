import json
from pathlib import Path
from datetime import datetime, timedelta

# Settings
DB_FILE = Path("study_sessions.json")

class SessionStore:

    def load_data(self):
        if DB_FILE.exists():
            try:
                with open(DB_FILE , "r", encoding="utf 8") as f:
                    data = json.load(f)

            except Exception:
                return {"sessions": []}
        return {"sessions": []}

    def save_data(self, data):
        with open(DB_FILE, "w", encoding="utf 8") as f:
            json.dump(data, f, indent=2)


# Study Logic Layer
class StudyTracker:
    def __init__(self):
        self.store = SessionStore()
        self.payload = self.store.load_data()

    def add_record(self, subject, hours):
        entry = {
            "date" :datetime.now().isoformat(),
            "subject": subject.strip().title(),
            "hours": float(hours)
        }

        self.payload["sessions"].append(entry)
        self.store.save_data(self.payload)

        print(f"✔ Recorded: {entry['subject']} ({hours}h)")

        # ---- aggregate ----
        def subject_summary(self):
            result = {}
            for s in self.payload["sessions"]:
                key = s["subject"]
                result[key] = result.get(key, 0) + s["hours"]

            return dict(sorted(result.items()))

        # ---- last N days ----
        def hours_in_days(self, days=7):
            border = datetime.now() - timedelta(days=days)
            total = 0

            for s in self.payload["sessions"]:
                d = datetime.fromisoformat(s["date"])
                if d >= border:
                    total += s["hours"]

            return round(total, 2)

        # ---- streak days ----
        def active_days(self):
            days = {s["date"][:10] for s in self.payload["sessions"]}
            return len(days)

# Console UI
class TrackerCLI:
    def __init__(self):
        self.tracker = StudyTracker()

    def menu(self):
        print("\n=== Study Tracker ===")
        print("1 → Add session")
        print("2 → Show report")
        print("3 → Exit")

    def handle(self):
        sub = input("subject:")
        try :
            hours = int(input("hours:"))
        except ValueError:
            print("invalid hours")
            return

        self.tracker.add_record(sub, hours)

    def handle_report(self):
        print("\n📊 Subject Summary")
        data = self.tracker.subject_summary()

        if not data:
            print("no sessions yet ")
        else:
            for k, v in data.items():
                print(f"{k:<12} {v} hrs")

        print("\n🗓 Last 7 days:", self.tracker.hours_in_days(7))
        print("🔥 Active days:", self.tracker.active_days())

    def run(self):
        while True:
            self.menu()
            choice = input("Select: ").strip()

            if choice == "1":
                self.handle_add()

            elif choice == "2":
                self.handle_report()

            elif choice == "3":
                break

            else:
                print("unknown option")


if __name__ == "__main__":
    TrackerCLI().run()
