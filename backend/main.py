from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from gaindata.dataprocess import mediaDataSet, mediaMatrixDataSet
import json
from utils.helper import readJsontoDict

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADER'] = 'Content-Type'


@app.route('/media_dataset', methods=['GET'])
@cross_origin()
def getMediaDataSet():
    data = mediaDataSet()
    # print(data)
    # args_dict = request.args
    # args_dict.to_dict()['mediatopData[]']
    return {'data': data}


@app.route('/media_matrix_dataset', methods=['GET'])
@cross_origin()
def getMediaMatrixDataSet():
    data = mediaMatrixDataSet()
    return {'data': data}

@app.route('/media_matrix_stroytree', methods=['GET'])
@cross_origin()
def getMediaMatrixStoryTreeDataSet():
    args_dict = request.args
    topics = args_dict.getlist('topics[]')
    date_index = args_dict.getlist('date_index[]')
    date = args_dict.getlist('date[]')
    print(topics)
    print(date_index)
    print(date)
    testdata = readJsontoDict("./tree_pro.json")
    # print(testdata)
    return {'data': testdata}

if __name__ == "__main__":
    print('run 0.0.0.0:14449')
    app.run(host='0.0.0.0', port=14449)

