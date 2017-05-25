from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import json


app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return send_file("frontend/index.html")
	


@app.route("/test")
def test():
    return jsonify({"test" : "hello tester", 
        "deep":{
            "id": 1,
            "items" : [ 1,2,3,4,5],
            "obj": {
                "name": "object1",
                "description": "description of object"
            }
        }
    })    

@app.route('/results')
def getResults():
    with open('../../files/identifier_scores.json', 'r') as file:
        results = json.load(file)

    return jsonify(results)

@app.route('/runIdentifier')
def runIdentifier():

    #Making an import from the parent directory
    import sys
    from location import main
    #execute the identifier
    main.execute_identifier()

    with open('../../files/identifier_scores.json', 'r') as file:
        results = json.load(file)

    return jsonify(results)


if __name__ == "__main__":
    # app.run(host='0.0.0.0')

    app.run()