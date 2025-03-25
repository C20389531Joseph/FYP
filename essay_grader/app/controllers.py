from flask import Blueprint, render_template, request
from .models import grade_essay
import os

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['document']
        year = request.form.get('year')
        
        if file and year:
            filepath = os.path.join('uploads', file.filename)
            file.save(filepath)

            result = grade_essay(filepath, year)
            return render_template('upload.html', result=result)

    return render_template('upload.html')
