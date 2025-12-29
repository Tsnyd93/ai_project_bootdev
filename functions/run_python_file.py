import os
import subprocess
from google.genai import types
def run_python_file(working_directory, file_path, args=None):
    try:
        abs_working_directory=os.path.normpath(os.path.abspath(working_directory))
        join_path= os.path.join(abs_working_directory,file_path)
        abs_file_path=os.path.normpath(join_path)

        if os.path.commonpath([abs_working_directory,abs_file_path])!=abs_working_directory:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
             return f'Error: "{file_path}" does not exist or is not a regular file'
        if not abs_file_path.endswith(".py"):
             return f'Error: "{file_path}" is not a Python file'
        
        command =["python", abs_file_path]
        if args is not None:
            command.extend(args)
        completed=subprocess.run(command,
        cwd=abs_working_directory,
        capture_output=True,
        text=True,
        timeout=30,
        )
        output=""
        if completed.returncode != 0:
            output +=  f"Process exited with code {completed.returncode}\n"
        if not completed.stdout and not completed.stderr:
            if not output:
                output="No output produced"
            else:
                output +="No output produced"
        else:
            if completed.stdout:
                output+= f"STDOUT:{completed.stdout}"
            if completed.stderr:
                output += f"STDERR:{completed.stderr}"

        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"
    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a Python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working dictionary",
                ),"args": types.Schema(type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of command-line arguments to pass to the Python file")
        },
        required=["file_path"],
        ),
    )