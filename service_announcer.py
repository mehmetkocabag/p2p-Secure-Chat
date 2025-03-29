import socket
import json
import time

def get_local_ip():         #0
    local_ip_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    local_ip_socket.connect(('255.255.255.255', 1))
    ip = local_ip_socket.getsockname()[0]                                         # Return this computers ip adress.   
    local_ip_socket.close()
    return ip

def service_announcer(username):     #1
    local_ip = get_local_ip()
    broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    message = json.dumps({"username": username, "ip": local_ip})
    print(f"| Broadcasting on LAN as > {username} < | Device ip: {local_ip} |")
    while True:
        broadcast_socket.sendto(message.encode(), ("255.255.255.255", 6000))        # bradcast to LAN port 6000
        time.sleep(8)

if __name__ == "__main__":      #1
    username = input("Please specify your username: ")
    service_announcer(username)