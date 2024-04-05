from flask import Flask, request, jsonify

app = Flask(__name__)

count = 0
rapoarte = []
registries = True
ram = True
edr = False
autopsy = True


@app.route('/rapoarte', methods=['GET'])
def handle_get_reports():
    response = {'message': 'This is a GET request', 'reports': rapoarte}
    return jsonify(response), 200


@app.route('/', methods=['POST'])
def handle_post():
    data = request.get_json()
    # data will be analyzed using a script
    # and then a report will be generated
    response = {'message': 'OK'}
    global count, rapoarte
    count = count + 1
    report_name = f"Raportul {count}"
    rapoarte.append(report_name)

    return response, 200


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
