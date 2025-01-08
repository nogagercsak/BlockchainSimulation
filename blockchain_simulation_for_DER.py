import hashlib
import time
import random
from flask import Flask, jsonify, request
from numpy.random import laplace
import matplotlib
matplotlib.use('Agg')  # Set Matplotlib to use a non-GUI backend
import matplotlib.pyplot as plt


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
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Recompute the hash of the previous block
            recalculated_previous_hash = self.hash_block(
                cert_data=previous_block['data'],
                previous_hash=previous_block['previous_hash']
            )

            # Check if the stored hash matches the recalculated hash
            if previous_block['hash'] != recalculated_previous_hash:
                return False

            # Check if the previous_hash of the current block matches the hash of the previous block
            if current_block['previous_hash'] != previous_block['hash']:
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

        # Measure the transaction time before adding noise
        tx_start = time.perf_counter()  # Start timing the transaction
        
        # Add differential privacy using Laplace noise
        noise = laplace(loc=0, scale=1)  # Adjust 'scale' for noise level
        noisy_cert_data = cert_data + f"_noise_{noise}"
        
        # Create the block
        new_block = self.create_block(cert_data=noisy_cert_data, previous_hash=self.chain[-1]['hash'])
        self.nodes[node_id]["certificates"].append(new_block)
        
        tx_end = time.perf_counter()  # End timing the transaction
        
        # Measure transaction speed
        transaction_time = tx_end - tx_start
        block_size = len(noisy_cert_data)  # Block size after adding noise
        
        return new_block, transaction_time, block_size


    def simulate_attack(self, attack_type):
        """Simulate attacks like replay attacks, DDoS, or certificate spoofing."""
        if attack_type == "replay":
            last_block = self.chain[-1]
            response = self.create_block(cert_data=last_block['data'], previous_hash=last_block['hash'])
            is_valid = self.is_chain_valid()
            return {"attack": "Replay Attack", "block_added": response, "chain_valid": is_valid}
        elif attack_type == "spoofing":
            fake_node_id = f"FakeNode_{random.randint(1, 100)}"  # Unique ID for each malicious node
            fake_cert_data = "FakeCertificate"
            self.nodes[fake_node_id] = {"role": "malicious", "certificates": []}  # Add to malicious nodes
            response = self.issue_certificate(fake_node_id, fake_cert_data)
            return {"attack": "Certificate Spoofing", "response": response}
        elif attack_type == "ddos":
            transaction_times = []
            start_time = time.perf_counter()  # Start timing the attack

            # Process 1,000 transactions
            for _ in range(1000):
                tx_start = time.perf_counter()  # Start timing this transaction
                self.create_block(cert_data=f"Noise_{random.randint(1, 1000)}", previous_hash=self.chain[-1]['hash'])
                tx_end = time.perf_counter()  # End timing this transaction
                transaction_times.append(tx_end - tx_start)  # Record processing time for this transaction

            end_time = time.perf_counter()  # End timing the attack
            total_time = end_time - start_time
            avg_tx_time = sum(transaction_times) / len(transaction_times)

            # Measure real recovery time
            recovery_start = time.perf_counter()
            while True:
                recovery_tx_start = time.perf_counter()
                self.create_block(cert_data="Recovery Test", previous_hash=self.chain[-1]['hash'])
                recovery_tx_end = time.perf_counter()
                recovery_tx_time = recovery_tx_end - recovery_tx_start
                
                # Break the loop when processing time stabilizes to normal
                if recovery_tx_time <= avg_tx_time * 1.2:  # 20% tolerance for "normal" time
                    break

            recovery_end = time.perf_counter()
            recovery_time = recovery_end - recovery_start

            return {
                "attack": "DDoS",
                "total_time": total_time,
                "average_transaction_time": avg_tx_time,
                "transactions_processed": len(transaction_times),
                "recovery_time": recovery_time,
                "transaction_times": transaction_times
            }
        return {"error": "Unknown attack type"}

    def rollback_chain(self, block_index):
        """Rollback the blockchain to a previous stable state."""
        if block_index < len(self.chain):
            self.chain = self.chain[:block_index]
            return {"status": "Rollback Successful", "new_chain_length": len(self.chain)}
        return {"error": "Invalid block index"}

    def measure_recovery(self, attack_type):
        """Measure recovery time and validate chain after an attack."""
        start_time = time.perf_counter()
        attack_response = self.simulate_attack(attack_type)
        recovery_time = time.perf_counter() - start_time
        is_valid = self.is_chain_valid()
        return {
            "attack_type": attack_type,
            "attack_response": attack_response,
            "recovery_time": recovery_time,
            "chain_valid": is_valid
        }
    def get_node_activity(self):
        legitimate_count = sum(1 for node in self.nodes.values() if node["role"] in ["producer", "consumer"])
        malicious_count = sum(1 for node in self.nodes.values() if node["role"] == "malicious")
        total_nodes = legitimate_count + malicious_count
        return {
            "total_nodes": total_nodes,
            "legitimate_count": legitimate_count,
            "malicious_count": malicious_count,
            "legitimate_percentage": (legitimate_count / total_nodes) * 100 if total_nodes > 0 else 0,
            "malicious_percentage": (malicious_count / total_nodes) * 100 if total_nodes > 0 else 0
        }

