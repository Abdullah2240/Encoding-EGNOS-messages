from flask import jsonify
from helper import crc24_encode, binary_to_hex

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
def hex_to_binary(hex_string):
	"""Convert 2-digit hex string to 8-bit binary string. Strict validation."""
	if hex_string is None:
		raise ValueError('preamble: missing')
	hex_clean = str(hex_string).strip().lower()
	if hex_clean.startswith('0x'):
		hex_clean = hex_clean[2:]
	if len(hex_clean) != 2:
		raise ValueError("preamble: must be exactly 2 hex digits (e.g., 53, 9A, C6)")
	try:
		decimal_value = int(hex_clean, 16)
	except Exception:
		raise ValueError("preamble: invalid hex digits")
	return f"{decimal_value:08b}"

def int_to_binary(value, bit_length):
	"""Convert integer to binary string with specified bit length"""
	if value < 0:
		# Handle negative numbers using two's complement
		value = (1 << bit_length) + value
	return f"{value & ((1 << bit_length) - 1):0{bit_length}b}"

def encode_signed_scaled(value, bit_length, scale=1):
	"""Scale, clamp to signed range for bit_length, return two's complement binary."""
	scaled = int(round(value * scale))
	min_val = -(1 << (bit_length - 1))
	max_val = (1 << (bit_length - 1)) - 1
	if scaled < min_val:
		scaled = min_val
	elif scaled > max_val:
		scaled = max_val
	return int_to_binary(scaled, bit_length)

def validate_iod_values(iodp, iodf):
	"""Validate IODP and IODF values"""
	if not (0 <= iodp <= 3):
		return False, 'IODP must be between 0 and 3'
	if not (0 <= iodf <= 3):
		return False, 'IODF must be between 0 and 3'
	return True, ''

def parse_csv_strict(value_str: str, value_type: str, max_count: int, min_value, max_value, field_name: str):
	"""Parse strictly comma-separated values, enforce numeric regex and range."""
	if value_str is None:
		raise ValueError(f"{field_name}: missing input")
	text = value_str.strip()
	if text == "":
		return []
	tokens = text.split(',')
	if len(tokens) > max_count:
		raise ValueError(f"{field_name}: too many values; maximum is {max_count}")
	result = []
	for raw in tokens:
		part = raw.strip()
		if part == "":
			raise ValueError(f"{field_name}: empty entry between commas")
		if ' ' in part:
			raise ValueError(f"{field_name}: invalid format; use commas only between values")
		if value_type == 'int':
			if not part.lstrip('+-').isdigit():
				raise ValueError(f"{field_name}: '{part}' is not a valid integer")
			val = int(part)
		elif value_type == 'float':
			try:
				val = float(part)
			except Exception:
				raise ValueError(f"{field_name}: '{part}' is not a valid number")
		else:
			raise ValueError("Unsupported value_type")
		if val < min_value or val > max_value:
			raise ValueError(f"{field_name}: value {val} out of range [{min_value}, {max_value}]")
		result.append(val)
	return result

def create_message_frame_with_preamble(preamble_hex, message_type, data_bits):
	"""Create complete message frame with custom preamble and message type (validates preamble)."""
	preamble_bits = hex_to_binary(preamble_hex)
	message_type_bits = f"{message_type:06b}"
	return preamble_bits + message_type_bits + data_bits

def encode_message_with_crc(message_bits):
	"""Encode message with CRC-24 and convert to hex"""
	try:
		coded_string = crc24_encode(message_bits)
		hex_string = binary_to_hex(coded_string)
		return hex_string
	except Exception as e:
		print(f"Encoding error: {str(e)}")
		return None

def encode_fast_bits_and_udrei(prc_list, udrei_list):
	"""Encode 13 fast corrections and UDREIs."""
	prc_bits = ""
	udrei_bits = ""
	prc_vals = list(prc_list)[:13]
	udrei_vals = list(udrei_list)[:13]
	while len(prc_vals) < 13:
		prc_vals.append(0.0)
	while len(udrei_vals) < 13:
		udrei_vals.append(0)
	for i in range(13):
		prc = prc_vals[i]
		udrei = udrei_vals[i]
		if prc < -256.0 or prc > 255.875:
			encoded = encode_signed_scaled(prc, 12, 8)
			prc_bits += encoded
			udrei_bits += int_to_binary(15, 4)
		else:
			prc_bits += encode_signed_scaled(prc, 12, 8)
			if udrei < 0:
				udrei = 0
			elif udrei > 15:
				udrei = 15
			udrei_bits += int_to_binary(udrei, 4)
	return prc_bits, udrei_bits

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

def mt10(request):
	return jsonify({'error': 'Message Type 10 not implemented yet'}), 501

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