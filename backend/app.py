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
<<<<<<< HEAD
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
=======
        numbers = list(map(int, numbers_str.split(',')))
    except ValueError as e:
        return jsonify({
            "error": "ValueError",
            "message": str(e)
        }), 400 

    if len(numbers) > 51:
        return jsonify({
            "error": "TooMuchDataError",
            "message": "Too many numbers provided. Maximum is 51."
        }), 400 

    if any(num < 1 or num > 210 for num in numbers):
        return (jsonify({'error': 'Numbers must be between 1 and 210.'}), 400)


    # Here you can add any processing logic for the numbers 
    

    # Main program (add OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOP)
    preamble = "10001011"
    message_type1 = "000001"
    data = [0] * 210
    iodp = "00" # we can ch

    PRN_list = numbers # input from user

    #VALIDATE USER INPUT
    for d in PRN_list:
        if not isinstance(d, int):  # Ensure that `d` is an integer
            raise ValueError(f"Warning: '{d}' is not a valid number")
        
        idx = d  # `d` is already an integer
        if 0 <= idx < 210:
            data[idx] = 1
        else:
            raise ValueError(f"Warning: PRN {idx} is out of range (0-209)")

    # Build final message string
    non_coded_message = preamble + message_type1 + ''.join(str(b) for b in data) + iodp

    print("Non BCH coded message:")
    print(non_coded_message, "\n")

    #BCH ENCODING
    coded_string = bch250_226_encode(non_coded_message)
    bit_string = ""
    for a in coded_string:
        bit_string += str(a)
        
    # Bit string of length 250
    print("Bit String:    ", bit_string, "\nlength of bit string: ", len(bit_string))

    # hex string of length 63
    hex_string = binary_to_hex(bit_string + "00")
    print("Hex String:    ", hex_string, "\n length of hex string: ", len(hex_string))

    #extract 234 bits from 250 bits
    decoded_string = bch226_250_decode(bit_string)

    #Now we have 234 bits lets check if the user didnt just enter 250 random things
    if decoded_string[:8] != preamble:
        raise ValueError("Preamble does not match up, fake input")

    if decoded_string[8:14] != message_type1:  
        raise ValueError("Not a message of type 1, maybe others type we dont know")

    recieved_PRNs = []
    data = decoded_string[14:226]
    for idx, bit in enumerate(data):
        if bit == "1":
            recieved_PRNs.append(idx)

    # BACKSOLVING OUTPUT KINDA
    for prn in recieved_PRNs:
        print("PRNs: ", prn)

    return jsonify({
        'bit_string': bit_string,
        'hex_string': hex_string,
        'received_PRNs': recieved_PRNs  
    })
>>>>>>> f80c2643a48760c0e931f9a7465f8ba9b76394a7


# Run app
if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
