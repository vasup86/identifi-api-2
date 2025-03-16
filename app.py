
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import os

from payments import sendPayment

app = Flask(__name__)

CORS(app)

@app.route('/send-payment', methods=['POST'])
@cross_origin()
def sendPaymentEndPoint():
    try:
        senderUsername = request.json['senderUsername']
        receiverUsername = request.json['receiverUsername']
        amount = request.json['amount']

        sendPayment(senderUsername, receiverUsername, amount)


        return jsonify({"result":"connected"})
    except:
        return jsonify({"result":"failed"})



@app.route('/')
def homepage():
    return jsonify({"result":"connected"})

if __name__ == '__main__':
    app.run()
