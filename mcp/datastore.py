import sqlite3

class EmployeeDB:
    def __init__(self, db_file: str = "employees.db"):
        self.db_file = db_file
        self._create_table()

    def _create_table(self):
        """Create employees table if it does not exist."""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    role TEXT NOT NULL,
                    salary REAL NOT NULL
                )
            """)
            conn.commit()

    def add_employee(self, name: str, role: str, salary: float) -> int:
        """Insert a new employee and return the inserted ID."""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO employees (name, role, salary)
                VALUES (?, ?, ?)
            """, (name, role, salary))
            conn.commit()
            return cursor.lastrowid


# ---------- Example usage ----------
if __name__ == "__main__":
    db = EmployeeDB()

    # Save employee details
    emp_id1 = db.add_employee("Alice", "Data Scientist", 120000)
    emp_id2 = db.add_employee("Bob", "ML Engineer", 110000)
    emp_id3 = db.add_employee("arpan", "ML Engineer", 150000)
    emp_id4 = db.add_employee("shilpa", "ML Engineer", 160000)

    print(f"Inserted Alice with ID {emp_id1}")
    print(f"Inserted Bob with ID {emp_id2}")
    print(f"Inserted arpan with ID {emp_id3}")
    print(f"Inserted shilpa with ID {emp_id4}")
