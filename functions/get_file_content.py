import os
from google.genai import types
from config import MAX_CHARS
def get_file_content(working_directory, file_path):
    try:
        abs_working_directory=os.path.normpath(os.path.abspath(working_directory))
        join_path= os.path.join(abs_working_directory,file_path)
        abs_file_path=os.path.normpath(join_path)

        if os.path.commonpath([abs_working_directory,abs_file_path])!=abs_working_directory:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
       

        with open(abs_file_path, "r") as f:
            file_content_string= f.read(MAX_CHARS) 
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    except Exception as e:
        return f'Error: {e}'
    return file_content_string


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get the contents of a file. Use this to call get_file_content with a file_path.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory",
            ),
        },
        required=["file_path"],
    ),
)