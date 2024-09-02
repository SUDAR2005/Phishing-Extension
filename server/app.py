from flask import Flask,request,jsonify
import joblib
import re
import numpy as np
from flask_cors import CORS
app=Flask(__name__)
CORS(app)
model=joblib.load('.\\server\\ann_model.pkl')

def preprocess(url):
    features=[]
    features.append(url.count('&'))
    letters_count=len(re.findall(r'[a-zA-Z]',url))
    features.append(letters_count)
    digits_count=len(re.findall(r'\d',url))
    features.append(digits_count)
    special_char_count=len(re.findall(r'[!@#$%^&*(),.?":{}|<>]',url))
    obfuscation_ratio=special_char_count / len(url) if len(url) > 0 else 0
    features.append(obfuscation_ratio)    
    url_title_match_score=0  
    features.append(url_title_match_score)
    other_special_chars=len(re.findall(r'[^a-zA-Z0-9&=]',url))
    features.append(other_special_chars)
    features.append(url.count('='))
    return np.array(features).reshape(1,-1)

@app.route('/predict',methods=['POST'])
def predict():
    data=request.get_json()
    url=data['url']
    features=preprocess(url)
    prediction=model.predict(features)
    result={
        'isFake': bool(prediction[0])
    }
    print(result)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True,port=5000)
