from flask import jsonify
from helper import crc24_encode, binary_to_hex, dict_to_bitstring, hex_to_binary, int_to_binary, encode_signed_scaled, validate_iod_values, parse_csv_strict, create_message_frame_with_preamble, encode_fast_bits_and_udrei, encode_message_with_crc, mt10_to_bits

def mt1(request):
	print(request)
	req_data = request.get_json()
	# Extract fields
	numbers_str = req_data.get('numbers', '')
	preamble = req_data.get('preamble', '53')
	iodp = req_data.get('iodp', '0')
	try:
		numbers = list(map(int, numbers_str.split(',')))
		iodp_int = int(iodp)
	except ValueError:
		return jsonify({'error': 'Invalid input. Please provide valid numbers and IODP.'}), 400
	if len(numbers) > 51:
		return jsonify({'error': 'Too many numbers. Max is 51.'}), 400
	if any(num < 1 or num > 210 for num in numbers):
		return jsonify({'error': 'Numbers must be between 1 and 210.'}), 400
	if not (0 <= iodp_int <= 3):
		return jsonify({'error': 'IODP must be between 0 and 3.'}), 400
	# Convert hex preamble to binary
	try:
		preamble_bits = hex_to_binary(preamble)
	except ValueError as ve:
		return jsonify({'error': str(ve)}), 400
	message_type_bits = "000001"  # Message Type 1
	# Create PRN mask (210 bits)
	prn_mask = [0] * 210
	for prn in numbers:
		if 1 <= prn <= 210:
			prn_mask[prn-1] = 1
		else:
			return jsonify({'error': f'PRN {prn} is out of range 1-210'}), 400
	# Convert IODP to 2 bits
	iodp_bits = f"{iodp_int:02b}"
	# Combine all bits: preamble + message_type + prn_mask + iodp
	data_bits = ''.join(map(str, prn_mask)) + iodp_bits
	message_bits = preamble_bits + message_type_bits + data_bits
	# Encode with CRC-24
	try:
		coded_string = crc24_encode(message_bits)
		hex_string = binary_to_hex(coded_string)
		return hex_string
	except Exception as e:
		print(f"Encoding error: {str(e)}")
		return jsonify({'error': 'Failed to encode message'}), 500

# Utility functions

# Message Type 2 - Fast Corrections (12-bit each)
def mt2(request):
	print(request)
	req_data = request.get_json()
	preamble = req_data.get("preamble", "53")
	iodp = int(req_data.get("iodp", 0))
	iodf = int(req_data.get("iodf", 0))
	pseudo_range_corrections = req_data.get("pseudoRangeCorrections", "")
	udreis = req_data.get("udreis", "")
	is_valid, error_msg = validate_iod_values(iodp, iodf)
	if not is_valid:
		return jsonify({'error': error_msg}), 400
	try:
		prc_list = parse_csv_strict(pseudo_range_corrections, 'float', 13, -256.0, 255.875, 'pseudoRangeCorrections')
		udrei_list = parse_csv_strict(udreis, 'int', 13, 0, 15, 'udreis')
	except ValueError as ve:
		return jsonify({'error': str(ve)}), 400
	if len(prc_list) == 0 or len(udrei_list) == 0:
		return jsonify({'error': 'Provide at least one fast correction and one UDREI (comma separated).'}), 400
	if len(prc_list) != len(udrei_list):
		return jsonify({'error': f'Count mismatch: {len(prc_list)} fast corrections vs {len(udrei_list)} UDREIs. Provide equal counts (up to 13).'}), 400
	iodf_bits = int_to_binary(iodf, 2)
	iodp_bits = int_to_binary(iodp, 2)
	prc_bits, udrei_bits = encode_fast_bits_and_udrei(prc_list, udrei_list)
	data_bits = iodf_bits + iodp_bits + prc_bits + udrei_bits
	try:
		message_bits = create_message_frame_with_preamble(preamble, 2, data_bits)
	except ValueError as ve:
		return jsonify({'error': str(ve)}), 400
	hex_string = encode_message_with_crc(message_bits)
	if hex_string is None:
		return jsonify({'error': 'Failed to encode message'}), 500
	return hex_string

