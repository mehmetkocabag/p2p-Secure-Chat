import socket
import json
import time
from service_announcer import get_local_ip
peers_file = "peers.txt"                                              

def update_peers_file(peers):      #0                                         
    with open(peers_file, 'w') as file:
        for ip, info in peers.items():
            file.write(f"{ip} {info['username']} {info['timestamp']}\n")

def peer_discovery():          #1                                             
    port=6000
    peers = {}                                                              # Dictionary for peers information
    discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    discovery_socket.bind(('', port))
    discovery_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    discovery_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    print(f"| Listening for peers | Port: {port} |")

    while True:
        message, addr = discovery_socket.recvfrom(1024)
        message.decode()                                         #
        data = json.loads(message)
        ip = addr[0]
        username = data['username']
        timestamp = time.time()
        if ip in peers:                                          # Check if ip exists in dictionary
            if peers[ip]['username'] == username:                # Check if the same ip(computer) is using a new name
                peers[ip]['timestamp'] = timestamp 
            else:                                                # Same ip(computer) restarted app and using a new name
                oldname = peers[ip]['username']                  # Save old name to variable
                peers[ip]['username'] = username                 # Update name
                peers[ip]['timestamp'] = timestamp     
                print(f"\n >{oldname}< changed their name to >{username}< ")
        else:                                                       
            peers[ip] = {'username': username, 'timestamp': timestamp}      # New ip, add to dictionary. # It will also listen to its own announer calls because of LAN broadcast.
            if ip != get_local_ip():                             # Wont get notified by own online status.
                print(f"\n| {username} is online |")          
        update_peers_file(peers)

if __name__ == "__main__":      #1
    peer_discovery()