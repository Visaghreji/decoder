import sys
from PIL import Image

DELIMITER = "1111111111111110"  # 16-bit marker that signals "end of message"


def text_to_bits(text: str) -> str:
    return ''.join(format(ord(c), '08b') for c in text)


def encode(input_path: str, output_path: str, message: str) -> None:
    img = Image.open(input_path).convert("RGB")
    width, height = img.size
    pixels = img.load()

    bits = text_to_bits(message) + DELIMITER
    capacity = width * height * 3  # 1 bit per color channel

    if len(bits) > capacity:
        raise ValueError(
            f"Message too long: needs {len(bits)} bits, "
            f"image only has capacity for {capacity} bits."
        )

    bit_index = 0
    for y in range(height):
        for x in range(width):
            if bit_index >= len(bits):
                break
            r, g, b = pixels[x, y]
            channels = [r, g, b]
            for c in range(3):
                if bit_index < len(bits):
                    channels[c] = (channels[c] & ~1) | int(bits[bit_index])
                    bit_index += 1
            pixels[x, y] = tuple(channels)
        if bit_index >= len(bits):
            break

    img.save(output_path)
    print(f"Message encoded successfully into '{output_path}'")
    print(f"({len(message)} characters / {len(bits)} bits used out of {capacity} available)")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print('Usage: python encode_message.py input.png output.png "secret message"')
        sys.exit(1)

    input_path, output_path, message = sys.argv[1], sys.argv[2], sys.argv[3]

    if not output_path.lower().endswith(".png"):
        print("Warning: output should be saved as .png (or another lossless format), "
              "otherwise the hidden bits will be destroyed by compression.")

    encode(input_path, output_path, message)