# Message Type 3 - Fast Corrections (12-bit each)
def mt3(request):
	print(request)
	req_data = request.get_json()
	preamble = req_data.get("preamble", "53")
	iodp = int(req_data.get("iodp", 0))
	iodf = int(req_data.get("iodf", 0))
	pseudo_range_corrections = req_data.get("pseudoRangeCorrections", "")
	udreis = req_data.get("udreis", "")
	is_valid, error_msg = validate_iod_values(iodp, iodf)
	if not is_valid:
		return jsonify({'error': error_msg}), 400
	try:
		prc_list = parse_csv_strict(pseudo_range_corrections, 'float', 13, -256.0, 255.875, 'pseudoRangeCorrections')
		udrei_list = parse_csv_strict(udreis, 'int', 13, 0, 15, 'udreis')
	except ValueError as ve:
		return jsonify({'error': str(ve)}), 400
	iodf_bits = int_to_binary(iodf, 2)
	iodp_bits = int_to_binary(iodp, 2)
	prc_bits, udrei_bits = encode_fast_bits_and_udrei(prc_list, udrei_list)
	data_bits = iodf_bits + iodp_bits + prc_bits + udrei_bits
	try:
		message_bits = create_message_frame_with_preamble(preamble, 3, data_bits)
	except ValueError as ve:
		return jsonify({'error': str(ve)}), 400
	hex_string = encode_message_with_crc(message_bits)
	if hex_string is None:
		return jsonify({'error': 'Failed to encode message'}), 500
	return hex_string

# Message Type 4 - Fast Corrections (12-bit each)
def mt4(request):
	print(request)
	req_data = request.get_json()
	preamble = req_data.get("preamble", "53")
	iodp = int(req_data.get("iodp", 0))
	iodf = int(req_data.get("iodf", 0))
	pseudo_range_corrections = req_data.get("pseudoRangeCorrections", "")
	udreis = req_data.get("udreis", "")
	is_valid, error_msg = validate_iod_values(iodp, iodf)
	if not is_valid:
		return jsonify({'error': error_msg}), 400
	try:
		prc_list = parse_csv_strict(pseudo_range_corrections, 'float', 13, -256.0, 255.875, 'pseudoRangeCorrections')
		udrei_list = parse_csv_strict(udreis, 'int', 13, 0, 15, 'udreis')
	except ValueError as ve:
		return jsonify({'error': str(ve)}), 400
	iodf_bits = int_to_binary(iodf, 2)
	iodp_bits = int_to_binary(iodp, 2)
	prc_bits, udrei_bits = encode_fast_bits_and_udrei(prc_list, udrei_list)
	data_bits = iodf_bits + iodp_bits + prc_bits + udrei_bits
	try:
		message_bits = create_message_frame_with_preamble(preamble, 4, data_bits)
	except ValueError as ve:
		return jsonify({'error': str(ve)}), 400
	hex_string = encode_message_with_crc(message_bits)
	if hex_string is None:
		return jsonify({'error': 'Failed to encode message'}), 500
	return hex_string

# Message Type 5 - Fast Corrections (12-bit each)
def mt5(request):
	print(request)
	req_data = request.get_json()
	preamble = req_data.get("preamble", "53")
	iodp = int(req_data.get("iodp", 0))
	iodf = int(req_data.get("iodf", 0))
	pseudo_range_corrections = req_data.get("pseudoRangeCorrections", "")
	udreis = req_data.get("udreis", "")
	is_valid, error_msg = validate_iod_values(iodp, iodf)
	if not is_valid:
		return jsonify({'error': error_msg}), 400
	try:
		prc_list = parse_csv_strict(pseudo_range_corrections, 'float', 13, -256.0, 255.875, 'pseudoRangeCorrections')
		udrei_list = parse_csv_strict(udreis, 'int', 13, 0, 15, 'udreis')
	except ValueError as ve:
		return jsonify({'error': str(ve)}), 400
	iodf_bits = int_to_binary(iodf, 2)
	iodp_bits = int_to_binary(iodp, 2)
	prc_bits, udrei_bits = encode_fast_bits_and_udrei(prc_list, udrei_list)
	data_bits = iodf_bits + iodp_bits + prc_bits + udrei_bits
	try:
		message_bits = create_message_frame_with_preamble(preamble, 5, data_bits)
	except ValueError as ve:
		return jsonify({'error': str(ve)}), 400
	hex_string = encode_message_with_crc(message_bits)
	if hex_string is None:
		return jsonify({'error': 'Failed to encode message'}), 500
	return hex_string

