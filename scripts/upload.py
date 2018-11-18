import os
from flask import Flask, jsonify, flash, request, redirect, url_for, render_template
import requests 
import sys
from werkzeug.utils import secure_filename
import ocr_script

UPLOAD_FOLDER = '/Users/shravanc/flask/file_upload'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print('Request paramter', request.files)
        print('Request paramter', request.files['file'])
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_path = app.config['UPLOAD_FOLDER'] + "/" + file.filename
            json_resp = ocr_script.mainFun(file_path)
            return jsonify(json_resp)
            #return redirect(url_for('upload_file',
            #                        filename=filename))

    return render_template('upload_template.html')

"""
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
"""



@app.route('/hello')
def hello_world():
    return jsonify(hello="hello world json")

@app.route('/form-example', methods=['GET', 'POST']) #allow both GET and POST requests
def form_example():
    if request.method == 'POST':  #this block is only entered when the form is submitted
        language = request.form.get('language')
        framework = request.form['framework']

        return '''<h1>The language value is: {}</h1>
                  <h1>The framework value is: {}</h1>'''.format(language, framework)

    return '''<form method="POST">
                  Language: <input type="text" name="language"><br>
                  Framework: <input type="text" name="framework"><br>
                  <input type="submit" value="Submit"><br>
              </form>'''

@app.route('/google', methods=['GET'])
def google_it():
    print('This error output', 100 + 100)
    r = requests.get('https://jsonplaceholder.typicode.com/users/')
    print('This error output', r)
    jsons_resp = r.json()
    print('This error output', jsons_resp[0]['id'])
    return r.text