# Initialize Blockchain
blockchain = Blockchain()

# Add some DER nodes
blockchain.add_node("Node1", "producer")
blockchain.add_node("Node2", "consumer")
blockchain.add_node("Node3", "certificate_authority")

# Data Visualization

# Define the blockchain data function
def get_blockchain_data():
    # Example: return a simple list of blocks or data from your actual blockchain
    blockchain = [
        {"block": 1, "data": "Block 1 data"},
        {"block": 2, "data": "Block 2 data"},
        # Add more blocks here or retrieve from your storage
    ]
    return blockchain


# Idenitfy and visualize node acitivity 

def visualize_node_activity_distribution(node_activity):
    labels = ["Legitimate Nodes", "Malicious Nodes"]
    sizes = [node_activity["legitimate_count"], node_activity["malicious_count"]]
    colors = ["green", "red"]
    explode = (0.1, 0)  # Highlight malicious nodes
    
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct="%1.1f%%", shadow=True, startangle=140)
    plt.title("Node Activity Distribution")
    
    # Save the plot
    plot_path = "static/node_activity_distribution.png"
    plt.savefig(plot_path)
    plt.close()
    return plot_path


# Function to visualize the blockchain growth
def visualize_chain_growth(blockchain):
    # Create a plot of blockchain growth using real data
    plt.figure(figsize=(10, 6))
    
    # Extract block numbers and data length from the blockchain
    block_numbers = [block['index'] for block in blockchain.chain]  # Using 'index' for block number
    block_data = [len(block['data']) for block in blockchain.chain]  # Data length from 'data'

    # Plot the growth (block number vs. data length in the block)
    plt.plot(block_numbers, block_data)

    # Set labels and title for better clarity
    plt.xlabel('Block Number')
    plt.ylabel('Block Data Size')
    plt.title('Blockchain Growth Visualization')

    # Save the plot as an image
    plot_path = 'static/chain_growth.png'
    plt.savefig(plot_path)  # Save the plot as a file
    plt.close()  # Close the plot to free memory

    # Return the path to the saved image
    return plot_path


    # Save the plot to a file@app.route('/visualize/chain_growth', methods=['GET'])
def visualize_chain():
    plot_path = visualize_chain_growth(blockchain)
    return jsonify({"message": "Chain growth visualization rendered", "image_path": plot_path})

    plot_path = "/path/to/save/chain_growth.png"
    plt.savefig(plot_path)  # Save the plot to a file
    plt.close()  # Close the plot to free up memory

    return plot_path

# Collect data for plotting
transaction_times = []
block_sizes = []
noise_levels = []

