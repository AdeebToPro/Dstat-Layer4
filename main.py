import os
import socket
import threading
import requests
import time
import signal

Tcp_Connection_PerSecond = 0
Udp_Connection_PerSecond = 0

def get_public_ip():
    response = requests.get('https://api.ipify.org')
    return response.text

public_ip = get_public_ip()

def reset_counters():
    global Tcp_Connection_PerSecond, Udp_Connection_PerSecond
    while True:
        Tcp_Connection_PerSecond = 0
        Udp_Connection_PerSecond = 0
        time.sleep(1)

def tcp_server(port):
    global Tcp_Connection_PerSecond
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(1)

    while True:
        client, addr = server.accept()
        Tcp_Connection_PerSecond += 1

def udp_server(port):
    global Udp_Connection_PerSecond
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('0.0.0.0', port))

    while True:
        data, addr = server.recvfrom(1024)
        Udp_Connection_PerSecond += 1

def print_stats():  # Print
    os.system('cls' if os.name == 'nt' else 'clear')
    print('''
 /$$                                               /$$   /$$ /$$$$$$$             /$$                /$$    
| $$                                              | $$  | $$| $$__  $$           | $$               | $$    
| $$        /$$$$$$  /$$   /$$  /$$$$$$   /$$$$$$ | $$  | $$| $$  \ $$  /$$$$$$$/$$$$$$   /$$$$$$  /$$$$$$  
| $$       |____  $$| $$  | $$ /$$__  $$ /$$__  $$| $$$$$$$$| $$  | $$ /$$_____/_  $$_/  |____  $$|_  $$_/  
| $$        /$$$$$$$| $$  | $$| $$$$$$$$| $$  \__/|_____  $$| $$  | $$|  $$$$$$  | $$     /$$$$$$$  | $$    
| $$       /$$__  $$| $$  | $$| $$_____/| $$            | $$| $$  | $$ \____  $$ | $$ /$$/$$__  $$  | $$ /$$
| $$$$$$$$|  $$$$$$$|  $$$$$$$|  $$$$$$$| $$            | $$| $$$$$$$/ /$$$$$$$/ |  $$$$/  $$$$$$$  |  $$$$/
|________/ \_______/ \____  $$ \_______/|__/            |__/|_______/ |_______/   \___/  \_______/   \___/  
                     /$$  | $$                                                                              
                    |  $$$$$$/                                                                              
                     \______/                                                                               
''')
    print("------------------------------------------------------------------")
    print(f"Public Ip Listening On {public_ip}:{port}")
    print(f"Private Ip Listening On {socket.gethostbyname(socket.gethostname())}:{port}")
    print(f"-----------------------------------------------------------------")
    print(f"tcp connecting: {Tcp_Connection_PerSecond}")
    print(f"udp connecting: {Udp_Connection_PerSecond}")
    print()
    time.sleep(1)


def handle_signals(signum, frame):
    if signum == signal.SIGINT or signum == signal.SIGTSTP or signum == signal.SIGQUIT:
        print("\nThank For Using This Code. Exiting...")
        os._exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, handle_signals)
signal.signal(signal.SIGTSTP, handle_signals)
signal.signal(signal.SIGQUIT, handle_signals)


if __name__ == '__main__':
    port = int(input("Enter the port number: "))

    # Start reset thread
    reset_thread = threading.Thread(target=reset_counters)
    reset_thread.start()

    # Start TCP server in a separate thread
    tcp_thread = threading.Thread(target=tcp_server, args=(port,))
    tcp_thread.start()

    # Start UDP server in a separate thread
    udp_thread = threading.Thread(target=udp_server, args=(port,))
    udp_thread.start()

    while True:
        print_stats()

