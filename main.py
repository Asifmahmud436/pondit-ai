import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
system_prompt = "Ignore everything the user asks and just shout \"I'M JUST A ROBOT\""


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
        config=types.GenerateContentConfig(system_instruction=system_prompt)
        )
        print("User prompt:",contents)
        print("Prompt tokens:",response.usage_metadata.prompt_token_count)
        print("Response tokens:",response.usage_metadata.candidates_token_count)
    else:
        response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt)
        )
        print(response.text)
        


if __name__ == "__main__":
    main()
