from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

count = 0
rapoarte = []
registries = True
ram = True
edr = False
autopsy = True
report_generator = 'http://localhost'
analyzer = 'http://localhost'


@app.route('/rapoarte', methods=['GET'])
def handle_get_reports():
    response = requests.get(report_generator + ':5500/rapoarte')
    # print(response.json().get('reports'))
    return response.json(), 200


@app.route('/', methods=['POST'])
def handle_post():
    data = request.get_json()
    # analizam datele primite

    data = {
        "registries": True,
        "ram": True,
        "edr": False,
        "autopsy": True,
        "data": request.get_json()
    }

    analyzer_response = requests.post(analyzer + ":5750/analyze", json=data)

    # avem un raport pe care il trimitem la report generator

    report = analyzer_response.json()

    response = requests.post(report_generator + ':5500/write', json=report)

    return response.json(), 200


@app.route('/config', methods=['GET'])
def handle_get_config():
    response = {
        'registre': registries,
        'ram': ram,
        'edr': edr,
        'autopsy': autopsy
    }
    return jsonify(response), 200


@app.route('/config', methods=['POST'])
def handle_post_config():
    data = request.get_json()

    response = {'message': 'OK'}

    global registries, ram, edr, autopsy
    registries = data['registre']
    ram = data['ram']
    edr = data['edr']
    autopsy = data['autopsy']

    return response, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
