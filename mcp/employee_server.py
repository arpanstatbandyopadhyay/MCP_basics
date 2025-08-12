# Import the FastMCP class (a high-level MCP server wrapper) and the Server class from the MCP framework.
# FastMCP makes it easier to register tools and run a server with minimal boilerplate.
from mcp.server import FastMCP, Server

# Import the Employee class we defined earlier.
# This is our Pydantic model with database interaction methods (get_by_id, get_all, etc.).
from employee import Employee


# Create an MCP server instance named "EmployeeServer".
# This will be the logical name of the server when clients discover or interact with it.
mcp = FastMCP("EmployeeServer")


# Register an MCP tool (endpoint) that can be called remotely by MCP clients.
# The decorator `@mcp.tool()` automatically exposes this function as an available MCP tool.
@mcp.tool()
def get_employee_by_id(emp_id: int) -> dict:
    """
    Fetch a single employee by ID.

    Args:
        emp_id (int): The unique identifier of the employee.

    Returns:
        dict: Dictionary containing employee data if found, 
              or an error message if the ID does not exist.
    """
    # Use the Employee model's class method to fetch data from the SQLite database.
    emp = Employee.get_by_id(emp_id)
    
    # If the employee exists, return their details as a dictionary.
    # The .dict() method is provided by Pydantic's BaseModel for easy serialization.
    if emp:
        return emp.dict()
    
    # If no matching employee is found, return an error message in a dictionary format.
    return {"error": f"Employee with ID {emp_id} not found"}


# Register another MCP tool to fetch ALL employees.
@mcp.tool()
def get_all_employees() -> list:
    """
    Fetch all employees from the database.

    Returns:
        list: A list of dictionaries, where each dictionary contains an employee's details.
    """
    # Call Employee.get_all() to retrieve all employee records from the DB.
    employees = Employee.get_all()
    
    # Convert each Employee object to a dictionary for easy JSON serialization.
    return [emp.dict() for emp in employees]


# Register an MCP tool to add a new employee to the database
@mcp.tool()
def add_employee(name: str, role: str, salary: float) -> dict:
    """
    Add a new employee to the database.

    Args:
        emp_id (int): Unique employee ID.
        name (str): Employee's full name.
        role (str): Job title or role.
        salary (float): Employee's salary.

    Returns:
        dict: A success message if added successfully, or an error message otherwise.
    """
    success = Employee.add_employee(name, role, salary)
    
    if success:
        return {"success": f"Employee {name} added successfully"}
    else:
        return {"error": f"Failed to add employee with name {name}.  there was a DB error."}



# Standard Python entry point check to ensure the server runs only when executed directly.
# This avoids accidental execution if the file is imported elsewhere.
if __name__ == "__main__":
    # Start the MCP server and listen for incoming client requests.
    # This will block the main thread and keep the server running until stopped.
    mcp.run()
