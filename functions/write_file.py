import os 
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        abs_working_directory=os.path.normpath(os.path.abspath(working_directory))
        join_path= os.path.join(abs_working_directory,file_path)
        abs_file_path=os.path.normpath(join_path)

        if os.path.commonpath([abs_working_directory,abs_file_path])!=abs_working_directory:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(abs_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)

        with open(abs_file_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'
    

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="allows prgram to edit files",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="path to the python file to edit, relative to the working dictionary",
                ),"content": types.Schema(type=types.Type.STRING
                ,
                description="Required content to add to the file")
        },
        required=["file_path","content"]
        ),
    )