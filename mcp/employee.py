import sqlite3  # Standard Python library for interacting with SQLite databases
from typing import List, Optional  # Type hints for better code readability and validation
from pydantic import BaseModel  # Base class from Pydantic for data validation and parsing


# Define an Employee model that represents one row in the "employees" table.
# Inherits from Pydantic's BaseModel, so it automatically validates types and structures.
class Employee(BaseModel):
    id: int       # Employee ID (primary key in DB)
    name: str     # Employee's name
    role: str     # Job title or role of the employee
    salary: float # Salary amount for the employee

    @classmethod
    def get_by_id(cls, emp_id: int, db_file: str = "employees.db") -> Optional["Employee"]:
        """
        Fetch a single employee by their unique ID.

        Args:
            emp_id (int): The ID of the employee to fetch.
            db_file (str): Path to the SQLite database file. Defaults to "employees.db".

        Returns:
            Employee object if found, otherwise None.
        """
        
        # Open a connection to the SQLite database
        conn = sqlite3.connect(db_file)
        
        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()
        
        # Execute a parameterized SQL query to prevent SQL injection.
        # The `?` placeholder ensures safe substitution of `emp_id`.
        cursor.execute(
            "SELECT id, name, role, salary FROM employees WHERE id = ?", 
            (emp_id,)  # Tuple is required here
        )
        
        # Fetch the first matching row (or None if no match)
        row = cursor.fetchone()
        
        # Close the database connection to free resources
        conn.close()

        # If a record is found, create an Employee instance from the row data
        if row:
            return cls(id=row[0], name=row[1], role=row[2], salary=row[3])
        
        # If no record found, return None
        return None


    @classmethod
    def get_all(cls, db_file: str = "employees.db") -> List["Employee"]:
        """
        Fetch all employee records from the database.

        Args:
            db_file (str): Path to the SQLite database file. Defaults to "employees.db".

        Returns:
            List[Employee]: A list of Employee objects.
        """

        # Open a connection to the SQLite database
        conn = sqlite3.connect(db_file)
        
        # Create a cursor object
        cursor = conn.cursor()
        
        # Execute a query to select all employees
        cursor.execute("SELECT id, name, role, salary FROM employees")
        
        # Fetch all rows (list of tuples)
        rows = cursor.fetchall()
        
        # Close the database connection
        conn.close()

        # Convert each tuple (row) into an Employee instance using list comprehension
        return [
            cls(id=r[0], name=r[1], role=r[2], salary=r[3])
            for r in rows
        ]

    @classmethod
    def add_employee(cls,  name: str, role: str, salary: float, db_file: str = "employees.db") -> bool:
        """
        Add a new employee to the database.

        Args:
            emp_id (int): Employee ID (must be unique)
            name (str): Employee's name
            role (str): Job title
            salary (float): Employee's salary
            db_file (str): Path to SQLite database file

        Returns:
            bool: True if insertion successful, False otherwise
        """
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()

            # Create the table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    role TEXT NOT NULL,
                    salary REAL NOT NULL
                )
            """)

            # Insert the new employee record using parameterized query
            cursor.execute(
                "INSERT INTO employees (name, role, salary) VALUES (?, ?, ?)",
                (name, role, salary)
            )

            conn.commit()  # Save changes
            conn.close()
            return True
        except sqlite3.IntegrityError:
            # This will be raised if the employee ID already exists
            return False
        except Exception as e:
            print(f"Error inserting employee: {e}")
            return False    


