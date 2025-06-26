import os
from google.genai import types

def write_file(working_directory, file_path, content):
    """
    Writes content to a specified file within a permitted working directory.
    Creates necessary directories if they do not exist.

    Args:
        working_directory (str): The base directory where writing is permitted.
        file_path (str): The relative path to the file to write.
        content (str): The text content to write into the file.

    Returns:
        str: Success message or an error message describing the failure.
    """
    # Get the absolute paths for working directory and target file
    working_path = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_path, file_path))

    # Restrict execution to within the working directory
    if not full_path.startswith(working_path):
        f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    # If file does not exist, create parent directories as needed
    if not os.path.exists(full_path):
        try:
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
        except Exception as e:
            return f"Error: creating directory: {e}"

    # Prevent overwriting a directory with a file
    if os.path.exists(full_path) and os.path.isdir(full_path):
        return f'Error: "{file_path}" is a directory, not a file'

    # Write the content to the file
    try:
        with open(full_path, "w") as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: writing to file: {e}"

# This schema is used to describe the function to the Google GenAI model so it can invoke the function with structured input.
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite files",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the python file that is going to be executed.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that is being written to a file",
            )
        }
    )
)