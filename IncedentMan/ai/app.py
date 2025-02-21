from flask import Flask, request, jsonify
import joblib
import numpy as np
from typing import Dict, Any
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

app = Flask(__name__)

# Download required NLTK resources
def download_nltk_resources():
    """Download required NLTK resources with error handling"""
    resources = ['stopwords', 'wordnet', 'punkt']
    for resource in resources:
        try:
            nltk.download(resource, quiet=True)
        except Exception as e:
            print(f"Warning: Could not download {resource}: {str(e)}")

# Initialize preprocessing components
download_nltk_resources()
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
tokenizer = RegexpTokenizer(r'\w+')

def preprocess_text(text):
    """Preprocess text using the same steps as the training pipeline"""
    if not text:
        return ""
    text = str(text).lower()
    tokens = tokenizer.tokenize(text)
    tokens = [lemmatizer.lemmatize(token) for token in tokens 
             if token not in stop_words and len(token) > 1]
    return ' '.join(tokens)

# Load models
try:
    category_model = joblib.load('models/enhanced_category_classifier.joblib')
    priority_model = joblib.load('models/enhanced_priority_classifier.joblib')
    # Try to load subcategory model if it exists
    try:
        subcategory_model = joblib.load('models/enhanced_subcategory_classifier.joblib')
        has_subcategory = True
    except FileNotFoundError:
        has_subcategory = False
except FileNotFoundError as e:
    print(f"Error loading models: {e}")
    raise

def check_security_terms(text: str) -> Dict[str, Any]:
    """Check for security-related terms in the incident description"""
    security_terms = ['breach', 'hack', 'malware', 'ransom', 'phish', 'compromise', 
                     'unauthor', 'hijack', 'suspicious', 'threat']
    
    text_lower = text.lower()
    detected_terms = [term for term in security_terms if term in text_lower]
    
    result = {}
    if 'hijack' in text_lower or len(detected_terms) >= 2:
        result['security_alert'] = True
        result['detected_security_terms'] = detected_terms
        
        # Override priority to high if security issue detected
        if 'hijack' in text_lower or len(detected_terms) >= 3:
            result['priority_override'] = 4
            result['override_reason'] = "Security keywords detected, priority elevated"
    
    return result

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

        # Preprocess the input text
        processed_description = preprocess_text(description)
        
        # Get predictions with confidence scores
        category_probs = category_model.predict_proba([processed_description])[0]
        priority_probs = priority_model.predict_proba([processed_description])[0]
        
        predicted_category = category_model.predict([processed_description])[0]
        predicted_priority = int(priority_model.predict([processed_description])[0])
        
        # Create confidence score dictionaries
        category_scores = {
            str(cat): float(prob) 
            for cat, prob in zip(category_model.classes_, category_probs)
        }
        
        priority_scores = {
            str(pri): float(prob)
            for pri, prob in zip(priority_model.classes_, priority_probs)
        }
        
        # Initialize response
        response = {
            'category': predicted_category,
            'category_confidence': category_scores,
            'priority': predicted_priority,
            'priority_confidence': priority_scores,
            'processed_text': processed_description
        }
        
        # Add subcategory prediction if model exists
        if has_subcategory:
            subcategory_probs = subcategory_model.predict_proba([processed_description])[0]
            predicted_subcategory = subcategory_model.predict([processed_description])[0]
            subcategory_scores = {
                str(subcat): float(prob)
                for subcat, prob in zip(subcategory_model.classes_, subcategory_probs)
            }
            response['subcategory'] = predicted_subcategory
            response['subcategory_confidence'] = subcategory_scores
            
        # Check for security terms and add to response
        security_info = check_security_terms(description)
        if security_info:
            response.update(security_info)
            if 'priority_override' in security_info:
                response['priority'] = security_info['priority_override']
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'error': f'Prediction error: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)