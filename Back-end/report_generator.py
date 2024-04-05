from flask import Flask, request, jsonify

app = Flask(__name__)

count = 0
rapoarte = []

@app.route('/rapoarte', methods=['GET'])
def handle_get_reports():
    response = {'message': 'This is a GET request', 'reports': rapoarte}
    return jsonify(response), 200


@app.route('/write', methods=['POST'])
def handle_post():
    data = request.get_json()

    response = {'message': 'OK'}
    global count, rapoarte
    count = count + 1
    report_name = f"Raportul {count}"
    rapoarte.append(report_name)

    return response, 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500)
