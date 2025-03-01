# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import easyocr
import os

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app)

# Initialize EasyOCR reader for English and Arabic (this might take a moment on first run)
reader = easyocr.Reader(['en', 'ar'], gpu=False)

@app.route('/ocr', methods=['POST'])
def ocr():
    """
    Accepts a POST request with an image file.
    Runs EasyOCR on the image and returns the recognized text as JSON.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        # Save file temporarily
        file_path = os.path.join("temp", file.filename)
        os.makedirs("temp", exist_ok=True)
        file.save(file_path)

        # Run EasyOCR on the saved image
        results = reader.readtext(file_path, detail=0)
        recognized_text = "\n".join(results)

        # Clean up temporary file
        os.remove(file_path)

        return jsonify({'recognized_text': recognized_text}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return "EasyOCR Backend is running!"

if __name__ == '__main__':
    # Run locally on port 5000 for testing
    app.run(host='0.0.0.0', port=5000, debug=True)