# Simulate multiple certificates being issued
for i in range(100):  # You can adjust the number of iterations
    cert_data = f"Certificate {i}"
    block, transaction_time, block_size = blockchain.issue_certificate("Node1", cert_data)
    
    # Track the data
    transaction_times.append(transaction_time)
    block_sizes.append(block_size)
    noise_levels.append(abs(laplace(loc=0, scale=1)))  # Track the magnitude of the noise added

def plot_transaction_performance(transaction_times, block_sizes, noise_levels):
    plt.figure(figsize=(10, 6))
    
    # Scatter plot for block size vs noise level
    plt.subplot(1, 2, 1)
    plt.scatter(noise_levels, block_sizes, color='blue', alpha=0.5)
    plt.title("Noise Level vs Block Size")
    plt.xlabel("Noise Level")
    plt.ylabel("Block Size (bytes)")

    # Scatter plot for transaction time vs noise level
    plt.subplot(1, 2, 2)
    plt.scatter(noise_levels, transaction_times, color='red', alpha=0.5)
    plt.title("Noise Level vs Transaction Time")
    plt.xlabel("Noise Level")
    plt.ylabel("Transaction Time (seconds)")

    # Save the plot
    plot_path = 'static/privacy_performance_plot.png'
    plt.tight_layout()  # Adjust layout for clarity
    plt.savefig(plot_path)
    plt.close()

    return plot_path


def visualize_attack_recovery(metrics):
    attack_types = [metric['attack_type'] for metric in metrics]
    recovery_times = [metric['recovery_time'] for metric in metrics]

    plt.figure(figsize=(10, 6))
    plt.bar(attack_types, recovery_times, color='skyblue')
    plt.title("Attack Recovery Times")
    plt.xlabel("Attack Type")
    plt.ylabel("Recovery Time (seconds)")

    # Save the plot as an image
    plot_path = 'static/attack_recovery.png'
    plt.savefig(plot_path)
    plt.close()

    return plot_path

def visualize_node_activity(blockchain):
    roles = [data['role'] for node, data in blockchain.nodes.items()]
    legitimate_count = roles.count("producer") + roles.count("consumer")
    malicious_count = roles.count("malicious")  # Simulated attack nodes

    labels = ['Legitimate Nodes', 'Malicious Nodes']
    sizes = [legitimate_count, malicious_count]
    colors = ['green', 'red']
    explode = (0.1, 0)  # explode malicious nodes for emphasis

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title("Node Activity Distribution")

    # Save the plot as an image
    plot_path = 'static/node_activity.png'
    plt.savefig(plot_path)
    plt.close()

    return plot_path


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
    
@app.route('/visualize/chain_growth')
def visualize_chain_growth_route():
    # Fetch real blockchain data directly from the blockchain instance
    plot_path = visualize_chain_growth(blockchain)  # Visualize using actual blockchain data
    return jsonify({"image_url": plot_path})  # Return the image path as JSON

@app.route('/visualize/attack_recovery', methods=['POST'])
def visualize_recovery():
    metrics = request.get_json().get('metrics')
    plot_path = visualize_attack_recovery(metrics)
    return jsonify({"message": "Attack recovery visualization rendered", "image_url": plot_path})

@app.route('/visualize/node_activity', methods=['GET'])
def visualize_nodes():
    plot_path = visualize_node_activity(blockchain)
    return jsonify({"message": "Node activity visualization rendered", "image_url": plot_path})

@app.route("/node_activity", methods=["GET"])
def node_activity():
    node_activity = blockchain.get_node_activity()
    plot_path = visualize_node_activity_distribution(node_activity)
    node_activity["visualization_path"] = plot_path
    return jsonify(node_activity)

@app.route('/visualize/privacy_performance', methods=['GET'])
def visualize_privacy_performance():
    # Call the function to generate the plot
    plot_path = plot_transaction_performance(transaction_times, block_sizes, noise_levels)
    return jsonify({"message": "Privacy performance visualization rendered", "image_url": plot_path})

# Run Flask App
if __name__ == '__main__':
    app.run(debug=True)