# Message Type 6 - Integrity Information
def mt6(request):
	print(request)
	req_data = request.get_json()
	preamble = req_data.get("preamble", "53")
	try:
		iodf2 = int(req_data.get("iodf2", 0))
		iodf3 = int(req_data.get("iodf3", 0))
		iodf4 = int(req_data.get("iodf4", 0))
		iodf5 = int(req_data.get("iodf5", 0))
	except (TypeError, ValueError):
		return jsonify({'error': 'IODF2-5 must be integers'}), 400
	for idx, v in enumerate([iodf2, iodf3, iodf4, iodf5], start=2):
		if v < 0 or v > 3:
			return jsonify({'error': f'IODF{idx} must be 0..3'}), 400
	udreis_raw = req_data.get("udreis", "")
	try:
		udrei_clamped = parse_csv_strict(udreis_raw, 'int', 51, 0, 15, 'udreis')
	except ValueError as ve:
		return jsonify({'error': str(ve)}), 400
	while len(udrei_clamped) < 51:
		udrei_clamped.append(14)
	iodf_bits = (
		int_to_binary(iodf2, 2) +
		int_to_binary(iodf3, 2) +
		int_to_binary(iodf4, 2) +
		int_to_binary(iodf5, 2)
	)
	udrei_bits = ''.join(int_to_binary(u, 4) for u in udrei_clamped[:51])
	data_bits = iodf_bits + udrei_bits
	try:
		message_bits = create_message_frame_with_preamble(preamble, 6, data_bits)
	except ValueError as ve:
		return jsonify({'error': str(ve)}), 400
	hex_string = encode_message_with_crc(message_bits)
	if hex_string is None:
		return jsonify({'error': 'Failed to encode message'}), 500
	return hex_string

# Message Type 7 - Fast Correction Degradation

def mt7(request):
	print(request)
	req_data = request.get_json()
	preamble = req_data.get("preamble", "53")
	try:
		tlat = int(req_data.get("tlat", 0))
		iodp = int(req_data.get("iodp", 0))
	except (TypeError, ValueError):
		return jsonify({'error': 'tlat and iodp must be integers'}), 400
	if tlat < 0 or tlat > 15:
		return jsonify({'error': 'tlat must be 0..15 seconds'}), 400
	if iodp < 0 or iodp > 3:
		return jsonify({'error': 'iodp must be 0..3'}), 400
	aii_raw = req_data.get("aii", "")
	try:
		aii_list = parse_csv_strict(aii_raw, 'int', 51, 0, 15, 'aii')
	except ValueError as ve:
		return jsonify({'error': str(ve)}), 400
	while len(aii_list) < 51:
		aii_list.append(0)
	tlat_bits = int_to_binary(tlat, 4)
	iodp_bits = int_to_binary(iodp, 2)
	spare_bits = "00"
	aii_bits = ''.join(int_to_binary(a, 4) for a in aii_list[:51])
	data_bits = tlat_bits + iodp_bits + spare_bits + aii_bits
	try:
		message_bits = create_message_frame_with_preamble(preamble, 7, data_bits)
	except ValueError as ve:
		return jsonify({'error': str(ve)}), 400
	hex_string = encode_message_with_crc(message_bits)
	if hex_string is None:
		return jsonify({'error': 'Failed to encode message'}), 500
	return hex_string

# Message Type 9 - GEO Navigation

