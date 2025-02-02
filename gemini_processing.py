import google.generativeai as genai
import json
from vehicle_data import VEHICLE_DATA
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the API key




def process_text_with_gemini(text):
    """Sends the cleaned text to Gemini AI for extraction."""

    api_key = os.getenv('hui_hui')
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    # Prompt for extracting details
    prompt = f""" take your time and dont miss anything read the data correctly and try not to make any errors
        one more thing 
    The input contains chat messages related to logistics and transport. For each message, extract the following details in json format :
    - pickup_address (if possible write in english use translator cant be null)
    - drop_address (if possible write in english use translator cant be null)
    - vehicle_name (if not giver use "Brokers" cant be null)
    - vehicle_id (fron the json data)
    - vehicle_type (T by default)
    - vehicle_info (same as vehicle name)
    - vehicle_range (fron the json data)
    - vehicle_fee (fron the json data)
    - pickup_city
    - drop_city
    - part_full_load (full by default)
    - no_of_vehicles (1 by default)
    - contact_mobile (take only 1 phone number cant be null)
    - vehicles_needed ( the vehicle is required or its available by default required)
    if pickup_address, drop_address or contact_mobile any one of them is missing is null or not specified dont add that data
    If any vehicle-related detail is missing, supplement it using the following JSON data:
    {json.dumps(VEHICLE_DATA, indent=4)}
    be sure i want no data with null dont add that data that has things missing 

    Input: {text}
    """

    response = model.generate_content(prompt)
    return response.text.strip()
