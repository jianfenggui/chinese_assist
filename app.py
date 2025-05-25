import argparse
import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from google import genai
from PIL import Image

app = Flask(__name__, static_url_path='/static', static_folder='static')

# Configure Gemini API Key
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY") or "AIzaSyBiPSZpw3anpuGCQ4OHJIFt3OokmG22RG4"
if not GOOGLE_API_KEY:
    print("WARNING: GOOGLE_API_KEY environment variable not set.")
client = genai.Client(api_key=GOOGLE_API_KEY)

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
            from google.genai import types
            print(f"[DEBUG] image_file.mimetype: {image_file.mimetype}")
            print(f"[DEBUG] image_file.filename: {image_file.filename}")
            print(f"[DEBUG] image_bytes type: {type(image_bytes)}, length: {len(image_bytes)}")
            # 构造内容，包含文本和图片
            try:
                text_part = types.Part.from_text(text="请识别图片中的所有手写词汇，并将它们用空格分隔列出。")
            except Exception as e:
                print(f"[DEBUG] types.Part.from_text error: {e}")
                raise
            try:
                image_part = types.Part.from_bytes(data=image_bytes, mime_type=image_file.mimetype)
            except Exception as e:
                print(f"[DEBUG] types.Part.from_data error: {e}")
                raise
            # 按官方建议，图片在前，文本在后
            contents = [image_part, text_part]
            print(f"[DEBUG] contents: {contents}")
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=contents
                )
            except Exception as e:
                print(f"[DEBUG] client.models.generate_content error: {e}")
                raise
            print("[DEBUG] Gemini API Response Object:", response)
            print("[DEBUG] Gemini API Response Text:", getattr(response, 'text', None))
            recognized_text = getattr(response, 'text', '').strip()
            return jsonify({"recognized_text": recognized_text})
        except Exception as e: # Catch potential exceptions during API interaction
            import traceback
            print(f"Gemini API request failed: {e}") # Debugging: Print exception details
            traceback.print_exc()
            return jsonify({"error": "Gemini API request failed", "details": str(e)}), 500
    else:
        return jsonify({"error": "File type not allowed"}), 400

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the Flask app.')
    parser.add_argument('-p', '--port', type=int, default=8089,
                        help='port number to listen on')
    args = parser.parse_args()
    app.run(debug=True, host='0.0.0.0', port=args.port)