def mt9(request):
	print(request)
	req = request.get_json()
	preamble = req.get("preamble", "53")
	def req_float(name):
		v = req.get(name, None)
		if v is None or str(v).strip() == "":
			raise ValueError(f"{name}: missing input")
		try:
			return float(v)
		except Exception:
			raise ValueError(f"{name}: not a valid number")
	def req_int(name, min_v, max_v):
		v = req.get(name, None)
		if v is None or str(v).strip() == "":
			raise ValueError(f"{name}: missing input")
		try:
			iv = int(v)
		except Exception:
			raise ValueError(f"{name}: not a valid integer")
		if iv < min_v or iv > max_v:
			raise ValueError(f"{name}: value {iv} out of range [{min_v}, {max_v}]")
		return iv
	try:
		t0 = req_int("t0", 0, 86384)
		ura = req_int("ura", 0, 15)
		xg = req_float("xg")
		yg = req_float("yg")
		zg = req_float("zg")
		xg_rate = req_float("xg_rate")
		yg_rate = req_float("yg_rate")
		zg_rate = req_float("zg_rate")
		xg_acc = req_float("xg_acc")
		yg_acc = req_float("yg_acc")
		zg_acc = req_float("zg_acc")
		agf0 = req_float("agf0")
		agf1 = req_float("agf1")
	except ValueError as ve:
		return jsonify({'error': str(ve)}), 400
	def check_abs(name, value, limit):
		if abs(value) > limit:
			raise ValueError(f"{name}: |value| {value} exceeds nominal bound {limit}")
	try:
		check_abs("xg", xg, 42949673)
		check_abs("yg", yg, 42949673)
		check_abs("zg", zg, 6710886.4)
		check_abs("xg_rate", xg_rate, 40.96)
		check_abs("yg_rate", yg_rate, 40.96)
		check_abs("zg_rate", zg_rate, 524.288)
		check_abs("xg_acc", xg_acc, 0.0064)
		check_abs("yg_acc", yg_acc, 0.0064)
		check_abs("zg_acc", zg_acc, 0.032)
	except ValueError as ve:
		return jsonify({'error': str(ve)}), 400
	reserved8 = "00000000"
	try:
		t0_steps = int(round(t0 / 16.0))
		if t0_steps < 0:
			t0_steps = 0
		elif t0_steps > ((1 << 13) - 1):
			t0_steps = (1 << 13) - 1
		t0_bits = f"{t0_steps:013b}"
	except Exception:
		return jsonify({'error': 't0 encoding failed'}), 500
	ura_bits = f"{ura:04b}"
	xg_bits = encode_signed_scaled(xg, 30, 1/0.08)
	yg_bits = encode_signed_scaled(yg, 30, 1/0.08)
	zg_bits = encode_signed_scaled(zg, 25, 1/0.4)
	xg_rate_bits = encode_signed_scaled(xg_rate, 17, 1/0.000625)
	yg_rate_bits = encode_signed_scaled(yg_rate, 17, 1/0.000625)
	zg_rate_bits = encode_signed_scaled(zg_rate, 18, 1/0.004)
	xg_acc_bits = encode_signed_scaled(xg_acc, 10, 1/0.0000125)
	yg_acc_bits = encode_signed_scaled(yg_acc, 10, 1/0.0000125)
	zg_acc_bits = encode_signed_scaled(zg_acc, 10, 1/0.0000625)
	agf0_bits = encode_signed_scaled(agf0, 12, 2**31)
	agf1_bits = encode_signed_scaled(agf1, 8, 2**40)
	data_bits = (reserved8 + t0_bits + ura_bits + xg_bits + yg_bits + zg_bits +
				 xg_rate_bits + yg_rate_bits + zg_rate_bits +
				 xg_acc_bits + yg_acc_bits + zg_acc_bits +
				 agf0_bits + agf1_bits)
	try:
		message_bits = create_message_frame_with_preamble(preamble, 9, data_bits)
	except ValueError as ve:
		return jsonify({'error': str(ve)}), 400
	hex_string = encode_message_with_crc(message_bits)
	if hex_string is None:
		return jsonify({'error': 'Failed to encode message'}), 500
	return hex_string

