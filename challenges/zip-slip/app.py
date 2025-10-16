from flask import Flask, request, redirect, url_for
import zipfile, os

app = Flask(__name__)
UPLOAD = 'uploads'
PUBLIC = 'static'
os.makedirs(UPLOAD, exist_ok=True)
os.makedirs(PUBLIC, exist_ok=True)

@app.route('/', methods=['GET'])
def index():
    return '''
    <form action="/upload" method="post" enctype="multipart/form-data">
      <input type="file" name="archive">
      <input type="submit" value="Upload">
    </form>
    '''

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('archive')
    if not f:
        return "No file", 400
    path = os.path.join(UPLOAD, f.filename)
    f.save(path)
    # vulnérable : extraction sans nettoyage -> Zip Slip
    with zipfile.ZipFile(path, 'r') as z:
        for member in z.namelist():
            z.extract(member, PUBLIC)   # insecure
    return "Extracted. Browse /static/"

if __name__ == '__main__':
    # place the flag in a protected location that can be written by zip extraction
    with open(os.path.join(PUBLIC,'flag_upload.txt'),'w') as fh:
        fh.write('PLACEHOLDER_NOT_USED')
    app.run(host='0.0.0.0', port=5002)
