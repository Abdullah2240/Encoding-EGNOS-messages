# CRC-24 generator polynomial: x^24 + x^23 + x^18 + x^17 + x^14 + x^11 +
#                               x^10 + x^7 + x^6 + x^5 + x^4 + x^3 + x + 1
# Global var
CRC24_POLY = "1100001100100110011111011"  # binary form as per Qualcom computing standards in CRC-24

#HELPER FUNCTIONSS
def crc24_encode(data_bits: str) -> str:
    print(len(data_bits))
    n = len(CRC24_POLY)
    print("n:", n)
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
    print("\n", len(crc))
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
    Converts a binary string to a hexadecimal string. Assumes the binary string is correctly padded to a multiple of 4 bits.
    """

    # binary_string += "00" + binary_string
    # Step 2: Use Python's built-in conversion for efficiency
    print(hex(int(binary_string, 2)))
    hex_string = hex(int(binary_string, 2))[2:].upper()
    
    hex_string = hex_string + "0"

    return hex_string
