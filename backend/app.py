from flask import Flask, request, jsonify, send_from_directory
import os
from flask_cors import CORS
from helper import crc24_encode, binary_to_hex, crc24_check

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



# API Endpoint
@app.route('/api/numbers', methods=['POST'])
def process_numbers():
    try:
        # Parse and validate JSON input
        req_data = request.get_json()
        if not req_data or 'numbers' not in req_data:
            return jsonify({'error': 'Missing "numbers" field.'}), 400

        numbers_str = req_data['numbers']
        try:
            numbers = list(map(int, numbers_str.split(',')))
        except ValueError:
            return jsonify({'error': 'Invalid input. Please provide a comma-separated list of numbers.'}), 400

        if len(numbers) > 51:
            return jsonify({'error': 'Too many numbers. Max is 51.'}), 400
        if any(num < 1 or num > 210 for num in numbers):
            return jsonify({'error': 'Numbers must be between 1 and 210.'}), 400

        # Prepare message
        preamble = "10011010"
        message_type1 = "000001"
        data_bits = [0] * 212

        for prn in numbers:
            if 0 <= prn < 210:
                data_bits[prn-1] = 1
            else:
                return jsonify({'error': f'PRN {prn} is out of range (0–209)'}), 400

        non_coded_message = preamble + message_type1 + ''.join(map(str, data_bits))

        # Encode message
        coded_string = crc24_encode(non_coded_message)
        bit_string = ''.join(map(str, coded_string))

        if len(bit_string) != 250:
            return jsonify({'error': 'Bit string should be 250 bits.'}), 500

        hex_string = binary_to_hex(bit_string + "00")  # +00 to align to byte boundary

        # CRC check
        if not crc24_check(bit_string):
            return jsonify({'error': 'CRC check failed. Input may be corrupted.'}), 400

        # Decode message
        decoded_string = bit_string[:226]
        if decoded_string[:8] != preamble:
            return jsonify({'error': 'Preamble mismatch. Likely fake input.'}), 400
        if decoded_string[8:14] != message_type1:
            return jsonify({'error': 'Unknown message type. Expected type 1.'}), 400

        received_PRNs = [idx for idx, bit in enumerate(decoded_string[14:226]) if bit == "1"]

        return jsonify({
            'bit_string': bit_string,
            'hex_string': hex_string,
            'received_PRNs': received_PRNs
        })

    except Exception as e:
        print(f"Server error: {str(e)}")
        return jsonify({'error': 'Internal server error.'}), 500


# Run app
if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
