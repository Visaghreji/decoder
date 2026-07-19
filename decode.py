import sys
from PIL import Image

DELIMITER = "1111111111111110"  # must match the one used in encode_message.py


def decode(input_path: str) -> str:
    img = Image.open(input_path).convert("RGB")
    width, height = img.size
    pixels = img.load()

    bits = []
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            for value in (r, g, b):
                bits.append(str(value & 1))

    bitstring = ''.join(bits)

    end_index = bitstring.find(DELIMITER)
    if end_index == -1:
        raise ValueError(
            "No hidden message found (delimiter missing). "
            "The image may not contain an embedded message, or it was "
            "re-saved/compressed after encoding, which destroys the data."
        )

    message_bits = bitstring[:end_index]

    chars = []
    for i in range(0, len(message_bits), 8):
        byte = message_bits[i:i + 8]
        if len(byte) == 8:
            chars.append(chr(int(byte, 2)))

    return ''.join(chars)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python decode_message.py stego_image.png")
        sys.exit(1)

    try:
        message = decode(sys.argv[1])
        print("Hidden message found:")
        print(message)
    except ValueError as e:
        print(f"Error: {e}")
