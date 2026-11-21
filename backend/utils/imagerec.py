import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)

def upload_to_gemini(path, mime_type=None):
  """Uploads the given file to Gemini.

  See https://ai.google.dev/gemini-api/docs/prompting_with_media
  """
  file = genai.upload_file(path, mime_type=mime_type)
  # print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash-exp",
  generation_config=generation_config,
  system_instruction='''You are an expert product analyzer. 
  Your task is to analyze the image of one or more food-related items and provide the specific product name, such as "rice" or "yoghurt" in csv format.
  
  The final csv should contain a comma between every 2 items.
  ensure the csv has no spaces before and after the commas.
  If the item is not recognized, ignore the item.
  '''
)

def img_detect_items(img_path, mime_type="image/jpeg"):
    
    # You may need to update the file paths
    files = [
    upload_to_gemini(img_path, mime_type=mime_type),
    ]

    chat_session = model.start_chat(
    history=[
        {
        "role": "user",
        "parts": [
            files[0],
        ],
        },
    ]
    )

    response = chat_session.send_message("Answer")

    raw = response.text.split(",")

    # Remove duplicates by converting to a set and back to a list
    unique_items = list(set(raw))

    # Join the list back into a comma-separated string
    result_string = ",".join(sorted(unique_items))
    return result_string
