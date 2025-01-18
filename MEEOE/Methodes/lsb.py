from PIL import Image

def hide_message_lsb(image_path, message, output_path):
    img = Image.open(image_path)
    binary_message = ''.join([format(ord(char), '08b') for char in message]) + '1111111111111110'  # End marker
    img_data = list(img.getdata())
    if len(binary_message) > len(img_data) * 3:
        raise ValueError("Message too large to hide in image.")

    new_data = []
    binary_idx = 0

    for pixel in img_data:
        r, g, b = pixel[:3]
        if binary_idx < len(binary_message):
            r = (r & ~1) | int(binary_message[binary_idx])
            binary_idx += 1
        if binary_idx < len(binary_message):
            g = (g & ~1) | int(binary_message[binary_idx])
            binary_idx += 1
        if binary_idx < len(binary_message):
            b = (b & ~1) | int(binary_message[binary_idx])
            binary_idx += 1
        new_data.append((r, g, b) + pixel[3:] if len(pixel) == 4 else (r, g, b))

    img.putdata(new_data)
    img.save(output_path)

def extract_message_lsb(image_path):
    img = Image.open(image_path)
    img_data = list(img.getdata())
    binary_message = ''

    for pixel in img_data:
        for color in pixel[:3]:
            binary_message += str(color & 1)

    bytes_message = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    decoded_message = ''
    for byte in bytes_message:
        if byte == '11111110':
            break
        decoded_message += chr(int(byte, 2))
    return decoded_message
