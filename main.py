import re
import zipfile
from io import BytesIO
from flask import Flask, request, render_template
import json
import requests
from file_processing import process_file, clean_json
from gemini_processing import process_text_with_gemini

app = Flask(__name__)

# Send content to external API
def send_to_api(content):
    url = "https://mysite-x067.onrender.com/rides/add_rides"
    headers = {"Content-Type": "application/json"}
    json_content = json.loads(content)
    try:
        response = requests.post(url, json=json_content, headers=headers, timeout=100)  # Added timeout
        response.raise_for_status()  # Raise an error for bad HTTP responses
        return "Content successfully sent to the API!"
    except requests.exceptions.RequestException as e:
        # Log or print the error
        print(f"Error sending content to API: {e}")
        return f"Failed to send content: {e}"

# Process in chunks function
def process_in_chunks(txt_data, chunk_size=150):
    # Initialize results
    results = []

    # Process lines in chunks
    lines = txt_data.splitlines()

    while lines:
        # Read the next chunk
        chunk = lines[:chunk_size]
        lines = lines[chunk_size:]  # Remove the processed lines

        # Join the chunk into a string
        chunk_text = '\n'.join(chunk)

        # Process chunk with Gemini
        processed_data = process_text_with_gemini(chunk_text)
        processed_data = clean_json(processed_data)

        # Store processed result
        results.append(processed_data)

    return results

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST" and "file" in request.files:
        file = request.files["file"]
        if not file.filename.endswith(".zip"):
            return "Please upload a ZIP file"

        # Read the ZIP file into memory
        zip_data = file.read()
        zip_file = zipfile.ZipFile(BytesIO(zip_data), 'r')

        # Check if _chat.txt exists in the ZIP file
        if "_chat.txt" not in zip_file.namelist():
            return "No _chat.txt found in the ZIP file"

        # Extract the content of _chat.txt
        with zip_file.open("_chat.txt") as txt_file:
            txt_data = txt_file.read().decode('utf-8')

        # Clean the extracted content
        process_file(txt_data)

        # Process the file in chunks
        processed_results = process_in_chunks(txt_data)

        # Combine all processed results into a single response
        final_result = '\n'.join(processed_results)
        final_result = re.sub(r'\]\s*\[\s*', ', ', final_result)
        final_result = clean_json(final_result)

        return render_template("index.html", content=final_result)

    return render_template("index.html", content=None)

@app.route("/post_to_api", methods=["POST"])
def post_to_api():
    if "content" in request.form:
        content = request.form["content"]  # Get the content from the form
        result_message = send_to_api(content)  # Send the content to the API
        return render_template("index.html", content=content, result_message=result_message)
    return render_template("index.html", content=None)

if __name__ == "__main__":
    app.run(debug=True)
