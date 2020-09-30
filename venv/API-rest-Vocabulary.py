import nltk
from flask import Flask, request, jsonify
import re
from pymongo import MongoClient
from datetime import datetime
from nltk.corpus import stopwords

nltk.download('stopwords')

app = Flask(__name__)

# mongo config
client = MongoClient('mongodb://localhost:27017/')
DataBase_History = client.test_database  # Database
Vocabulary_History = DataBase_History.test_collection  # Collections
# DataBase_History.dropDatabase()
# Voc_History = banco.Vocabulary_History

# config stop words
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


@app.route("/Len_comp_vocabulary", methods=["GET"])
def Len_comp_vocabulary():
    mensage = str("O Vocabulario composto possui " + str(len(Vocabulary_compost_list)) + " itens")
    retorno = {"status": 200, "message": mensage, "valor": len(Vocabulary_compost_list)}
    return jsonify(retorno)


@app.route("/Len_simple_vocabulary", methods=["GET"])
def Len_simple_vocabulary():
    mensage = str("O Vocabulario simples possui " + str(len(Vocabulary_list)) + " itens")
    retorno = {"status": 200, "message": mensage, "valor": len(Vocabulary_list)}
    return jsonify(retorno)


@app.route("/history", methods=["GET"])
def history():
    json_history = []
    for database_history in Vocabulary_History.find({}, {'_id': False}):
        json_history.append(database_history)
    return jsonify(json_history)


@app.route("/vocabulary", methods=['POST', 'GET'])
def vocabulary():
    text = request.get_data(False, True, False)
    text2 = re.split(r'[ -@{-~\s]', text)
    Vocabulary_one = list(filter(None, text2))
    Vocabulary_two = []
    length = len(Vocabulary_one)
    for j in range(0, length - 1):
        if not Vocabulary_one[j] in stop_words:
            if not Vocabulary_one[j + 1] in stop_words:
                Vocabulary_two.append(Vocabulary_one[j] + " " + Vocabulary_one[j + 1])
    for n in range(0, len_SW):
        if stop_words[n] in Vocabulary_one:
            Vocabulary_one.remove(stop_words[n])
    for k in range(0, len(Vocabulary_one)):
        if not Vocabulary_one[k] in Vocabulary_list:
            Vocabulary_list.append(Vocabulary_one[k])
    for m in range(0, len(Vocabulary_two)):
        if not Vocabulary_two[m] in Vocabulary_compost_list:
            Vocabulary_compost_list.append(Vocabulary_two[m])
    # datetime_now = datetime.now()  datetime_now.strftime("%m/%d/%Y, %H:%M:%S")
    Database_Vocabulary = {"data": datetime.now(), "texto inserido": text,
                           "Vocabulario simples adicionado": Vocabulary_list,
                           "Vocabulario Composto adicionado": Vocabulary_compost_list}
    insert_id_voc = Vocabulary_History.insert_one(Database_Vocabulary)
    return Vocabulary_create(200, "add new words to Vocabulary", Vocabulary_one)


def Vocabulary_create(status, message, content):
    response = {"status": status, "message": message, "Words": content}
    return jsonify(response)


app.run()
