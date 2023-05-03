from flask import Flask, jsonify, request
import scripts.similarity as similarity

similarity.load()

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():

    return app.send_static_file('main.html')

@app.route('/getData')
def getData(methods = ['GET']):

    params = request.args

    return similarity.findTopMatches(params['data'])

if(__name__ == '__main__'):

    app.run(debug=True)