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