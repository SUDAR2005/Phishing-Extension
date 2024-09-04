from flask import Flask,request,jsonify
import joblib
import re
import numpy as np
from flask_cors import CORS
import pandas as pd
from urllib.parse import urlparse
app=Flask(__name__)
CORS(app)
model=joblib.load('.\\server\\ann_model-new.pkl')

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
        'DomainInSubdomains': [1 if 'domain' in hostname.split('.')[:-2] else 0],  # Adjust 'domain' accordingly
        'DomainInPaths': [1 if 'domain' in path.split('/') else 0],  # Adjust 'domain' accordingly
        'HttpsInHostname': [1 if 'https' in hostname else 0],
        'HostnameLength': [len(hostname)],
        'PathLength': [len(path)],
        'QueryLength': [len(query)],
        'DoubleSlashInPath': [1 if '//' in path else 0],
        'EmbeddedBrandName': [1 if 'brandname' in url else 0]  # Adjust 'brandname' accordingly
    }
    
    return pd.DataFrame(features)

@app.route('/predict',methods=['POST'])
def predict():
    data=request.get_json()
    url=data['url']
    features=preprocess(url)
    prediction=model.predict(features)
    result={
        'isFake': not bool(prediction[0])
    }
    print(result)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True,port=5000)