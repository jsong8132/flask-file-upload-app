from flask import Flask, request, render_template_string
from azure.storage.blob import BlobServiceClient
import os

app = Flask(__name__)
# Get Azure connection string from environment variables or hardcode for testing (use Key Vault for production)
AZURE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
BLOB_CONTAINER = "uploads"  # your container name

blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(BLOB_CONTAINER)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part", 400
        file = request.files["file"]
        if file.filename == "":
            return "No selected file", 400
        
        # Upload to Azure Blob Storage
        blob_client = container_client.get_blob_client(file.filename)
        blob_client.upload_blob(file, overwrite=True)
        return f"File {file.filename} uploaded to Azure Blob Storage!"
    
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
