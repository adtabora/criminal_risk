from flask import Flask, send_file

app = Flask(__name__)

@app.route("/")
def index():
    return send_file("frontend/index.html")
	
if __name__ == "__main__":
    # app.run(host='0.0.0.0')

    app.run()
    

@app.route('/prd/<path:path>')
def send_js(path):
    return send_from_directory('./frontend/', path)