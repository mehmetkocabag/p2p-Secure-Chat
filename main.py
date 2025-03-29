import threading
from peer_discovery import peer_discovery
from service_announcer import service_announcer
from chat_responder import chat_responder
from chat_initiator import chat_initiator
import time 


username = input("| **Peer2Peer Chat** | \n| Please specify your username: ")
service_announcer_thread = threading.Thread(target=service_announcer, args=(username,))
service_announcer_thread.start()
time.sleep(1)
peer_discovery_thread = threading.Thread(target=peer_discovery)
peer_discovery_thread.start()
time.sleep(1)
chat_responder_thread = threading.Thread(target=chat_responder, args=(username,))
chat_responder_thread.start()

chat_initiator_thread = threading.Thread(target=chat_initiator, args=(username,))
chat_initiator_thread.start()