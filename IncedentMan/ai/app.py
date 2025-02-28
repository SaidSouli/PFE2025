from flask import Flask, request, jsonify
import joblib
from incident_classifier import IncidentClassifier
import json

app = Flask(__name__)

# Load the trained models
try:
    classifier = IncidentClassifier()
    # Fix: Updated attribute names to match the IncidentClassifier class
    classifier.category_pipeline = joblib.load('models/category_classifier.joblib')
    classifier.priority_pipeline = joblib.load('models/priority_classifier.joblib')

    with open('models/model_metadata.json', 'r') as f:
        model_metadata = json.load(f)
except Exception as e:
    print(f"Error loading models: {type(e).__name__}: {str(e)}")
    import os
    print(f"Current working directory: {os.getcwd()}")
    print("Please ensure models are trained before running the API.")
    exit(1)

@app.route('/health', methods=['GET'])
def health_check():
    """Basic health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_training_date': model_metadata['training_date']
    })

@app.route('/predict', methods=['POST'])
def predict_incident():
    """Endpoint for incident classification"""
    try:
        data = request.get_json()
        
        if not data or 'description' not in data:
            return jsonify({
                'error': 'Missing incident description',
                'required_format': {
                    'description': 'text description of the security incident'
                }
            }), 400
        
        prediction = classifier.predict(data['description'])
        
        return jsonify({
            'input_description': data['description'],
            'prediction': prediction,
            'model_info': {
                'training_date': model_metadata['training_date'],
                'performance_metrics': model_metadata['performance_metrics']
            }
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Prediction error: {str(e)}'
        }), 500

@app.route('/metrics', methods=['GET'])
def get_metrics():
    """Endpoint to get model performance metrics"""
    return jsonify({
        'training_date': model_metadata['training_date'],
        'dataset_stats': model_metadata['dataset_stats'],
        'performance_metrics': model_metadata['performance_metrics']
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)



