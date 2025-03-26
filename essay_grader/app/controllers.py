#from flask import Blueprint, render_template, request
#from .models import grade_essay
#import os

#main = Blueprint('main', __name__)

#@main.route('/', methods=['GET', 'POST'])
#def upload_file():
    # if request.method == 'POST':
    #     file = request.files['document']
    #     year = request.form.get('year')
        
    #     if file and year:
    #         filepath = os.path.join('uploads', file.filename)
    #         file.save(filepath)

    #         result = grade_essay(filepath, year)
    #         return render_template('upload.html', result=result)

    # return render_template('upload.html')

from flask import Blueprint, render_template, request
from .modules_BERT import grade_BERT_essay, extract_text
from .models import grade_LSTM_essay
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

            text = extract_text(filepath)
            resultLSTM = grade_LSTM_essay(filepath, year)
            resultBERT = grade_BERT_essay(text, year)
            result = f"{resultLSTM} \n {resultBERT}"
            return render_template('upload.html', result=result)

    return render_template('upload.html')
