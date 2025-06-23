from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os
from resume_parser import extract_resume_text
from job_matcher import compare_resume_with_job

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'resume' not in request.files or 'jobdesc' not in request.form:
            return 'Missing resume or job description.'

        file = request.files['resume']
        jobdesc = request.form['jobdesc']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            resume_text = extract_resume_text(filepath)
            result = compare_resume_with_job(resume_text, jobdesc)

            return render_template('index.html', result=result)

    return render_template('index.html', result=None)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
