import csv
from datetime import datetime

FILE_NAME = "assignments.csv"
assignments = []


def add_assignment():
    title = input("Assignment title: ").strip()
    course = input("Course name: ").strip()
    due_date = input("Due date (YYYY-MM-DD): ").strip()

    if not title or not course:
        print("Title and course cannot be blank.")
        return

    try:
        datetime.strptime(due_date, "%Y-%m-%d")
        if datetime.strptime(due_date, "%Y-%m-%d").strftime("%Y-%m-%d") != due_date:
            raise ValueError
    except ValueError:
        print("Please enter a valid date in YYYY-MM-DD format.")
        return

    next_id = max((item["assignment_id"] for item in assignments), default=0) + 1
    assignments.append({
        "assignment_id": next_id,
        "title": title,
        "course": course,
        "due_date": due_date,
        "status": "Pending"
    })
    print("Assignment added!")


def view_assignments():
    if not assignments:
        print("No assignments yet.")
        return

    for item in sorted(assignments, key=lambda x: x["due_date"]):
        print(f'ID: {item["assignment_id"]} | Course: {item["course"]} | '
              f'Title: {item["title"]} | Due: {item["due_date"]} | '
              f'Status: {item["status"]}')


def complete_assignment():
    try:
        selected_id = int(input("Enter assignment ID: "))
    except ValueError:
        print("Please enter a number.")
        return

    for item in assignments:
        if item["assignment_id"] == selected_id:
            item["status"] = "Completed"
            print("Assignment marked completed!")
            return

    print("Assignment ID not found.")


def save_assignments():
    try:
        with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=["assignment_id", "title", "course", "due_date", "status"]
            )
            writer.writeheader()
            writer.writerows(assignments)
        print("Assignments saved!")
    except OSError as error:
        print(f"Could not save assignments: {error}")


def load_assignments():
    try:
        with open(FILE_NAME, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            required = {"assignment_id", "title", "course", "due_date", "status"}
            if not reader.fieldnames or not required.issubset(reader.fieldnames):
                raise ValueError("Missing CSV columns")

            loaded = []
            ids = set()
            for row in reader:
                assignment_id = int(row["assignment_id"])
                date = row["due_date"]
                datetime.strptime(date, "%Y-%m-%d")
                if (assignment_id <= 0 or assignment_id in ids
                        or not row["title"].strip() or not row["course"].strip()
                        or row["status"] not in ("Pending", "Completed")):
                    raise ValueError("Invalid assignment data")
                ids.add(assignment_id)
                loaded.append({
                    "assignment_id": assignment_id,
                    "title": row["title"],
                    "course": row["course"],
                    "due_date": date,
                    "status": row["status"]
                })
        assignments.clear()
        assignments.extend(loaded)
        print("Assignments loaded!")
    except FileNotFoundError:
        print("No saved file found. Add assignments to get started.")
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(f"Could not load assignments: {error}")


def main():
    while True:
        print("\n--- Student Assignment Tracker ---")
        print("1. Add Assignment")
        print("2. View Assignments")
        print("3. Mark Assignment Completed")
        print("4. Save Assignments")
        print("5. Load Assignments")
        print("6. Exit")

        choice = input("Choose an option (1-6): ").strip()
        if choice == "1":
            add_assignment()
        elif choice == "2":
            view_assignments()
        elif choice == "3":
            complete_assignment()
        elif choice == "4":
            save_assignments()
        elif choice == "5":
            load_assignments()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
