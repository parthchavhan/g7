from gemini_processing import process_text_with_gemini
from file_processing import process_file
from file_processing import clean_json

def process_in_chunks(txt_data, chunk_size=20):
    # Initialize results
    results = []
    txt_data = process_file(txt_data)  # Clean the raw text data

    # Process lines in chunks
    lines = txt_data.splitlines()

    while lines:
        chunk = lines[:chunk_size]  # Grab the next chunk
        lines = lines[chunk_size:]  # Remove the processed lines

        # Join the chunk into a string
        chunk_text = '\n'.join(chunk)

        # Process chunk with Gemini
        processed_data = process_text_with_gemini(chunk_text)
        processed_data = clean_json(processed_data)  # Clean after processing

        results.append(processed_data)

    return results
