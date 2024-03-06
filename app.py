from flask import Flask , jsonify

import time

app = Flask (__name__)

@app.route('/')

def get_message():
    timestamp = time.strftime('%m%Y')
    message ='stanley maina'
    return jsonify ({"message": message , "timestamp":timestamp})

if __name__ == '__main__':
    app.run(debug =True)
