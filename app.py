from flask import Flask, request, send_from_directory, jsonify, render_template
import os
import glob

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_folder='images')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/image")
def image():
    newest = max(glob.iglob('images/*'), key=os.path.getctime)
    print(newest)
    current_image = {"path": newest}
    return jsonify(current_image)

if __name__ == "__main__":
    app.run()