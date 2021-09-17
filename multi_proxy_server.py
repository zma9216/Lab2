import socket, time, sys
from multiprocessing import Process

# TO-DO: get_remote_ip() method

# TO-DO: handle_request() method

def main():
    # Establish localhost, extern_host (Google), port, and buffer size
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start: # Establish "start" of proxy (connects to localhost)
        # TO-DO: bind, and set to listening mode

        while True:
            # TO-DO: Accept incoming connections from proxy_start and print information about connection

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end: # Establish "end" of proxy (connects to Google)
                # TO-DO: Get remote IP of Google and connect proxy_end to it

                # Multiprocessing...

                # TO-DO: Allow for multiple connections with Process daemon
                # Set target = handle_request

            # TO-DO: Close the connection
