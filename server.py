from flask import Flask, request, jsonify
import pytesseract #ocr
import cv2 #pustaka video/gambar untuk edit kontras dll
import numpy as np #membantu cv2 karena cv2 memakai array numerik(matrix)
import base64 #mengubah data gambar dari front end yang disamarkan seperti hash
from io import BytesIO #mengubah base64(biner) menjadi buffer
from PIL import Image #buka gambar dari base64(biner)

app = Flask(__name__);

@app.route('/ocr', methods=['POST'])
def ocr():
    data = request.get_json();
    image_data = data['image'].split(',')[1];
    image_bytes = base64.b64decode(image_data)

    # ubah ke format OpenCV
    img = Image.open(BytesIO(image_bytes))
    img = np.array(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # threshold
    gray = cv2.threshold(gray, 180, 225, cv2.THRESH_BINARY)[1]

    # ocr
    text = pytesseract.image_to_string(gray, lang='eng')
    return jsonify({'text' : text.strip()})

if __name__ =='__main__':
    app.run(debug=True, port=5000)

    