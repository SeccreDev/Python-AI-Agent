import os
from google.genai import types
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    working_path = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_path, file_path))

    if not full_path.startswith(working_path):
        f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(full_path):
        f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(full_path, "r") as file:
            file_content = file.read(MAX_CHARS)

            if os.path.getsize(full_path) > MAX_CHARS:
                content += (f'[...File "{file_path}" truncated at {MAX_CHARS} characters]')
            
        return file_content
    except Exception as e:
        return f"Error listing content: {e}"

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