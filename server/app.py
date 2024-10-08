from flask import Flask, request, jsonify
import joblib
import re
import numpy as np
from flask_cors import CORS
import pandas as pd
from urllib.parse import urlparse
from web3 import Web3
import os

app = Flask(__name__)
CORS(app)
model = joblib.load('.\\server\\ann_model-new.pkl')

# Connect to Polygon via Web3 (replace with your provider)
infura_api_key = os.getenv('INFURA_API_KEY')
provider_url = f"https://polygon-mainnet.infura.io/v3/{infura_api_key}"
web3 = Web3(Web3.HTTPProvider(provider_url))

contract_address = Web3.to_checksum_address("0x45b47d4a68babd0286ab3ee75bbcd23986516760")
contract_abi = [
    {
        "inputs": [{"internalType": "string", "name": "url", "type": "string"}],
        "name": "addUrl",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "index", "type": "uint256"}],
        "name": "urlEntries",
        "outputs": [
            {"internalType": "string", "name": "url", "type": "string"},
            {"internalType": "uint256", "name": "timestamp", "type": "uint256"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "getUrlCount",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
]

private_key = os.getenv('PRIVATE_KEY')
account_address = web3.eth.account.from_key(private_key).address

contract = web3.eth.contract(address=contract_address, abi=contract_abi)

def preprocess(url):
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname or ''
    path = parsed_url.path or ''
    query = parsed_url.query or ''

    features = {
        'NumDots': [url.count('.')],
        'SubdomainLevel': [len(hostname.split('.')) - 2],
        'PathLevel': [len(path.split('/')) - 1],
        'UrlLength': [len(url)],
        'NumDash': [url.count('-')],
        'NumDashInHostname': [hostname.count('-')],
        'AtSymbol': [1 if '@' in url else 0],
        'TildeSymbol': [1 if '~' in url else 0],
        'NumUnderscore': [url.count('_')],
        'NumPercent': [url.count('%')],
        'NumAmpersand': [url.count('&')],
        'NumHash': [url.count('#')],
        'NumNumericChars': [len(re.findall(r'\d', url))],
        'NoHttps': [1 if parsed_url.scheme != 'https' else 0],
        'IpAddress': [1 if re.match(r'^\d{1,3}(\.\d{1,3}){3}$', hostname) else 0],
        'DomainInSubdomains': [1 if 'domain' in hostname.split('.')[:-2] else 0],
        'DomainInPaths': [1 if 'domain' in path.split('/') else 0],
        'HttpsInHostname': [1 if 'https' in hostname else 0],
        'HostnameLength': [len(hostname)],
        'PathLength': [len(path)],
        'QueryLength': [len(query)],
        'DoubleSlashInPath': [1 if '//' in path else 0],
        'EmbeddedBrandName': [1 if 'brandname' in url else 0]
    }
    
    return pd.DataFrame(features)

def is_url_blocked(url):
    try:
        url_count = contract.functions.getUrlCount().call()
        for i in range(url_count):
            entry = contract.functions.urlEntries(i).call()
            if entry[0] == url:
                return True
        return False
    except Exception as e:
        print(f"Error checking URL in contract: {e}")
        return False

def add_url_to_block(url):
    try:
        nonce = web3.eth.get_transaction_count(account_address)
        transaction = contract.functions.addUrl(url).build_transaction({
            'gas': 2000000,
            'gasPrice': web3.to_wei('50', 'gwei'),
            'nonce': nonce,
            'from': account_address
        })
        signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        web3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"URL {url} added to block successfully")
    except Exception as e:
        print(f"Error adding URL to block: {e}")


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    url = data.get('url')
    
    if url is None:
        return jsonify({'message': 'URL is required'}), 400

    if is_url_blocked(url):
        return jsonify({'message': 'URL is already blocked', 'isFake': True})

    features = preprocess(url)
    prediction = model.predict(features)
    is_fake = not bool(prediction[0])

    if not is_fake:
        add_url_to_block(url)

    result = {
        'isFake': is_fake
    }
    print(result)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
