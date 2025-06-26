import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    """
    Entry point for the AI Code Assistant.

    Loads environment variables, processes command-line arguments, initializes
    the Gemini client, and handles iterative content generation.
    """
    load_dotenv()
    
    # Check for verbose mode
    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("AI Code Assistant\n")
        print('Usage: python main.py "prompt" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)
    if verbose:
        print(f"User prompt: {user_prompt}")

    # Initialize conversation with user prompt
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    for i in range (20):
        if i == 19:
            print(f"Maximum iterations ({i+1}) reached.")
            sys.exit(1)

        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")


def generate_content(client, messages, verbose):
    """
    Handles content generation and function calls using the Gemini API.

    Args:
        client (genai.Client): The Gemini API client.
        messages (list): Conversation history.
        verbose (bool): Whether to print debug output.

    Returns:
        str | None: The final response text if available, else None.

    Raises:
        Exception: If function call fails or no valid response is generated.
    """
    response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    # Add candidate responses to conversation
    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            messages.append(function_call_content)

    # If no function call needed, return the response text
    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (not function_call_result.parts or not function_call_result.parts[0].function_response):
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("No function responses generated, exiting.")
    
    # Add tool responses to conversation
    messages.append(types.Content(role="tool", parts=function_responses))



if __name__ == "__main__":
    main()