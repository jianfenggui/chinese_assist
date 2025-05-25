import argparse
import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import google.generativeai as genai
from PIL import Image

app = Flask(__name__, static_url_path='/static', static_folder='static')

# Configure Gemini API Key
try:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
except AttributeError as e:
    print(f"Error configuring Gemini API: {e}")
    print("WARNING: GOOGLE_API_KEY environment variable not set or google.generativeai is not correctly initialized.")

if not os.environ.get("GOOGLE_API_KEY"):
    print("WARNING: GOOGLE_API_KEY environment variable not set.")

vocabulary_list = []

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vocabulary', methods=['GET', 'POST'])
def vocabulary():
    if request.method == 'POST':
        words_string = request.form.get('words', '')
        if words_string:
            new_words = words_string.strip().split()
            for word in new_words:
                if word not in vocabulary_list: # Avoid duplicates
                    vocabulary_list.append(word)
        return redirect(url_for('vocabulary'))
    return render_template('vocabulary.html', words=vocabulary_list)

@app.route('/reading')
def reading():
    return render_template('reading.html')

@app.route('/classical')
def classical():
    return render_template('classical.html')

@app.route('/recognize_image_with_gemini', methods=['POST'])
def recognize_image_with_gemini():
    if 'image_file' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image_file']

    if image_file.filename == '':
        return jsonify({"error": "No image selected"}), 400

    if image_file and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename) # Secure the filename
        image_bytes = image_file.read()

        try:
            model = genai.GenerativeModel('gemini-pro-vision') # Or the latest recommended vision model
            
            image_parts = [
                {
                    "mime_type": image_file.mimetype, # e.g., "image/jpeg" or "image/png"
                    "data": image_bytes
                }
            ]
            
            prompt_parts = ["请识别图片中的所有手写词汇，并将它们用空格分隔列出。"] # Instruct Gemini to identify handwritten words and list them

            # Make the API call
            response = model.generate_content([*prompt_parts, *image_parts])
            
            # Debugging: Print the raw response
            print("Gemini API Response Text:", response.text)
            # print("Gemini API Response Parts:", response.parts) # Uncomment for more detailed debugging

            # Extract the recognized text
            recognized_text = response.text.strip()
            
            return jsonify({"recognized_text": recognized_text})

        except Exception as e: # Catch potential exceptions during API interaction
            print(f"Gemini API request failed: {e}") # Debugging: Print exception details
            return jsonify({"error": "Gemini API request failed", "details": str(e)}), 500
    else:
        return jsonify({"error": "File type not allowed"}), 400

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the Flask app.')
    parser.add_argument('-p', '--port', type=int, default=8089,
                        help='port number to listen on')
    args = parser.parse_args()
    app.run(debug=True, host='0.0.0.0', port=args.port)
