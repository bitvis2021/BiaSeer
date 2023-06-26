from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from gaindata.dataprocess import fuctionA, mediaDataSet

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

if __name__ == "__main__":
    print('run 0.0.0.0:14449')
    app.run(host='0.0.0.0', port=14449)

