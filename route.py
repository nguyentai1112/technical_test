''' flask app to run'''
from flask import Flask, request, jsonify
import db

APP = Flask(__name__)

OK = {'result': 'OK'}
INIT_DB_FAIL = {'result': 'initialization is not success, please check log for more info'}
ERROR_VALIDATE = {"Error": "input UUID and score is the number from 0 to 5"}
ERROR_GET_DATA = {"Error": "Can not get data from database"}
ERROR_INSERT_DATA = {"Error": "Can not insert into database"}


@APP.route('/', methods=['GET'])
def home():
    ''' default page, just print out the message of this excecise'''

    return "<h1>Inspectorio - Technical Test </h1>" \
           "<p>This site is a technical test for data engineer position in Inspectorio </p>"


@APP.route('/api/init_db', methods=['GET'])
def init_db():
    ''' call init database

        Returns:
            Json : The return value. OK if success, Error message otherwise
    '''

    success = db.init_db()
    if not success:
        return INIT_DB_FAIL

    return jsonify(OK)


@APP.route("/api/push", methods=["POST"])
def push():
    ''' API receives product data, the app processes data and return the mean of that product

        Example to run pushing data on localhost:
            curl -X POST \
          http://localhost:5000/api/push \
          -H 'content-type: application/json' \
          -d '{  "UUID": "a2-b3", "score": 5  }'

        Returns:
            Json : The return value. new mean value of product if success,
                    error json message otherwise
    '''
    req = request.get_json()
    product_id = req['UUID']
    score = req['score']
    validated = db.validate(product_id, score)
    if not validated:
        return ERROR_VALIDATE

    data = db.update_and_get_stat(product_id, score)

    if not data:
        return ERROR_GET_DATA

    res = {'UUID': data[0], 'mean': data[1]}
    return res


if __name__ == '__main__':
    APP.run(debug=False)
