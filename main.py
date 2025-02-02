import re
from flask import Flask, request, render_template
import os
import json
import zipfile
from file_processing import process_file
from file_processing import clean_json
import requests
from gemini_processing import process_text_with_gemini

app = Flask(__name__)

# Define folders
UPLOAD_FOLDER = "uploads"
EXTRACT_FOLDER = "extracted"

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXTRACT_FOLDER, exist_ok=True)

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
def process_in_chunks(txt_path, chunk_size=150):
    # Open file and read lines
    with open(txt_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Initialize results
    results = []

    # Process lines in chunks
    while lines:
        # Read the next chunk
        chunk = lines[:chunk_size]
        lines = lines[chunk_size:]  # Remove the processed lines

        # Join the chunk into a string
        chunk_text = ''.join(chunk)

        # Process chunk with Gemini
        processed_data = process_text_with_gemini(chunk_text)
        processed_data=clean_json(processed_data)

        # Store processed result
        results.append(processed_data)

        # Optionally, you can delete the processed lines from the file
        with open(txt_path, "w", encoding="utf-8") as file:
            file.writelines(lines)

    return results

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST" and "file" in request.files:
        if "file" not in request.files:
            return "No file part"

        file = request.files["file"]
        if file.filename == "":
            return "No selected file"

        if not file.filename.endswith(".zip"):
            return "Please upload a ZIP file"

        # Save uploaded ZIP
        zip_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(zip_path)

        # Extract ZIP
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(EXTRACT_FOLDER)

        txt_path = os.path.join(EXTRACT_FOLDER, "_chat.txt")

        if not os.path.exists(txt_path):
            return "No _chat.txt found in the ZIP file"

        # Clean the extracted file
        process_file(txt_path)

        # Process the file in chunks
        processed_results = process_in_chunks(txt_path)

        # Remove files after processing
        os.remove(txt_path)
        os.remove(zip_path)

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
