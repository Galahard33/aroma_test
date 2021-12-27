import os
from flask import send_from_directory, request, url_for
from flask_ckeditor import CKEditor, upload_success, upload_fail
from app import app



@app.route('/files/<path:filename>')
def uploaded_files(filename):
    path = 'upload'
    return send_from_directory(path, filename)


@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')
    # Add more validations here
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    f.save(os.path.join('upload', f.filename))
    url = url_for('uploaded_files', filename=f.filename)
    return upload_success(url, filename=f.filename)