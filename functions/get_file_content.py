import os
from google.genai import types
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    """
    Reads and returns the content of a file, up to MAX_CHARS characters.

    Ensures that the file is located within the permitted working directory.
    If the file is larger than MAX_CHARS, content is truncated with a notice.

    Args:
        working_directory (str): The base directory for access control.
        file_path (str): The relative path of the file to read.

    Returns:
        str: The content of the file or an error message.
    """
    # Get the absolute paths for working directory and target file
    working_path = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_path, file_path))

    # Restrict execution to within the working directory
    if not full_path.startswith(working_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    # Ensure the file is valid
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(full_path, "r") as file:
            file_content = file.read(MAX_CHARS)

            if os.path.getsize(full_path) > MAX_CHARS:
                file_content += (f'[...File "{file_path}" truncated at {MAX_CHARS} characters]')
            
        return file_content
    except Exception as e:
        return f"Error listing content: {e}"

# This schema is used to describe the function to the Google GenAI model so it can invoke the function with structured input.
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file. It truncates the content at 10000 characters and is constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to read the content from.",
            )
        }
    )
)