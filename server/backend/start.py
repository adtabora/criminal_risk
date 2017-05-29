from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import json

import pandas as pd


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

# ----------- Article Explorer ----------- #

@app.route('/topic/list')
def listTopicArticles():
    filter_dataset = request.args["dataset"]
    #Filters: True Positive, False Positive, True Negative, False Negative
    filter_tp = request.args["tp"]
    filter_fp = request.args["fp"]
    filter_tn = request.args["tn"]
    filter_fn = request.args["fn"]

    #read the csv
    classified_df = pd.read_csv("../../files/documents_classified.csv")
    #filter by dataset
    classified_df = classified_df[classified_df["data_set"] == filter_dataset ]
    
    
    # create a list depending on the filter flags
    articles_list = pd.DataFrame(columns=["art_id"])

    if filter_tp == "true":
        conditions = (classified_df["gold"] == "Criminal") & (classified_df["pred"] == "Criminal")
        articles_list = pd.concat([articles_list, classified_df[conditions]])
    if filter_fn== "true":
        conditions = (classified_df["gold"] == "Criminal") & (classified_df["pred"] == "Other")
        articles_list = pd.concat([articles_list, classified_df[conditions]])
    if filter_fp== "true":
        conditions = (classified_df["gold"] == "Other") & (classified_df["pred"] == "Criminal")
        articles_list = pd.concat([articles_list, classified_df[conditions]])
    if filter_tn== "true":
        conditions = (classified_df["gold"] == "Other") & (classified_df["pred"] == "Other")
        articles_list = pd.concat([articles_list, classified_df[conditions]])

    # prepare the response
    count = classified_df.shape[0]
    data = [{"id": artid, "title": "Article "+str(int(artid)) } for artid in articles_list.art_id.values]
    
    return jsonify({
        "count": count,
        "data": data
    })

@app.route('/entity/list')
def listEntityArticles():
    filter_dataset = request.args["dataset"]
    #read the csv
    classified_df = pd.read_csv("../../files/words_classified.csv")
    #filter by dataset
    classified_df = classified_df[classified_df["dataset"] == filter_dataset ]

    count = classified_df.shape[0]
    data = [{"id": artid, "title": "Article "+str(int(artid)) } for artid in classified_df.art_id.unique()]

    return jsonify({
        "count": count,
        "data": data
    })

@app.route("/topic/get/<id>")
def getTopicArticle(id):
    #read the csv
    classified_df = pd.read_csv("../../files/documents_classified.csv")
    documents_df = pd.read_csv("../../files/documents.csv")

    document = documents_df[documents_df["id"]==int(id)].iloc[0]
    categories = classified_df[classified_df["art_id"]==int(id)][["gold","pred"]].iloc[0]

    return jsonify({
        "art_id": document.id,
        "title": document.title,
        "gold": categories.gold,
        "pred": categories.pred,
        #array of sentences with chunks.. fn is just to signal the ui to not color that chunk
        "sentences": [[[ document.content, "fn"]]]  
    })


@app.route("/entity/get/<id>")
def getEntityArticle(id):
    #read the csv
    classified_df = pd.read_csv("../../files/words_classified.csv")
    documents_df = pd.read_csv("../../files/documents.csv")

    document = documents_df[documents_df["id"]==int(id)].iloc[0]
    article_words = classified_df[classified_df["art_id"]==int(id)]


    print "- Confucius analysis"
    #TP
    conditions = (article_words["iob_tag"].isin(["B-Loc","I-Loc"])) & (article_words["pred"].isin(["B-Loc","I-Loc"]))
    article_words.at[conditions,"conf"] = "tp"
    #FP
    conditions = (article_words["iob_tag"].isin(["none"])) & (article_words["pred"].isin(["B-Loc","I-Loc"]))
    article_words.at[conditions,"conf"] = "fp"
    #TN
    conditions = (article_words["iob_tag"].isin(["none"])) & (article_words["pred"].isin(["none"]))
    article_words.at[conditions,"conf"] = "tn"
    #FN
    conditions = (article_words["iob_tag"].isin(["B-Loc","I-Loc"])) & (article_words["pred"].isin(["none"]))
    article_words.at[conditions,"conf"] = "fn"


    # Brackets
    print "- Brackets"
    article_words = article_words.sort_values(by=["art_id","sent_id","pos"] )
    article_words.loc[:,"bracket"] = ["none"] * article_words.shape[0]

    begin_bracket = 0
    error = False
    last_iob = "none"
    last_sent = -1

    for index, art_word in article_words.iterrows():
        #reset last_iob when initiating a new sentence
        # if last_sent != art_word.cs_id:
        #     last_iob = "none"
        print "last sent %i" %last_sent
        # process the word
        if art_word.iob_tag == "B-Loc":
            print "-- Begin word"
            print art_word.word
            begin_bracket = index
        elif art_word.iob_tag == "none" and last_iob in ["I-Loc","B-Loc"]:
            print "-- end bracket"
            print art_word.word
            if error:
                article_words.loc[begin_bracket,"bracket"] = "begin-red"
                article_words.loc[index,"bracket"] = "end-red"
            else:
                article_words.loc[begin_bracket,"bracket"] = "begin-green"
                article_words.loc[index,"bracket"] = "end-green"
            error = False
            begin_bracket = 0
        # see if there's an error
        if art_word.iob_tag in ["I-Loc","B-Loc"] and art_word.pred == "none":
            error = True

        #set last iob and last sentence id before iterating
        last_iob = art_word.iob_tag
        last_sent = art_word.cs_id

    
    # combine words into chunks and in sentences
    print "- chunking"
    sentences = []
    for sent_id in article_words.sent_id.unique():
        sentence = []
        for index, word in article_words[article_words["sent_id"] == sent_id].iterrows():
            if len(sentence)==0 or sentence[-1][1] != word.conf:
                sentence.append([word.word, word.conf, word.bracket, word.iob_tag, word.pred])
            elif sentence[-1][1] == word.conf:
                sentence[-1][0] += " " + word.word 
                sentence[-1][3] += ", " + word.iob_tag 
                sentence[-1][4] += ", " + word.pred 
        sentences.append(sentence)
            
    # return the values
    return jsonify( sentences )


    

# ----------- MAIN ----------- #
if __name__ == "__main__":
    # app.run(host='0.0.0.0')

    app.run()