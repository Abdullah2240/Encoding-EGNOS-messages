# CRC-24 generator polynomial: x^24 + x^23 + x^18 + x^17 + x^14 + x^11 +
#                               x^10 + x^7 + x^6 + x^5 + x^4 + x^3 + x + 1
# Global var
CRC24_POLY = "1100001100100110011111011"  # binary form as per Qualcom computing standards in CRC-24

#HELPER FUNCTIONSS
def crc24_encode(data_bits: str) -> str:
    n = len(CRC24_POLY)
    dividend = data_bits + "0" * (n - 1)

    # Modulo-2 division
    remainder = dividend
    for i in range(len(data_bits)):
        if remainder[i] == "1":
            # XOR with the polynomial
            remainder = (remainder[:i] +
                         ''.join('0' if remainder[i + j] == CRC24_POLY[j] else '1'
                                 for j in range(n)) +
                         remainder[i + n:])
    crc = remainder[-(n - 1):]
    return data_bits + crc

# returns true if no errors and returns false if there are errors 
def crc24_check(codeword_bits: str) -> bool:
    """Checks if a CRC-24 encoded binary string is error-free."""
    n = len(CRC24_POLY)
    remainder = codeword_bits
    for i in range(len(codeword_bits) - (n - 1)):
        if remainder[i] == "1":
            remainder = (remainder[:i] +
                         ''.join('0' if remainder[i + j] == CRC24_POLY[j] else '1'
                                 for j in range(n)) +
                         remainder[i + n:])
    return set(remainder[-(n - 1):]) == {"0"}  # True if no error


def binary_to_hex(binary_string):
    """
    Converts a binary string to a hexadecimal string. 
    Pads with zeros to make the length a multiple of 4 bits.
    """
    # Pad with zeros to make length a multiple of 4
    padding_length = (4 - (len(binary_string) % 4)) % 4
    padded_binary = binary_string + "0" * padding_length
    
    # Convert to hex
    print(padded_binary)
    hex_string = hex(int(padded_binary, 2))[2:].upper()
    
    return hex_string + "0"

def dict_to_bitstring(validated_dict):
    # Define bit lengths for each parameter
    bit_lengths = {
        "Brrc": 10, "Cltc_lsb": 10, "Cltc_v1": 10, "Iltc_v1": 9,
        "Cltc_v0": 10, "Iltc_v0": 9, "Cgeo_lsb": 10, "Cgeo_v": 10,
        "Igeo": 9, "Cer": 6, "Ciono_step": 10, "Iiono": 9,
        "Ciono_ramp": 10, "RSSUDRE": 1, "RSSiono": 1, "Ccovariance": 7
    }

    bitstring_parts = []

    for key, value in validated_dict.items():
        if key in bit_lengths:
            bits = bit_lengths[key]
            # Convert value to binary, pad with leading zeros
            bin_val = format(value, f'0{bits}b')
            bitstring_parts.append(f"{key}: {bin_val}")

    return "\n".join(bitstring_parts)

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

def mt10_to_bits(data):
    # Spec: field → (bits, scale factor)
    spec = {
        "Brrc":        (10, 0.002),
        "Cltc_lsb":    (10, 0.002),
        "Cltc_v1":     (10, 0.00005),
        "Iltc_v1":     (9, 1),
        "Cltc_v0":     (10, 0.002),
        "Iltc_v0":     (9, 1),
        "Cgeo_lsb":    (10, 0.0005),
        "Cgeo_v":      (10, 0.00005),
        "Igeo":        (9, 1),
        "Cer":         (6, 0.5),
        "Ciono_step":  (10, 0.001),
        "Iiono":       (9, 1),
        "Ciono_ramp":  (10, 0.000005),
        "RSSUDRE":     (1, 1),
        "RSSiono":     (1, 1),
        "Ccovariance": (7, 0.1),
    }

    bits = ""

    for field, (nbits, lsb) in spec.items():
        value = data[field]
        raw_int = round(value / lsb)
        bits += format(raw_int, f"0{nbits}b")

    # Add 81 spare bits
    bits += "0" * 81
    return bits