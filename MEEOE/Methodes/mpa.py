import numpy as np
from scipy.io import wavfile

def hide_message_audio(input_audio_path, message, output_audio_path):
    rate, data = wavfile.read(input_audio_path)
    binary_message = ''.join(format(ord(char), '08b') for char in message) + '11111110'
    message_bits = list(map(int, binary_message))
    flat_data = data.flatten()
    if len(message_bits) > len(flat_data):
        raise ValueError("Message too large for audio.")
    
    for i, bit in enumerate(message_bits):
        flat_data[i] = (flat_data[i] & ~1) | bit

    new_data = flat_data.reshape(data.shape)
    wavfile.write(output_audio_path, rate, new_data.astype(data.dtype))

def extract_message_audio(input_audio_path):
    rate, data = wavfile.read(input_audio_path)
    flat_data = data.flatten()
    binary_message = ''.join(str(flat_data[i] & 1) for i in range(len(flat_data)))
    
    bytes_message = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    decoded_message = ''
    for byte in bytes_message:
        if byte == '11111110':
            break
        decoded_message += chr(int(byte, 2))
    return decoded_message
