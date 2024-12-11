from flask import Flask, request, jsonify, render_template
import pytesseract
from PIL import Image

app = Flask(__name__, template_folder='templates') # Specify template folder explicitly

# Configure Tesseract path for Ubuntu
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400

    image = request.files['image']
    if image.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        img = Image.open(image)
        text = pytesseract.image_to_string(img)
        return jsonify({'text': text}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)