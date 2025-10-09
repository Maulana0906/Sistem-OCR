from flask import Flask, request, jsonify, render_template, send_file
import pytesseract #ocr
import cv2 #pustaka video/gambar untuk edit kontras dll
import numpy as np #membantu cv2 karena cv2 memakai array numerik(matrix)
import base64 #mengubah data gambar dari front end yang disamarkan seperti hash
from io import BytesIO #mengubah base64(biner) menjadi buffer
from PIL import Image #buka gambar dari base64(biner)
from flask_cors import CORS
from gtts import gTTS


app = Flask(__name__);
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ocr', methods=['POST'])
def ocr():
    data = request.get_json();
    image_data = data['image'].split(',')[1];
    image_bytes = base64.b64decode(image_data)

    # ubah ke format OpenCV
    img = Image.open(BytesIO(image_bytes))
    img = np.array(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # ocr   
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    text = pytesseract.image_to_string(gray, lang='eng')

    tts = gTTS(text, lang='id')
    filename = 'speech.mp3'
    tts.save(filename)
    return send_file(filename, mimetype='audio/mpeg')

if __name__ =='__main__':
    app.run(debug=True, port=5000)

    