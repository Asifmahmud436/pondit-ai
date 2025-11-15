import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    abs_path = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory,file_path))
    if not target_file.startswith(abs_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(target_file):
        return f'Error: File "{file_path}" not found.'
    if not target_file.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        cmd = ['uv','run',target_file]
        if args:
            cmd += args.split()
        result = subprocess.run(cmd,cwd=working_directory,timeout=30,capture_output=True,text=True)
        stdout = result.stdout
        stderr = result.stderr
        return f"STDOUT:{stdout} \n STDERR:{stderr}"
    except Exception as e:
        return f"Error: executing Python file: {e}"