# Placeholder functions for other message types

from flask import request, jsonify

from flask import request, jsonify

def mt10(request):
    req_data = request.get_json(force=True, silent=True)
    print("Received request data:", req_data)
    if not req_data:
        return jsonify({'error': 'Invalid or missing JSON body'}), 400

    # Default preamble (hex string)
    preamble = req_data.get("preamble", "53")

    # Expected fields → (type, min, max, units)
    fields = {
        "Brrc": (float, 0, 2.046, "m"),
        "Cltc_lsb": (float, 0, 2.046, "m"),
        "Cltc_v1": (float, 0, 0.05115, "m/s"),
        "Iltc_v1": (int, 1, 511, "s"),       # 0 auto-corrected → enforce min=1
        "Cltc_v0": (float, 0, 2.046, "m"),
        "Iltc_v0": (int, 1, 511, "s"),       # 0 auto-corrected → enforce min=1
        "Cgeo_lsb": (float, 0, 0.5115, "m"),
        "Cgeo_v": (float, 0, 0.05115, "m/s"),
        "Igeo": (int, 0, 511, "s"),
        "Cer": (float, 0, 31.5, "m"),
        "Ciono_step": (float, 0, 1.023, "m"),
        "Iiono": (int, 1, 511, "s"),         # 0 auto-corrected → enforce min=1
        "Ciono_ramp": (float, 0, 0.005115, "m/s"),
        "RSSUDRE": (int, 0, 1, "unitless"),
        "RSSiono": (int, 0, 1, "unitless"),
        "Ccovariance": (float, 0, 12.7, "unitless"),
    }

    validated = {}

    # Validate & cast
    for field, (dtype, min_val, max_val, unit) in fields.items():
        raw_value = req_data.get(field)
        if raw_value is None:
            print("Missing field:", field)
            return jsonify({'error': f'Missing required field: {field}'}), 400

        try:
            value = dtype(raw_value)
        except (TypeError, ValueError):
            print(f"Invalid type for {field}: {raw_value} (expected {dtype.__name__})")
            return jsonify({'error': f'Invalid type for {field}, expected {dtype.__name__}'}), 400

        if not (min_val <= value <= max_val):
            print(f"Value out of range for {field}: {value} ({min_val}–{max_val} {unit})")
            return jsonify({'error': f'{field} out of range ({min_val}–{max_val} {unit}), got {value}'}), 400

        validated[field] = value

    # Build header bits (preamble + message type)
    try:
        mt_type = 10
        data_bits = format(int(preamble, 16), '08b') + format(mt_type, '06b')
    except Exception:
        return jsonify({'error': 'Invalid preamble format (must be hex)'}), 400

    # At this point you can feed `validated` into your encoder
    print("Validated data:", validated)
    print("Header bits:", data_bits)
	
	# Convert validated data to bitstring
    data_bits += mt10_to_bits(validated)

    hex_string = encode_message_with_crc(data_bits)
    print("length of data bits: ", len(data_bits), "data: ", data_bits, "\n\n\n")
    print("length of hex string: ", "hex:", hex_string)
    
    return hex_string



def mt12(request):
	return jsonify({'error': 'Message Type 12 not implemented yet'}), 501

def mt17(request):
	return jsonify({'error': 'Message Type 17 not implemented yet'}), 501

def mt18(request):
	return jsonify({'error': 'Message Type 18 not implemented yet'}), 501

def mt24(request):
	return jsonify({'error': 'Message Type 24 not implemented yet'}), 501

def mt25(request):
	return jsonify({'error': 'Message Type 25 not implemented yet'}), 501

def mt26(request):
	return jsonify({'error': 'Message Type 26 not implemented yet'}), 501

def mt27(request):
	return jsonify({'error': 'Message Type 27 not implemented yet'}), 501

def mt28(request):
	return jsonify({'error': 'Message Type 28 not implemented yet'}), 501