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

@app.route('/identifier/results')
def getIdentifierResults():
    with open('../../files/identifier_scores.json', 'r') as file:
        results = json.load(file)
    return jsonify(results)

@app.route('/identifier/run')
def runIdentifier():
    #Making an import from the parent directory
    from location import main
    #execute the identifier
    main.execute_identifier()

    with open('../../files/identifier_scores.json', 'r') as file:
        results = json.load(file)
        
    return jsonify(results)

@app.route('/topic/results')
def getTopicResults():
    with open('../../files/topic_scores.json', 'r') as file:
        results = json.load(file)
    return jsonify(results)




@app.route('/topic/run')
def runTopic():
    #Making an import from the parent directory
    from topic import topic_classifier
    #execute the identifier
    topic_classifier.execute()

    with open('../../files/topic_scores.json', 'r') as file:
        results = json.load(file)
        
    return jsonify(results)


# ----------- MAIN ----------- #
if __name__ == "__main__":
    # app.run(host='0.0.0.0')

    app.run()