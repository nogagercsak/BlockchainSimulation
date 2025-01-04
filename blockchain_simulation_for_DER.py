import hashlib
import time
import random
from flask import Flask, jsonify, request
from numpy.random import laplace

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Test successful!"})

class Blockchain:
    def __init__(self):
        self.chain = []
        self.nodes = {}  # Dictionary to store DER nodes
        self.blacklist = set()  # Set to track malicious nodes
        self.create_block(cert_data="Genesis Block", previous_hash="0")

    def create_block(self, cert_data, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'data': cert_data,
            'previous_hash': previous_hash,
            'hash': self.hash_block(cert_data, previous_hash),
        }
        self.chain.append(block)
        return block

    def hash_block(self, cert_data, previous_hash):
        block_string = f"{cert_data}{previous_hash}{time.time()}".encode()
        return hashlib.sha256(block_string).hexdigest()

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            if self.chain[i]['previous_hash'] != self.chain[i - 1]['hash']:
                return False
        return True

    def add_node(self, node_id, role):
        """Add a DER node with a role (producer, consumer, or certificate authority)."""
        self.nodes[node_id] = {"role": role, "certificates": []}

    def issue_certificate(self, node_id, cert_data):
        """Issue a certificate for a node with differential privacy."""
        if node_id not in self.nodes:
            return {"error": "Node not found"}
        if node_id in self.blacklist:
            return {"error": "Node is blacklisted for malicious activity"}

        # Add differential privacy using Laplace noise
        noise = laplace(loc=0, scale=1)
        cert_data += f"_noise_{noise}"
        new_block = self.create_block(cert_data=cert_data, previous_hash=self.chain[-1]['hash'])
        self.nodes[node_id]["certificates"].append(new_block)
        return new_block

    def simulate_attack(self, attack_type):
        """Simulate attacks like replay attacks, DDoS, or certificate spoofing."""
        if attack_type == "replay":
            last_block = self.chain[-1]
            response = self.create_block(cert_data=last_block['data'], previous_hash=last_block['hash'])
            is_valid = self.is_chain_valid()
            return {"attack": "Replay Attack", "block_added": response, "chain_valid": is_valid}
        elif attack_type == "spoofing":
            fake_node_id = "FakeNode"
            fake_cert_data = "FakeCertificate"
            response = self.issue_certificate(fake_node_id, fake_cert_data)
            return {"attack": "Certificate Spoofing", "response": response}
        elif attack_type == "ddos":
            start_time = time.time()
            for _ in range(1000):  # Simulate high transaction volume
                self.create_block(cert_data=f"Noise_{random.randint(1, 1000)}", previous_hash=self.chain[-1]['hash'])
            end_time = time.time()
            return {"attack": "DDoS", "time_taken": end_time - start_time, "blocks_added": len(self.chain)}
        return {"error": "Unknown attack type"}

    def rollback_chain(self, block_index):
        """Rollback the blockchain to a previous stable state."""
        if block_index < len(self.chain):
            self.chain = self.chain[:block_index]
            return {"status": "Rollback Successful", "new_chain_length": len(self.chain)}
        return {"error": "Invalid block index"}

    def measure_recovery(self, attack_type):
        """Measure recovery time and validate chain after an attack."""
        start_time = time.time()
        attack_response = self.simulate_attack(attack_type)
        recovery_time = time.time() - start_time
        is_valid = self.is_chain_valid()
        return {
            "attack_type": attack_type,
            "attack_response": attack_response,
            "recovery_time": recovery_time,
            "chain_valid": is_valid
        }

# Initialize Blockchain
blockchain = Blockchain()

# Add some DER nodes
blockchain.add_node("Node1", "producer")
blockchain.add_node("Node2", "consumer")
blockchain.add_node("Node3", "certificate_authority")

# Flask APIs
@app.route('/chain', methods=['GET'])
def get_chain():
    return jsonify(blockchain.chain)

@app.route('/issue_certificate/<node_id>', methods=['POST'])
def issue_certificate(node_id):
    data = request.get_json()
    cert_data = data.get("cert_data")
    response = blockchain.issue_certificate(node_id, cert_data)
    return jsonify(response)

@app.route('/simulate_attack/<attack_type>', methods=['GET'])
def simulate_attack(attack_type):
    response = blockchain.simulate_attack(attack_type)
    return jsonify(response)

@app.route('/rollback/<int:block_index>', methods=['POST'])
def rollback_chain(block_index):
    response = blockchain.rollback_chain(block_index)
    return jsonify(response)

@app.route('/validate', methods=['GET'])
def validate_chain():
    is_valid = blockchain.is_chain_valid()
    return jsonify({"is_valid": is_valid})

@app.route('/measure_recovery/<attack_type>', methods=['GET'])
def measure_recovery(attack_type):
    response = blockchain.measure_recovery(attack_type)
    return jsonify(response)

@app.route('/block/<int:index>', methods=['GET'])
def get_block(index):
    if 0 <= index < len(blockchain.chain):  # Ensure the index is valid
        return jsonify(blockchain.chain[index])
    else:
        return jsonify({"error": "Block index out of range"}), 400

# Run Flask App
if __name__ == '__main__':
    app.run(debug=True)
