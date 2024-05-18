#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import zipfile
from flask import Flask, request, redirect, send_file, url_for, flash, render_template,send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__))
ALLOWED_EXTENSIONS = set(['zip','xlsx','pdf','json','jpeg','png','jpg','gif','tiff','dimp','xml'])

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

            #zip extractor
            #zip_ref = zipfile.ZipFile(os.path.join(UPLOAD_FOLDER, filename), 'r')
            #zip_ref.extractall(UPLOAD_FOLDER)
            #zip_ref.close()
            return redirect(url_for('upload_file',filename=filename))
    return render_template('index.html')

@app.route('/upload_file/<filename>', methods=['GET', 'POST'])
def upload_file(filename):
    if request.method == 'POST':
        pass
    return render_template('download.html',filename=filename)

@app.route('/download_file/<filename>', methods=['GET', 'POST'])
def download_file(filename):
    if request.method == 'POST':
        pass
    return send_file(os.path.join(UPLOAD_FOLDER, filename),as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
