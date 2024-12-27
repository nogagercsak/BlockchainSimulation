import hashlib
import time
import random
from flask import Flask, jsonify, request

app = Flask(__name__)

class Blockchain:
    def __init__(self):
        self.chain = []
        self.nodes = {}  # Dictionary to store DER nodes
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
        # Add differential privacy (basic noise for simulation purposes)
        cert_data += f"_noise_{random.randint(1, 100)}"
        new_block = self.create_block(cert_data=cert_data, previous_hash=self.chain[-1]['hash'])
        self.nodes[node_id]["certificates"].append(new_block)
        return new_block

    def simulate_attack(self, attack_type):
        """Simulate attacks like replay attacks or certificate spoofing."""
        if attack_type == "replay":
            return {"attack": "Replay Attack", "description": "Resending a valid transaction to disrupt the chain"}
        elif attack_type == "spoofing":
            return {"attack": "Certificate Spoofing", "description": "Issuing a fake certificate"}
        return {"error": "Unknown attack type"}

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

@app.route('/validate', methods=['GET'])
def validate_chain():
    is_valid = blockchain.is_chain_valid()
    return jsonify({"is_valid": is_valid})

# Run Flask App
if __name__ == '__main__':
    app.run(debug=True)
