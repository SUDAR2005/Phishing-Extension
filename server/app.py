from flask import Flask,request,jsonify
import joblib
import re
import numpy as np
from flask_cors import CORS
import pandas as pd
app=Flask(__name__)
CORS(app)
model=joblib.load('.\\server\\ann_model.pkl')

def preprocess(url):
    features = {
        'NoOfAmpersandInURL':[url.count('&')],
        'NoOfLettersInURL':[len(re.findall(r'[a-zA-Z]', url))],
        'NoOfDegitsInURL':[len(re.findall(r'\d', url))],
        'ObfuscationRatio':[len(re.findall(r'[!@#$%^&*(),.?":{}|<>]', url)) / len(url) if len(url) > 0 else 0],
        'URLTitleMatchScore':[0],
        'NoOfOtherSpecialCharsInURL':[len(re.findall(r'[^a-zA-Z0-9&=]', url))],
        'NoOfEqualsInURL':[url.count('=')]
    }
    
    return pd.DataFrame(features)

@app.route('/predict',methods=['POST'])
def predict():
    data=request.get_json()
    url=data['url']
    features=preprocess(url)
    prediction=model.predict(features)
    result={
        'isFake':bool(prediction[0])
    }
    print(result)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True,port=5000)
