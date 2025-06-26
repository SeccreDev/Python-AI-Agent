import os
from google.genai import types

def get_files_info(working_directory, directory=None):
    """
    Returns a formatted list of files and directories within the given directory.

    The function ensures the requested path stays within the working directory.
    Each listed file includes its name, size in bytes, and whether it's a directory.

    Args:
        working_directory (str): The root directory within which operations are allowed.
        directory (str, optional): A subdirectory within the working directory to list.

    Returns:
        str: A string containing metadata of each item in the directory,
             or an error message if the path is invalid or an exception occurs.
    """
    # Get the absolute paths for working directory
    working_path = os.path.abspath(working_directory)
    
    if directory is None:
        # Use the root working directory if no subdirectory is provided
        full_path = working_path
    else:
        # Get the absolute paths for working directory and target directory
        full_path = os.path.abspath(os.path.join(working_path, directory))

        # Restrict execution to within the working directory
        if not full_path.startswith(working_path):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Ensure that the full path is to a directory
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
    
    try:
        contents = ""
        for file in os.listdir(full_path):
            full_file_path = os.path.join(full_path, file)
            
            # Append file info: name, size, and type
            contents += f"- {file}: file_size={os.path.getsize(full_file_path)} bytes, is_dir={os.path.isdir(full_file_path)}\n"
        contents = contents.rstrip()
        return contents
    except Exception as e:
        return f"Error listing files: {e}"

# This schema is used to describe the function to the Google GenAI model so it can invoke the function with structured input.
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            )
        }
    )
)