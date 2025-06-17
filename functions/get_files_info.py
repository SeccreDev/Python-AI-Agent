import os
def get_files_info(working_directory, directory=None):
    working_path = os.path.abspath(working_directory)
    
    if directory is None:
        full_path = working_path
    else:
        full_path = os.path.abspath(os.path.join(working_path, directory))

        if not full_path.startswith(working_path):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
    
    try:
        contents = ""
        for file in os.listdir(full_path):
            full_file_path = os.path.join(full_path, file)
            contents += f"- {file}: file_size={os.path.getsize(full_file_path)} bytes, is_dir={os.path.isdir(full_file_path)}\n"
        contents = contents.rstrip()
        return contents
    except Exception as e:
        return f"Error listing files: {e}"

def get_file_content(working_directory, file_path):
    working_path = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_path, file_path))

    if not full_path.startswith(working_path):
        f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(full_path):
        f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        MAX_CHARS = 10000
        with open(full_path, "r") as file:
            file_content = file.read(MAX_CHARS)
        file_content += f"[...File '{file_path}' truncated at 10000 characters]" 
        return file_content
    except Exception as e:
        return f"Error listing content: {e}"

