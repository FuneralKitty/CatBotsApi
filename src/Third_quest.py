from flask import Flask

app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    return "Cats Service. Version 0.1", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)