import nltk
from flask import Flask, request, jsonify
import re
from nltk.corpus import stopwords
nltk.download('stopwords')

app = Flask(__name__)

stop_words = list(nltk.corpus.stopwords.words('portuguese'))
len_SW = len(stop_words)
Vocabulary_list = []
Vocabulary_compost_list = []


@app.route("/simple_vocabulary", methods=["GET"])
def simple_vocabulary():
    return jsonify(Vocabulary_list)


@app.route("/compound_vocabulary", methods=["GET"])
def compound_vocabulary():
    return jsonify(Vocabulary_compost_list)


@app.route("/vocabulary", methods=['POST', 'GET'])
def vocabulary():
    text = request.get_data(False, True, False)
    text2 = re.split(r'[ -/:-@{-~\s]', text)
    Vocabulary_one = list(filter(None, text2))
    Vocabulary_two = []
    length = len(Vocabulary_one)
    for j in range(0, length-1):
        if not Vocabulary_one[j] or Vocabulary_one[j+1] in stop_words:
            Vocabulary_two.append(Vocabulary_one[j]+" "+Vocabulary_one[j+1])
    for n in range(0, len_SW):
        if stop_words[n] in Vocabulary_one:
            Vocabulary_one.remove(stop_words[n])
    # for n in range(0, tamanho):
    #    Vocabulary_compost = text2
    for l in range (0, len(Vocabulary_one)):
        if not Vocabulary_one[l] in Vocabulary_list:
            Vocabulary_list.append(Vocabulary_one[l])
    for m in range(0, len(Vocabulary_compost_list)):
        if not Vocabulary_two[l] in Vocabulary_compost_list:
            Vocabulary_compost_list.append(Vocabulary_one[l])
    return Vocabulary_create(200, "add new words to Vocabulary", Vocabulary_one)


def Vocabulary_create(status, message, content):
    response = {"status": status, "message": message, "Words": content}
    return jsonify(response)


app.run()
