import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path):
    """
    Executes a Python file located within a specified working directory.

    Args:
        working_directory (str): The base directory within which files are allowed to be executed.
        file_path (str): The relative path to the Python file to be executed.

    Returns:
        str: The output of the Python file execution, including stdout, stderr, or error messages.
    """
    # Get the absolute paths for working directory and target file
    working_path = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_path, file_path))

    # Restrict execution to within the working directory
    if not full_path.startswith(working_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    # Ensure the file exists
    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'

    # Ensure it's a Python file
    if not full_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        # Run the Python file using subprocess
        result = subprocess.run(
            ["python3", full_path],
            cwd=working_path,
            capture_output=True,
            text=True,
            timeout=30  # Set a timeout to prevent long-running scripts
            )

        output = []
        # Capture stdout if present
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout.strip()}")
        
        # Capture stderr if present
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr.strip()}")
        
        # Include exit code if not 0
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        
        if not output:
            return "No output produced."

        return "\n".join(output)

    except Exception as e:
        return f"Error: executing Python file: {e}"

# This schema is used to describe the function to the Google GenAI model so it can invoke the function with structured input.
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the python file that is going to be executed.",
            )
        }
    )
)