import zmq
import random
from threading import Thread

import sys
import time

# run command is :
#  - python3 pub_server_sending.py tcp://127.0.0.1:5566
#  or this :
# - python3 pub_server_sending.py tcp://*:5566


class PubServer:
    # constructor of TrackerPubServer .
    def __init__(self, pub_address):
        self.socket(pub_address)

    # create socket that bind pub address
    def socket(self, pub_address: str):
        # create zeroMQ socket .
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.bind(pub_address)
        print(f"Socket pub created to bind to : {pub_address}")

        # wiat for 3 second before start sending thread.
        print("wait for 3 second before start binding ...")
        time.sleep(3)

        # run json pub sender in new thread
        pub_threading = Thread(target=self.while_loop_pub_server(socket))
        pub_threading.start()

    # create random json to send by tcp .
    def random_json(self):
        random_number = random.randint(1, 10)
        json_value = {
            "x1": random_number + 1,
            "x2": random_number + 5,
            "y1": random_number + 3,
            "y2": random_number + 2,
        }
        return json_value

    # loop to send
    def while_loop_pub_server(self, socket: zmq.Context.socket):
        while True:
            json_value = self.random_json()

            # send json message (will receive it as Unit8List in dart )
            socket.send_json(json_value)
            print(f"sending : Message (' {json_value} ') sended.")
            # wait second before send json again
            time.sleep(1)


if __name__ == "__main__":
    assert (
        len(sys.argv) > 2,
        AssertionError(
            "Must be run python3 <file_name> <address> like this : python3 pub_tracker.py tcp://127.0.0.1:5566"
        ),
    )

    # run main pub server .
    pub_server = PubServer(sys.argv[1])
