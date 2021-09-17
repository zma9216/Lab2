import socket, time, sys
from multiprocessing import Process

# Define global address and buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024


# Get IP
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print('Hostname could not be resolved. Exiting')
        sys.exit()

    print(f'Ip address of {host} is {remote_ip}')
    return remote_ip


def handle_request(addr, conn, end_proxy):
    print("Connected by ", addr)

    send_full_data = conn.recv(BUFFER_SIZE)
    print(f"Sending received data {send_full_data} to Google")
    end_proxy.sendall(send_full_data)
    end_proxy.shutdown(socket.SHUT_WR)

    data = end_proxy.recv(BUFFER_SIZE)
    print(f"Sending received data {data} to client")
    conn.send(data)


def main():
    # Establish extern_host (Google) and port
    extern_host = "www.google.com"
    extern_port = 80

    with socket.socket(socket.AF_INET,
                       socket.SOCK_STREAM) as proxy_start:  # Establish "start" of proxy (connects to localhost)
        # Bind, and set to listening mode
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind((HOST, PORT))
        proxy_start.listen(1)

        while True:
            # Accept incoming connections from proxy_start and print information about connection
            conn, addr = proxy_start.accept()

            with socket.socket(socket.AF_INET,
                               socket.SOCK_STREAM) as proxy_end:  # Establish "end" of proxy (connects to Google)
                # Get remote IP of Google and connect proxy_end to it
                print("Connecting to Google")
                remote_ip = get_remote_ip(extern_host)
                proxy_end.connect((remote_ip, extern_port))

                # Allow for multiple connections with Process daemon
                p = Process(target=handle_request, args=(addr, conn, proxy_end))  # Set target = handle_request
                p.daemon = True
                p.start()
                print("Started process ", p)

            # Close the connection
            conn.close()


if __name__ == "__main__":
    main()
