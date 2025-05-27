from flask import Flask, request, render_template_string, send_from_directory
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part", 400
        file = request.files["file"]
        if file.filename == "":
            return "No selected file", 400
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        return f"File {file.filename} uploaded successfully!"
    
    return render_template_string('''
        <!doctype html>
        <title>Upload a File</title>
        <h1>Upload a File</h1>
        <form method=post enctype=multipart/form-data>
            <input type=file name=file>
            <input type=submit value=Upload>
        </form>
    ''')

@app.route("/files/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Azure will pass PORT in the environment
    app.run(host="0.0.0.0", port=port)
