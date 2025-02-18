from flask import Flask, request, jsonify
import joblib
import numpy as np
from typing import Dict, Any

app = Flask(__name__)


try:
    category_model = joblib.load('models/category_classifier.joblib')
    priority_model = joblib.load('models/priority_classifier.joblib')
except FileNotFoundError as e:
    print(f"Error loading models: {e}")
    raise

@app.route('/predict', methods=['POST'])
def predict() -> Dict[str, Any]:
    try:
        data = request.get_json() 
        if not data or 'description' not in data:
            return jsonify({
                'error': 'Missing description in request'
            }), 400
            
        description = data['description']
        
        
        if not isinstance(description, str) or not description.strip():
            return jsonify({
                'error': 'Description must be a non-empty string'
            }), 400

        
        predicted_category = category_model.predict([description])[0]
        predicted_priority = int(priority_model.predict([description])[0])
        
        return jsonify({
            'category': predicted_category,
            'priority': predicted_priority
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Prediction error: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)