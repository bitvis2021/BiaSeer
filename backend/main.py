from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from gaindata.dataprocess import mediaDataSet, mediaMatrixDataSet, getConnectedComponent, concatMediaDiff
import json
from utils.helper import readJsontoDict
from keywordExtract.test import test
from keywordExtract.storytree import getStoryTreedata
import numpy as np

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

@app.route('/media_concat_diff', methods=['GET'])
@cross_origin()
def getMediaConcatDiffDataSet():
    args_dict = request.args
    print('args_dict1', args_dict)
    mSrc_list = args_dict.getlist('mSrc_list[]')
    print('msrc_list', mSrc_list)
    # print(mSrc_list)
    data = None
    if len(mSrc_list) > 1:
        data = concatMediaDiff(mSrc_list)
    return {'data': data}

@app.route('/concat_connected_component', methods=['GET'])
@cross_origin()
def getMediaConcatConCom():
    args_dict = request.args
    print('args_dict ', args_dict)
    matrix = [[None for _ in range(44)] for _ in range(20)]
    for i in range (20):
        for j in range (44):
            matrix[i][j] = args_dict.get('matrix['+str(i)+']'+'['+str(j)+']')
    matrix = np.array(matrix)
    # matrix = args_dict.get('matrix['+)

    print('multi_array', matrix)
    data = None
    if len(matrix) > 1:
        data = getConnectedComponent(matrix)
    return {'data': data}


@app.route('/media_matrix_stroytree', methods=['GET'])
@cross_origin()
def getMediaMatrixStoryTreeDataSet():
    args_dict = request.args
    topics = args_dict.getlist('topics[]')
    date_index = args_dict.getlist('date_index[]')
    date = args_dict.getlist('date[]')
    mSrc_list = args_dict.getlist('mSrc_list[]')
    
    print(topics)
    print(date_index)
    print(date)
    print(mSrc_list)

    date_index.sort()

    binDict = readJsontoDict("binDict.json")
    time_scope = [binDict[str(date_index[0])][0], binDict[str(date_index[-1])][-1]]

    # mSrc_list = ["msn.com", "bbc.com"]
    # time_scope = ["2022-02-01","2022-02-21"]
    country_list = ["ALL"]
    # classnum = '["3","4"]'
    classnum = topics
    time_scope = [binDict[str(date_index[0])][0], binDict[str(date_index[-1])][-1]]

    testdata = getStoryTreedata(time_scope,mSrc_list,classnum,country_list)
    # testdata = readJsontoDict("./tree_pro.json")
    return {'data': testdata}

if __name__ == "__main__":
    print('run 0.0.0.0:14449')
    app.run(host='0.0.0.0', port=14449)

