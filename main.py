from flask import Flask, request, render_template
from file_processing import clean_json
from api_helper import send_to_api
import zipfile
from io import BytesIO
from chunk_processing import process_in_chunks

app = Flask(__name__)

def process_zip_file(zip_data):
    zip_file = zipfile.ZipFile(BytesIO(zip_data), 'r')

    # Find the first .txt file in the ZIP archive
    txt_files = [file for file in zip_file.namelist() if file.endswith('.txt')]

    if not txt_files:
        raise FileNotFoundError("No .txt file found in the ZIP file")

    # Use the first .txt file
    txt_file_name = txt_files[0]

    # Extract the content of the .txt file
    with zip_file.open(txt_file_name) as txt_file:
        txt_data = txt_file.read().decode('utf-8')

    # Process the file in chunks and return results
    processed_results = process_in_chunks(txt_data)
    return processed_results

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST" and "file" in request.files:
        file = request.files["file"]
        if not file.filename.endswith(".zip"):
            return "Please upload a ZIP file"

        # Read the ZIP file into memory
        zip_data = file.read()

        # Extract and process the text file
        try:
            processed_results = process_zip_file(zip_data)
            # Combine all processed results into a single response
            final_result = '\n'.join(processed_results)
            final_result = clean_json(final_result)

            return render_template("index.html", content=final_result)
        except FileNotFoundError as e:
            return str(e)

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
