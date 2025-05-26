# Blockchain-DP Framework for DER Security

**Enhancing Cybersecurity in DER-Based Smart Grids with Blockchain and Differential Privacy**

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-purple.svg)](https://flask.palletsprojects.com/)
[![Research](https://img.shields.io/badge/Research-UNC%20Charlotte-green.svg)](https://www.charlotte.edu/)

## 🔬 Research Overview

This repository contains the implementation of a novel cybersecurity framework that combines **blockchain technology** and **differential privacy** to protect Distributed Energy Resources (DERs) in smart grid environments. The framework addresses critical security gaps in modern energy infrastructure while maintaining performance suitable for real-world deployment.

### Key Achievements
- **10-100× faster** attack recovery times (18-40μs vs traditional 52s-1.2s)
- **Linear scalability** tested up to 1000 nodes
- **90% performance retention** during DDoS attacks
- **Consistent 0.85s** block creation times

## 🏗️ Architecture

The framework implements a three-tier blockchain architecture:

```
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│ Certificate         │    │ Producer Nodes      │    │ Consumer Nodes      │
│ Authorities         │◄──►│ (Solar, Wind, etc.) │◄──►│ (Storage, Load)     │
│ (Trusted Validators)│    │                     │    │                     │
└─────────────────────┘    └─────────────────────┘    └─────────────────────┘
           │                          │                          │
           └──────────────────────────┼──────────────────────────┘
                                      │
                    ┌─────────────────────────────────────┐
                    │     Blockchain Layer                │
                    │  + Differential Privacy Protection  │
                    └─────────────────────────────────────┘
```

## 🚀 Features

### 🔐 Security
- **Proof-of-Authority (PoA) Consensus**: Lightweight consensus mechanism optimized for DER environments
- **Certificate Management**: Secure, immutable certificate issuance and validation
- **Attack Resilience**: Protection against replay, spoofing, and DDoS attacks
- **Node Blacklisting**: Automatic identification and isolation of malicious nodes

### 🔒 Privacy Protection
- **Laplace Differential Privacy**: Configurable noise injection to protect sensitive energy data
- **Minimal Overhead**: Privacy protection with negligible performance impact
- **Utility Preservation**: Data remains useful for grid operations while protecting individual privacy

### 📊 Performance Monitoring
- **Real-time Metrics**: Transaction latency, block creation times, attack recovery
- **Visualization Tools**: Comprehensive plotting and analysis capabilities
- **Scalability Testing**: Support for testing with varying node counts

### 🛡️ Attack Simulation
- **Replay Attacks**: Duplicate transaction detection and prevention
- **Certificate Spoofing**: Fake node identification and blocking
- **DDoS Simulation**: High-volume transaction stress testing
- **Recovery Measurement**: Automated recovery time analysis

## 📋 Requirements

```
Python 3.7+
Flask 2.0+
NumPy
Matplotlib
Hashlib (built-in)
Time (built-in)
Random (built-in)
```

## 🔧 Installation

1. **Clone the repository**:
```bash
git clone https://github.com/your-username/blockchain-dp-der-security.git
cd blockchain-dp-der-security
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Create static directory** (for visualizations):
```bash
mkdir static
```

4. **Run the application**:
```bash
python app.py
```

The server will start at `http://localhost:5000`

## 📖 API Documentation

### Core Blockchain Operations

#### Get Blockchain
```http
GET /chain
```
Returns the complete blockchain with all blocks.

#### Issue Certificate
```http
POST /issue_certificate/<node_id>
Content-Type: application/json

{
    "cert_data": "Certificate data string"
}
```

#### Validate Chain
```http
GET /validate
```
Validates the integrity of the entire blockchain.

### Security Testing

#### Simulate Attacks
```http
GET /simulate_attack/<attack_type>
```
Supported attack types: `replay`, `spoofing`, `ddos`

#### Measure Recovery
```http
GET /measure_recovery/<attack_type>
```
Measures and returns recovery time after simulated attack.

#### Node Activity Analysis
```http
GET /node_activity
```
Returns statistics on legitimate vs malicious node distribution.

### Visualizations

#### Chain Growth
```http
GET /visualize/chain_growth
```

#### Attack Recovery Analysis
```http
POST /visualize/attack_recovery
Content-Type: application/json

{
    "metrics": [/* recovery metrics array */]
}
```

#### Privacy Performance Impact
```http
GET /visualize/privacy_performance
```

#### Node Activity Distribution
```http
GET /visualize/node_activity
```

## 🧪 Usage Examples

### Basic Blockchain Operations

```python
# Initialize and test the framework
import requests

base_url = "http://localhost:5000"

# Check if server is running
response = requests.get(f"{base_url}/")
print(response.json())

# Get current blockchain state
chain = requests.get(f"{base_url}/chain")
print(f"Blockchain length: {len(chain.json())}")

# Issue a certificate
cert_data = {"cert_data": "Solar Panel Certificate - 5kW"}
response = requests.post(f"{base_url}/issue_certificate/Node1", json=cert_data)
print(response.json())
```

### Security Testing

```python
# Test replay attack resilience
replay_test = requests.get(f"{base_url}/simulate_attack/replay")
print(f"Replay attack result: {replay_test.json()}")

# Test DDoS resilience
ddos_test = requests.get(f"{base_url}/simulate_attack/ddos")
print(f"DDoS recovery time: {ddos_test.json()['recovery_time']}s")

# Measure recovery performance
recovery_metrics = requests.get(f"{base_url}/measure_recovery/spoofing")
print(f"Spoofing recovery: {recovery_metrics.json()}")
```

### Performance Analysis

```python
# Generate chain growth visualization
growth_viz = requests.get(f"{base_url}/visualize/chain_growth")
print(f"Visualization saved: {growth_viz.json()['image_url']}")

# Analyze node activity
node_activity = requests.get(f"{base_url}/node_activity")
print(f"Legitimate nodes: {node_activity.json()['legitimate_percentage']:.1f}%")
```

## 📊 Performance Benchmarks

### Attack Recovery Times
| Attack Type | Recovery Time | Detection Rate |
|-------------|---------------|----------------|
| Replay      | 38.6 μs      | 100%           |
| Spoofing    | 32.8 μs      | 100%           |
| DDoS        | 18 μs        | 100%           |

### Scalability Metrics
| Nodes | Block Time | Transaction Latency | Performance Impact |
|-------|------------|--------------------|--------------------|
| 100   | 0.85s      | 4.98 μs           | Baseline           |
| 500   | 0.86s      | 5.12 μs           | +2.8%              |
| 1000  | 0.87s      | 5.35 μs           | +7.4%              |

### Privacy vs Performance
- **Differential Privacy Overhead**: < 5% performance impact
- **Data Utility Preservation**: 95%+ accuracy maintained
- **Privacy Budget**: ε = 1.0 (configurable)

## 🔬 Research Applications

This framework is designed for research and academic purposes in:

- **Smart Grid Cybersecurity**: Testing security mechanisms for DER environments
- **Blockchain Performance**: Analyzing consensus mechanisms in resource-constrained environments
- **Privacy-Preserving Systems**: Studying differential privacy in critical infrastructure
- **Attack Resilience**: Evaluating recovery mechanisms against various cyber threats

## 📄 Citation

If you use this framework in your research, please cite:

```bibtex
@article{gercsak2025blockchain,
  title={Enhancing Cybersecurity in DER-Based Smart Grids with Blockchain and Differential Privacy},
  author={Gercsak, Noga},
  journal={University of North Carolina at Charlotte},
  year={2025},
  url={https://github.com/your-username/blockchain-dp-der-security}
}
```

## 🤝 Contributing

We welcome contributions to improve the framework! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Areas for Contribution
- **Consensus Mechanisms**: Implement alternative consensus algorithms
- **Attack Vectors**: Add new attack simulation capabilities
- **Performance Optimization**: Improve scalability and efficiency
- **Visualization**: Enhance data visualization and analytics
- **Integration**: Add support for real DER device protocols

## License
This code is made available for academic research purposes only. 
Commercial use, redistribution, or modification requires explicit 
written permission from the author.


## 🔗 Related Work

- [Smart Grid Security Research](https://www.nist.gov/programs-projects/smart-grid-cybersecurity)
- [Blockchain in Energy Systems](https://www.energy.gov/eere/solar/solar-energy-technologies-office)
- [Differential Privacy Applications](https://privacytools.seas.harvard.edu/)

## Contact

**Noga Gercsak**  
Department of Computer Science  
University of North Carolina at Charlotte  
📧 ngercsak@charlotte.edu

---

** Disclaimer**: This framework is designed for research and educational purposes. For production deployment in critical infrastructure, additional security audits and compliance checks are recommended.

**🔍 Keywords**: Blockchain, Differential Privacy, Smart Grid, DER, Cybersecurity, Distributed Energy Resources, IoT Security, Critical Infrastructure Protection
