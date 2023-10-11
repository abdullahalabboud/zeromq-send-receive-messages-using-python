import zmq
from threading import Thread

import sys
import time

# run command is :
#  - python3 sub_client_receiving.py tcp://127.0.0.1:5566


class SubClient:
    # constructor
    def __init__(self, sub_address: str):
        self.socket(sub_address)

    # create sub socket
    def socket(self, sub_address: str):
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect(sub_address)

        # set socket options
        socket.setsockopt_string(zmq.SUBSCRIBE, "")

        # run selection sub json message with new thread .
        sub_threading = Thread(target=self.receive_sub_socket(socket))
        sub_threading.start()

    # loop of receiving json from tcp address.
    def receive_sub_socket(self, socket: zmq.Context.socket):
        print("start receiving ...")
        while True:
            # receive json message .
            received_json = socket.recv_json()
            print(f"receiving : Message ('{received_json}') ")


if __name__ == "__main__":
    assert (
        len(sys.argv) > 2,
        AssertionError(
            "Must be run python3 <file_name> <address> like this : python3 sub_selection_rect.py tcp://127.0.0.1:5566"
        ),
    )

    # run main pub tracker .
    sub_client = SubClient(sys.argv[1])
