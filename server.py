import socket
import threading
import rsa

class Server:

    def __init__(self, port: int) -> None:
        self.host = '127.0.0.1'
        self.port = port
        self.clients = {}
        self.username_lookup = {}
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def start(self):
        self.s.bind((self.host, self.port))
        self.s.listen(100)

        public, private = rsa.generate_public_and_private_keys()

        while True:
            c, addr = self.s.accept()
            username = c.recv(1024).decode()
            print(f"{username} tries to connect")
            self.broadcast(f'new person has joined: {username}')
            self.username_lookup[c] = username
            # send public key to the client

            c.send((",".join([str(key) for key in public])).encode())

            # receive client keys and save them

            client_keys_encoded = c.recv(1024).decode()
            client_keys = [int(key) for key in rsa.decode(private, client_keys_encoded).split(",")]
            print(client_keys)
            self.clients[c] = client_keys  # save keys as (e, n, d)

            threading.Thread(target=self.handle_client,args=(c,addr,)).start()

    def broadcast(self, msg: str):
        for client in self.clients:

            # encrypt the message

            # ...

            client.send(msg.encode())

    def handle_client(self, c: socket, addr):
        while True:
            msg = c.recv(1024)

            for client in self.clients:
                if client != c:
                    client.send(msg)

if __name__ == "__main__":
    s = Server(9001)
    s.start()
