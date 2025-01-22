import cv2
import numpy as np

def hide_message_dct(image_path, message, output_path):
    img = cv2.imread(image_path)

    if len(img.shape) == 3:  
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    h, w = img.shape

    if len(message) * 8 > h * w // 64:
        raise ValueError("Message too large for this image.")

    binary_message = ''.join([format(ord(char), '08b') for char in message]) + '11111110'
    binary_idx = 0

    for i in range(0, h, 8):
        for j in range(0, w, 8):
            if binary_idx >= len(binary_message):
                break
            block = img[i:i+8, j:j+8]

            dct_block = cv2.dct(block.astype(np.float32))

            dct_block[7, 7] = (dct_block[7, 7] & ~1) | int(binary_message[binary_idx])
            binary_idx += 1

            img[i:i+8, j:j+8] = cv2.idct(dct_block).clip(0, 255).astype(np.uint8)

    cv2.imwrite(output_path, img)


def extract_message_dct(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    h, w = img.shape
    binary_message = ''

    for i in range(0, h, 8):
        for j in range(0, w, 8):
            block = img[i:i+8, j:j+8]
            dct_block = cv2.dct(block.astype(np.float32))
            binary_message += str(int(dct_block[7, 7]) & 1)
            if binary_message.endswith('11111110'):
                break

    bytes_message = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    decoded_message = ''.join(chr(int(byte, 2)) for byte in bytes_message if byte != '11111110')
    return decoded_message
