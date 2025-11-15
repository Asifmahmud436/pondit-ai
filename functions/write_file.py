import os

def write_file(working_directory, file_path, content):
    abs_path = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory,file_path))
    if not target_file.startswith(abs_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        parent_dir = os.path.dirname(target_file)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir,exist_ok=True)
        with open(target_file, 'w') as f:
            f.write(content)
            return f'{len(content)} characters written'
    except Exception as e:
        return f'Error writing file: {e}'
    