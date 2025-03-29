import time
import socket
import json
import random
from Crypto.Cipher import AES
import base64
from datetime import datetime

P = 23
G = 5
LOG_FILE = 'chat_history.log'
peers_file = "peers.txt"

def load_peers():   #0
    peers = {}
    with open(peers_file, "r") as file:
        for line in file:
            ip, username, timestamp = line.strip().split()
            peers[ip] = {"username": username, "timestamp": float(timestamp)}
    return peers

def display_users():    #1
    peers = load_peers()
    current_time = time.time()
    for ip, info in peers.items():
        if (current_time - info['timestamp']) <= 10:
            status = "Online" 
        else: 
            status = "Away"
        print(f"| > {info['username']} < | {status} |")

def diffie_hellman_math(user_number, peer_number):  #0
    return (peer_number ** user_number) % P

def pad_message(message):
    pad_length = 16 - (len(message) % 16)   #n bytes missing from block
    return message + chr(pad_length) * pad_length   #\x01 || \x0b\x0b\x0b... etc

def encrypt_message(key, message):  #0
    key = key.encode('utf-8').ljust(16, b'0')[:16]
    cipher = AES.new(key, AES.MODE_ECB)
    padded_message = pad_message(message).encode('utf-8')
    encrypted_mess = cipher.encrypt(padded_message)
    return base64.b64encode(encrypted_mess).decode('utf-8')

def initiate_chat(user):    #2
    peers = load_peers()
    username = input("| Who would you like to chat with: ")
    peer_ip = None
    for ip, info in peers.items():
        if info['username'] == username:
            peer_ip = ip
            break
    if not peer_ip:
        print(f"| >{username}< not found! Be sure to enter a valid user |")
        return

    secure = input("| Will you chat securely? yes/no y/n : ").strip().lower()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
    client_socket.connect((peer_ip, 6001))

    if secure == 'yes' or secure =='y':
        user_random_number = random.randint(1, P)
        user_public_value = (G ** user_random_number) % P
        client_socket.send(json.dumps({"key": user_public_value}).encode()) # Diffie-Hellman Key exchange
        
        response = json.loads(client_socket.recv(4096).decode())            # Receive public value of the peer.
        peer_public_value = response.get("key")

        key = diffie_hellman_math(user_random_number, peer_public_value)    # Calculate the shared secret key, both peers have the shared secret key and can encrypt/decrypt messages.
        key = str(key)[:16].ljust(16, '0')
        message = input("| Type your message (secure): ")
        encrypted_message = encrypt_message(key, message)                   # AES encryption.
        client_socket.send(json.dumps({"encrypted message": encrypted_message}).encode())
        print(f"| Secure: {user} => {username} >> {message} |")
        log_message(user, username, message, secure)
    else:
        message = input("| Type your message (unsecure): ")
        print(f"| Unsecure: {user} => {username} >> {message} |")
        client_socket.send(json.dumps({"unencrypted message": message}).encode())
        log_message(user, username, message, secure)
    client_socket.close()

def log_message(user, username, message, secure):   #0
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if secure == 'yes' or secure =='y': state = "secure" 
    else: state = "unsecure"
    with open(LOG_FILE, 'a') as log:
        log.write(f"| {timestamp} | {user} >>    sent to    >> {username} | {state} message >> {message} |\n")

def display_history():  #3
    with open(LOG_FILE, 'r') as log:
        print(log.read())

def chat_initiator(user):               #9
    while True:
        user_input = input("| Type | 'Users' to view online users | 'Chat' to start chatting | 'History' to view chat history | Input is not case sensitive for this line |").strip().lower()
        if user_input == "users":       #1
            display_users()
        elif user_input == "chat":      #2
            initiate_chat(user)
        elif user_input == "history":   #3
            display_history()
        else:
            print("| Invalid input. Try 'Users', 'Chat', or 'History' |")

if __name__ == "__main__":              #9        
    chat_initiator()