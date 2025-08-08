#HELPER FUNCTIONSS
def bch250_226_encode(message_bits):
    """
    Encodes a 226-bit message using a BCH(250,226)-style encoder.
    Returns a 250-bit codeword.
    """
    # Dummy generator polynomial of degree 24 (replace with actual BCH generator)
    generator = 0b100010000001000010000100001011  # Degree 24 → 25 bits

    if len(message_bits) != 226:
        raise ValueError("Message must be exactly 226 bits long to be encoded")

    # Shift message left by 24 bits (room for parity)
    message = int("".join(str(b) for b in message_bits), 2) << 24
    remainder = message

    # Divide modulo 2
    for i in range(226):
        if (remainder >> (249 - i)) & 1:
            remainder ^= generator << (225 - i)

    # Parity = remainder (24 bits)
    parity = remainder & 0xFFFFFF

    # Final codeword = message + parity
    codeword = message | parity

    return [int(b) for b in format(codeword, '0250b')]


def bch226_250_decode(message_bits):
    """
    Decodes a 250-bit message using a BCH(226,250)-style decoder.
    Returns a 226-bit message.
    """
    # Check if this is 250 bits
    if len(message_bits) != 250:
        raise ValueError("Message must be 250 bits long to be decoded")
                        
    # Literally just remove the last 24 bits (parity bits)
    return message_bits[:226]


def binary_to_hex(binary_string):
    """
    Converts a binary string to a hexadecimal string. Assumes the binary string is correctly padded to a multiple of 4 bits.
    """

    # Step 2: Use Python's built-in conversion for efficiency
    print(hex(int(binary_string, 2)))
    hex_string = hex(int(binary_string, 2)).upper()
    

    # Ensure hex string length is even (pad with leading zero if necessary)
    if len(hex_string) % 2 != 0:
        hex_string = '0' + hex_string

    return hex_string
