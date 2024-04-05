from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/analyze', methods=['POST'])
def handle_post():
    data = request.get_json()

    # analizam datele primite
    # aici va fi cea mai mare parte de analiza statica
    analyze(data)

    # generam un raport
    generate_report()
    # trimitem raportul pentru a fi stocat

    print(data)
    response = {'message': 'OK'}

    return response, 200

def analyze(data):
   print("Analizam datele primite...")
    # analizam datele primite
   print("Analiza statica a fost efectuata cu succes!")


def generate_report():
   print("Generam un raport...")
    # generam un raport
   print("Raportul a fost generat cu succes!")



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5750)
