'''
BankNetCoin.

Usage:
  mybanknetcoin.py serve 
  mybanknetcoin.py ping 
  mybanknetcoin.py balance <name>
  mybanknetcoin.py tx <from> <to> <amount>
  

Options:
  -h --help     Show this screen.
  
'''


import uuid
import socketserver
import socket
import sys
from copy import deepcopy
from ecdsa import SigningKey, SECP256k1
from utils import serialize, deserialize
from identities import user_public_key
from docopt import docopt


def spend_message(tx, index):
    tx_in = tx.tx_ins[index]
    outpoint = tx_in.outpoint

    return serialize(outpoint) + serialize(tx.tx_outs)


class Tx:

    def __init__(self, id, tx_ins, tx_outs):
        self.id = id
        self.tx_ins = tx_ins
        self.tx_outs = tx_outs

    def sign_input(self, index, private_key):
        message = spend_message(self, index)
        signature = private_key.sign(message)
        self.tx_ins[index].signature = signature

    def verify_input(self, index, public_key):
        tx_in = self.tx_ins[index]
        message = spend_message(self, index)

        return public_key.verify(tx_in.signature, message)


class TxIn:

    def __init__(self, tx_id, index, signature=None):
        self.tx_id = tx_id
        self.index = index
        self.signature = signature

    @property
    def outpoint(self):
        return (self.tx_id, self.index)


class TxOut:

    def __init__(self, tx_id, index, amount, public_key):
        self.tx_id = tx_id
        self.index = index
        self.amount = amount
        self.public_key = public_key

    @property
    def outpoint(self):
        return (self.tx_id, self.index)


class Bank:

    def __init__(self):
        self.utxo = {}

    def update_utxo(self, tx):
        for tx_out in tx.tx_outs:
            self.utxo[tx_out.outpoint] = tx_out
        for tx_in in tx.tx_ins:
            del self.utxo[tx_in.outpoint]

    def issue(self, amount, public_key):
        id_ = str(uuid.uuid4())
        tx_ins = []
        tx_outs = [TxOut(tx_id=id_, index=0, amount=amount,
                         public_key=public_key)]
        tx = Tx(id=id_, tx_ins=tx_ins, tx_outs=tx_outs)

        self.update_utxo(tx)

        return tx

    def validate_tx(self, tx):
        in_sum = 0
        out_sum = 0

        for index, tx_in in enumerate(tx.tx_ins):
            tx_out = self.utxo[tx_in.outpoint]

            # Verify signature using public key of TxOut we're spending
            public_key = tx_out.public_key
            tx.verify_input(index, public_key)

            # Sum up the total inputs
            amount = tx_out.amount
            in_sum += amount

        for tx_out in tx.tx_outs:
            out_sum += tx_out.amount

    def handle_tx(self, tx):
        # Save to self.utxo if it's valid
        self.validate_tx(tx)
        self.update_utxo(tx)

    def fetch_utxo(self, public_key):
        return [utxo for utxo in self.utxo.values()
                if utxo.public_key == public_key]

    def fetch_balance(self, public_key):
        # Fetch utxo associated with this public key
        unspents = self.fetch_utxo(public_key)
        # Sum the amounts
        return sum([tx_out.amount for tx_out in unspents])


def prepare_message(command, data):
    return {
        "command": command,
        "data": data
    }


# networking code
host = "0.0.0.0"
port = 10000
bank = Bank()
address = (host, port)


class MyTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


class TCPHandler(socketserver.BaseRequestHandler):
    def respond(self, command, data):
        response = prepare_message(command, data)
        serialized_response = serialize(response)
        self.request.sendall(serialized_response)

    def handle(self):
        message_data = self.request.recv(5000).strip()
        message = deserialize(message_data)
        command = message["command"]

        print(f"got a message {message}")

        if command == "ping":
            self.respond("ping", "")
        elif command == "balance":
            public_key = message["data"]
            balance = bank.fetch_balance(public_key)
            self.respond("balance-response", balance)
        elif commmand == "tx":
            ```


def serve():
    server = MyTCPServer(address, TCPHandler)
    server.serve_forever()


def send_message(command, data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    message = prepare_message(command, data)
    serialized_message = serialize(message)
    sock.sendall(serialized_message)

    message_data = sock.recv(5000)
    message = deserialize(message_data)
    print(f"data recieved: {message}")


def main(args):
    if args["serve"]:
        alice_public_key = user_public_key("alice")
        bank.issue(1000, alice_public_key)
        serve()
    elif args["ping"]:
        send_message("ping", "")
    elif args["balance"]:
        name = args["<name>"]
        public_key = user_public_key(name)
        send_message("balance", public_key)
    elif arg['tx']:
        ```
    else:
        print("invalid command ")


if __name__ == "__main__":
    # print(__doc__)
    args = docopt(__doc__)

    main(args)
