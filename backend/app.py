from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.imagerec import img_detect_items
from ai import process_user_input
import os
import tempfile


app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure upload folder exists

@app.route("/upload", methods=["POST"])
def upload_file():
    if "image" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    return jsonify({"message": "File uploaded successfully", "file_path": file_path})


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get("message")

    if not user_input:
        return jsonify({"error": "Message is required"}), 400

    # Call the processing function from ai.py
    response = process_user_input(user_input)

    return jsonify({"response": response})

@app.route('/api/upload-photo', methods=['POST'])
def upload_photo():
    data = request.json
    photo_data_url = data.get('photo')

    if not photo_data_url:
        return jsonify({"error": "No photo data provided"}), 400

    import base64
    header, encoded = photo_data_url.split(",", 1)
    binary_data = base64.b64decode(encoded)
    mime_type = header.split(";", 1)[0].removeprefix("data:")

    try:
        with tempfile.NamedTemporaryFile(suffix=".png") as image:
            image.write(binary_data)
            image.flush()
            detected_items = img_detect_items(image.name, mime_type=mime_type)
        return jsonify({"detected_items": detected_items})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
