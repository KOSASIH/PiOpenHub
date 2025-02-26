import socket
import threading
import json

class Peer:
    def __init__(self, address):
        self.address = address

    def __repr__(self):
        return f"Peer({self.address})"

class Network:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.peers = []
        self.server = None

    def start_server(self):
        """Start the server to listen for incoming connections."""
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        print(f"Server started at {self.host}:{self.port}")

        while True:
            client_socket, addr = self.server.accept()
            print(f"Connection from {addr} established.")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        """Handle incoming messages from clients."""
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if not message:
                    break
                self.process_message(message)
            except Exception as e:
                print(f"Error handling client: {e}")
                break
        client_socket.close()

    def process_message(self, message):
        """Process incoming messages."""
        data = json.loads(message)
        print(f"Received message: {data}")

    def add_peer(self, peer_address):
        """Add a new peer to the network."""
        peer = Peer(peer_address)
        self.peers.append(peer)
        print(f"Added peer: {peer}")

    def broadcast(self, message):
        """Broadcast a message to all peers."""
        for peer in self.peers:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.connect(peer.address)
                    sock.sendall(json.dumps(message).encode())
            except Exception as e:
                print(f"Error sending message to {peer}: {e}")

# Example usage
if __name__ == "__main__":
    network = Network()

    # Start the server in a separate thread
    threading.Thread(target=network.start_server, daemon=True).start()

    # Add peers (for demonstration purposes, you can add actual peer addresses)
    network.add_peer(('127.0.0.1', 5001))
    network.add_peer(('127.0.0.1', 5002))

    # Broadcast a message
    network.broadcast({"type": "new_block", "data": "Block data here"})
