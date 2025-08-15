from flask import Flask, request, jsonify, send_from_directory, Response
import os
from flask_cors import CORS
from message_types import mt1, mt2, mt3, mt4, mt5, mt6, mt7, mt9, mt10, mt12, mt17, mt18, mt24, mt25, mt26, mt27, mt28 

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_BUILD_DIR = os.path.normpath(os.path.join(BASE_DIR, '..', 'frontend', 'build'))

# Flask setup
app = Flask(
    __name__,
    static_folder=FRONTEND_BUILD_DIR,
    static_url_path='/'
)

# Enable CORS globally
CORS(app)

# Serve frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    full_path = os.path.join(FRONTEND_BUILD_DIR, path)
    if path != '' and os.path.exists(full_path):
        return send_from_directory(FRONTEND_BUILD_DIR, path)
    else:
        return send_from_directory(FRONTEND_BUILD_DIR, 'index.html')


def _send_result(result):
    # If message_types returned a Flask Response or (Response, status), pass through
    if isinstance(result, Response):
        return result
    if isinstance(result, tuple) and len(result) >= 1 and isinstance(result[0], Response):
        return result
    # If a plain string (expected hex), wrap in JSON
    if isinstance(result, str):
        return jsonify({'hex_string': result})
    # Unexpected
    return jsonify({'error': 'Unexpected backend return type'}), 500

# API Endpoint
@app.route('/api/numbers/1', methods=['POST'])
def process_numbers_1():
    try:
        return _send_result(mt1(request))
    except Exception as e:
        print(f"Server error: {str(e)}")
        return jsonify({'error': 'Internal server error.'}), 500

@app.route('/api/numbers/2', methods=['POST'])
def process_numbers_2():
    try:
        return _send_result(mt2(request))
    except Exception as e:
        print(f"Server error: {str(e)}")
        return jsonify({'error': 'Internal server error.'}), 500
    
@app.route('/api/numbers/3', methods=['POST'])
def process_numbers_3():
    try:
        return _send_result(mt3(request))
    except Exception as e:
        print(f"Server error: {str(e)}")
        return jsonify({'error': 'Internal server error.'}), 500

@app.route('/api/numbers/4', methods=['POST'])
def process_numbers_4():
    try:
        return _send_result(mt4(request))
    except Exception as e:
        print(f"Server error: {str(e)}")
        return jsonify({'error': 'Internal server error.'}), 500

@app.route('/api/numbers/5', methods=['POST'])
def process_numbers_5():
    try:
        return _send_result(mt5(request))
    except Exception as e:
        print(f"Server error: {str(e)}")
        return jsonify({'error': 'Internal server error.'}), 500

@app.route('/api/numbers/6', methods=['POST'])
def process_numbers_6():
    try:
        return _send_result(mt6(request))
    except Exception as e:
        print(f"Server error: {str(e)}")
        return jsonify({'error': 'Internal server error.'}), 500

@app.route('/api/numbers/7', methods=['POST'])
def process_numbers_7():
    try:
        return _send_result(mt7(request))
    except Exception as e:
        print(f"Server error: {str(e)}")
        return jsonify({'error': 'Internal server error.'}), 500

@app.route('/api/numbers/9', methods=['POST'])
def process_numbers_9():
    try:
        return _send_result(mt9(request))
    except Exception as e:
        print(f"Server error: {str(e)}")
        return jsonify({'error': 'Internal server error.'}), 500

@app.route('/api/numbers/10', methods=['POST'])
def process_numbers_10():
    try:
        return _send_result(mt10(request))
    except Exception as e:
        print(f"Server error: {str(e)}")
        return jsonify({'error': 'Internal server error.'}), 500

@app.route('/api/numbers/12', methods=['POST'])
def process_numbers_12():
    try:
        return _send_result(mt12(request))
    except Exception as e:
        print(f"Server error: {str(e)}")
        return jsonify({'error': 'Internal server error.'}), 500

@app.route('/api/numbers/17', methods=['POST'])
def process_numbers_17():
    try:
        return _send_result(mt17(request))
    except Exception as e:
        print(f"Server error: {str(e)}")
        return jsonify({'error': 'Internal server error.'}), 500

@app.route('/api/numbers/18', methods=['POST'])
def process_numbers_18():
    try:
        return _send_result(mt18(request))
    except Exception as e:
        print(f"Server error: {str(e)}")
        return jsonify({'error': 'Internal server error.'}), 500

@app.route('/api/numbers/24', methods=['POST'])
def process_numbers_24():
    try:
        return _send_result(mt24(request))
    except Exception as e:
        print(f"Server error: {str(e)}")
        return jsonify({'error': 'Internal server error.'}), 500

@app.route('/api/numbers/25', methods=['POST'])
def process_numbers_25():
    try:
        return _send_result(mt25(request))
    except Exception as e:
        print(f"Server error: {str(e)}")
        return jsonify({'error': 'Internal server error.'}), 500

@app.route('/api/numbers/26', methods=['POST'])
def process_numbers_26():
    try:
        return _send_result(mt26(request))
    except Exception as e:
        print(f"Server error: {str(e)}")
        return jsonify({'error': 'Internal server error.'}), 500

@app.route('/api/numbers/27', methods=['POST'])
def process_numbers_27():
    try:
        return _send_result(mt27(request))
    except Exception as e:
        print(f"Server error: {str(e)}")
        return jsonify({'error': 'Internal server error.'}), 500

@app.route('/api/numbers/28', methods=['POST'])
def process_numbers_28():
    try:
        return _send_result(mt28(request))
    except Exception as e:
        print(f"Server error: {str(e)}")
        return jsonify({'error': 'Internal server error.'}), 500

# Run app
if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
