import socket
import json
import random
import base64
from Crypto.Cipher import AES
from datetime import datetime
from service_announcer import get_local_ip

P = 23                                                                            
G = 5
local_ip = get_local_ip()

def diffie_hellman_key_exchange(user_number, peer_number):  #0
    return (peer_number ** user_number) % P

def decrypt_message(key, encrypted_message):    #0
    key = key.encode('utf-8').ljust(16, b'0')[:16]  # AES require 16 bytes block
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_mess_bytes = base64.b64decode(encrypted_message)
    decrypted_mess = cipher.decrypt(encrypted_mess_bytes)
    pad_length = decrypted_mess[-1] # Learn padding length from last byte
    return decrypted_mess[:-pad_length].decode('utf-8').strip() # Remove padding

def log_message(user, username, message, state):    #0
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('chat_history.log', 'a') as log:
        log.write(f"| {timestamp} | {user} >> received from >> {username} | {state} message >> {message} |\n")

def load_peers():   #0
    peers = {}
    with open("peers.txt", "r") as file:
        for line in file:
            ip, username, timestamp = line.strip().split()
            peers[ip] = {"username": username, "timestamp": float(timestamp), "ip": ip}
    return peers

def get_username(adress):   #0
    peers = load_peers()
    for ip, info in peers.items():
        if adress == info['ip']:
            username = info['username']
    return username

def chat_responder(user):   #1
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((local_ip, 6001))                                                         
    server_socket.listen()
    
    while True:
        client_socket, addr = server_socket.accept()    
        while True:                                                 # Need an inner while loop to update message after key exchange with encrypted message
            message = json.loads(client_socket.recv(4096).decode()) # DEBUG print(f"Received message: {message}") 
            if 'key' in message:
                user_random_number = random.randint(1, P)
                user_public_value = (G ** user_random_number) % P
                client_socket.send(json.dumps({"key": user_public_value}).encode())
                peer_public_value = message['key']
                key = diffie_hellman_key_exchange(user_random_number, peer_public_value)
                key = str(key)[:16].ljust(16, '0')                   # DEBUG print(f"Generated key: {key}")
                continue            # Continue to the next iteration to wait for the encrypted message or unencrypted message

            elif 'encrypted message' in message:
                encrypted_message = message['encrypted message']     # DEBUG print(f"Incoming message: {message}") 
                decrypted_message = decrypt_message(key, encrypted_message) # DEBUG print(f"Encrypted message: {encrypted_message}")
                print(f"\n| Secure: {get_username(addr[0])} => {user} >> {decrypted_message} |")                
                log_message(user, get_username(addr[0]), decrypted_message, "secure")                            
 
            elif 'unencrypted message' in message:
                print(f"\n| Unsecure: {get_username(addr[0])} => {user} >> {message['unencrypted message']} |")    
                log_message(user, get_username(addr[0]), message['unencrypted message'], "unsecure")       

            client_socket.close()
            break   # Exit inner loop after handling the 'message'

if __name__ == "__main__":  #1
    chat_responder()