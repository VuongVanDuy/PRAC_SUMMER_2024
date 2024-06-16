from flask import Flask, request, jsonify, abort
import os
import json
from jsonschema import validate, ValidationError

app = Flask(__name__)
UPLOAD_FOLDER = './data'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def check_token(token):
    valid_tokens = ["token1", "token2", "token3"]
    return token in valid_tokens

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return jsonify({"error": "No file part in the request"}), 400
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({"error": "No file selected for uploading"}), 400
#     file.save(os.path.join(UPLOAD_FOLDER, file.filename))
#     return jsonify({"message": f"File {file.filename} has been uploaded successfully"}), 201

# @app.route('/upload-all', methods=['POST'])
# def upload_all_files():
#     if 'files' not in request.files:
#         return jsonify({"error": "No files part in the request"}), 400
#     files = request.files.getlist('files')
#     for file in files:
#         if file.filename == '':
#             return jsonify({"error": "One of the files has no filename"}), 400
#         file.save(os.path.join(UPLOAD_FOLDER, file.filename))
#     return jsonify({"message": f"{len(files)} files have been uploaded successfully"}), 201

@app.route('/data-route/<direction>/<routeId>', methods=['GET'])
def list_files(direction, routeId):
    token = request.headers.get('Authorization')

    if not token or not check_token(token):
        return abort(401, description="Unauthorized access")

    path_files = f'{UPLOAD_FOLDER}/direction_{direction}/{routeId}.json'
    try:
        with open(path_files, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return jsonify(data)
    except FileNotFoundError:
        return abort(404, description="File not found")

data_schema_user = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "username": {"type": "string"},
        "password": {"type": "string"},
        "link_icon": {"type": "string"}
    },
    "required": ["id", "username", "password", "link_icon"]
}

@app.route('/data-user', methods=['POST'])
def add_data_user():
    token = request.headers.get('Authorization')

    if not token or not check_token(token):
        return abort(401, description="Unauthorized access")
    
    # kiểm tra tính hợp lệ của dữ liệu được post lên
    try:
        new_data = request.get_json()
        validate(instance=new_data, schema=data_schema)
    except ValidationError as ve:
        return abort(401, description=f"Invalid data: {ve.message}")
    except Exception as e:
        return abort(401, description="Invalid JSON data")

    new_data = request.get_json()
    path_files = f'{UPLOAD_FOLDER}/404.json'
    
    try:
        with open(path_files, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"result": [], "success": True}

    # Thêm dữ liệu mới vào danh sách trong 'result'
    data['result'].append(new_data)

    try:
        with open(path_files, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
        return jsonify({"message": "Data saved successfully"}), 201
    except Exception as e:
        return abort(500, description=str(e))

@app.route('/data-review-user', methods=['POST'])
def add_data_review_user():
    token = request.headers.get('Authorization')

    if not token or not check_token(token):
        return abort(401, description="Unauthorized access")
    
    # kiểm tra tính hợp lệ của dữ liệu được post lên
    try:
        new_data = request.get_json()
        validate(instance=new_data, schema=data_schema)
    except ValidationError as ve:
        return abort(401, description=f"Invalid data: {ve.message}")
    except Exception as e:
        return abort(401, description="Invalid JSON data")

    new_data = request.get_json()
    path_files = f'{UPLOAD_FOLDER}/404.json'
    
    try:
        with open(path_files, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"result": [], "success": True}

    # Thêm dữ liệu mới vào danh sách trong 'result'
    data['result'].append(new_data)

    try:
        with open(path_files, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
        return jsonify({"message": "Data saved successfully"}), 201
    except Exception as e:
        return abort(500, description=str(e))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
