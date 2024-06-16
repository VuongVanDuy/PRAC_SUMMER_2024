from flask import Flask, jsonify, request

app = Flask(__name__)

# Route đơn giản để kiểm tra API
@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify(message="Hello, World!")

# Route để xử lý dữ liệu POST
@app.route('/api/data', methods=['POST'])
def receive_data():
    data = request.json
    return jsonify(received_data=data)

if __name__ == '__main__':
    app.run(debug=True)
