import textwrap, re
import json
import marvin
from openai import AuthenticationError
from marvin.beta.assistants import Assistant
from diff_match_patch import diff_match_patch
from marvin.beta.assistants import Thread, Assistant, PrintHandler
event_handler_class=marvin.beta.assistants.PrintHandler

def run_editor(submit_text, key):
    """
    Called in 'uploader' in 'views.py'
    """

    # Create an OpenAI Assistant with marvin
    assistant = Assistant(instructions="You are a professional copy editor who fixes typos and grammatical mistakes in text. You follow the Chicago Manual of Style for writing numbers, capitalization, headers, and punctuation. You make minimal edits to the voice or style of the prose.", model="gpt-3.5-turbo")
    marvin.settings.openai.api_key = key
    marvin.settings.openai.chat.completions.temperature = 0.1

    edited_text = ""
    run_count = 0
    chunk_count = (len(submit_text) // 4000) + 1  # for updating progress on terminal

    wrapped_text = textwrap.wrap(submit_text, width=4000, replace_whitespace=False, drop_whitespace=False)
    for submit_chunk in wrapped_text:
        try:
            # Call assistant.say and handle potential exceptions
            response = assistant.say(submit_chunk)

            # Access edited text based on library/API response structure (check documentation)
            # Assuming response is a dictionary with 'data', 'choices', and 'text' keys
            # Modify this section based on your actual response structure
            edited_text += response['data']['choices'][0]['text']

            print(edited_text)  # You can adjust the printing location as needed
        except AuthenticationError:
            return "key invalid"
        except Exception as e:  # Catch other potential exceptions
            print(f"Error: {e}")  # Log or handle the error appropriately

        run_count += 1
        print("Finished {:.0%}".format(run_count / chunk_count))
    print(edited_text)    
    return edited_text


def get_title(text):
    """
    Called in 'uploader'
    Take result text from uploader() and generate a title.
    Selects first 50 characters. If there is a line-break before the first 50, the title will end there.
    """
    text = text[:50].split("\n")
    # Clear any blank lines at top. Response saved from chatGPT usually has one.
    if text[0] == "":
        text = text[1:]
    title = text[0]
    return title


def compare_text(original_text, edited_text):
    """
    Called in 'workshop_render'. Builds a set of text to show the user on the HTML page.
    """

    dmp = diff_match_patch()
    dmp.Diff_Timeout = 0
    diffs = dmp.diff_main(original_text, edited_text)
    dmp.diff_cleanupSemantic(diffs)

    html_preview = dmp.diff_prettyHtml(diffs)

    # Clean out blank <ins> tags which diff_prettyHtml creates
    pattern = re.compile(r'<ins>\s*</ins>')
    html_preview = re.sub(pattern, '', html_preview)
    return html_preview
