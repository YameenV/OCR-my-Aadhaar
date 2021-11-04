from flask import Flask, request, app, render_template, redirect
from ocrmodel import ocrHandler

import cv2
import numpy as np

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':

        if 'file' not in request.files:
            return 'No file part', redirect('/')
    
        file = request.files['file']
        npimg = np.fromfile(file, np.uint8)
        file = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        li = ocrHandler(file)
        print(li)
        return li
        
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)