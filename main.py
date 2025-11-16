import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import available_functions
load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


def main():
    if len(sys.argv) == 1:
        print("No prompt was provided")
        exit(1)
    contents = sys.argv[1]
    messages = [
        types.Content(role='user',parts=[types.Part(text=contents)])
    ]
    
    if '--verbose' in sys.argv:
        response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=contents,
        config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt)
        )
        print("User prompt:",contents)
        print("Prompt tokens:",response.usage_metadata.prompt_token_count)
        print("Response tokens:",response.usage_metadata.candidates_token_count)
    else:
        response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
        )
        print(response.text)
        
    if not response.function_calls:
        return response.text

    for function_call_part in response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        


if __name__ == "__main__":
    main()
