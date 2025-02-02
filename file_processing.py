
import re

def process_file(file_path):
    """Cleans the _chat.txt file by removing unwanted characters and modifying the structure."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Step 1: Remove emojis using regex (same as before)
        emoji_pattern = re.compile(
            "[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F"
            "\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F"
            "\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251]+",
            flags=re.UNICODE
        )
        cleaned_content = re.sub(emoji_pattern, '', content)

        # Step 2: Remove asterisks (*)
        cleaned_content = cleaned_content.replace('*', '')

        # Step 3: Remove double spaces
        cleaned_content = re.sub(r'\s{2,}', ' ', cleaned_content)

        # Step 5: Remove all newlines to make the content a single line
        cleaned_content = cleaned_content.replace('\n', ' ')

        # Step 4: Remove content inside square brackets and replace with a new line
        cleaned_content = re.sub(r'\[.*?\]', '\n', cleaned_content)


        # Save cleaned content back to file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(cleaned_content)

        print("File processed successfully.")

    except Exception as e:
        print(f"Error processing the file: {e}")



def clean_json(text_content):
    cleaned_content = text_content.strip()

    # Find the first opening square bracket and the last closing curly brace
    start_index = cleaned_content.find("[")
    last_curly_brace_index = cleaned_content.rfind("}")

    # Debugging output (if needed)
    print(f"Start index of '[': {start_index}")
    print(f"Last curly brace index: {last_curly_brace_index}")

    # Check if there is an opening square bracket '[' and a last closing curly brace '}'
    if start_index != -1 and last_curly_brace_index != -1:
        # Extract the part of the string inside the square brackets
        cleaned_content = cleaned_content[start_index:last_curly_brace_index + 1]

        # Add the closing square bracket (if it's missing)
        cleaned_content += "]"
        # This will raise an error if the JSON is invalid
        return cleaned_content



