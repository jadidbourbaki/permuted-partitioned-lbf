from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
import secrets

# Generate a 128 bit key
def generate_key():
    return get_random_bytes(AES.block_size)

def generate_iv():
    return get_random_bytes(AES.block_size)

def encrypt(plaintext, key):
    iv = generate_iv()

    # Convert the key to bytes if it's a string
    if isinstance(key, str):
        key = key.encode('utf-8')
    
    # Ensure the key is 16 bytes (128 bits)
    key = key[:16].ljust(16, b'\0')
    
    # Create cipher object
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Pad the plaintext and encrypt
    padded_data = pad(plaintext.encode('utf-8'), AES.block_size)

    # embed IV into the ciphertext
    ciphertext = cipher.encrypt(iv + padded_data)
    
    # Combine IV and ciphertext and encode as base64
    encrypted_message = base64.b64encode(ciphertext)
    
    return encrypted_message.decode('utf-8')

def decrypt(encrypted_message, key):
    # Convert the key to bytes if it's a string
    if isinstance(key, str):
        key = key.encode('utf-8')
    
    # Ensure the key is 16 bytes (128 bits)
    key = key[:16].ljust(16, b'\0')
    
    raw = base64.b64decode(encrypted_message)
    iv = raw[:AES.block_size]
    encrypted_data = raw[AES.block_size:]

    # Decode the base64 encrypted message
    padded_data = pad(encrypted_data.encode('utf-8'), AES.block_size)
    encrypted_data = base64.b64decode(padded_data)
    
    # Create cipher object
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Decrypt and unpad
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    
    return decrypted_data.decode('utf-8')