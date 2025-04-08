from flask import Flask, request, jsonify
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from bson.dbref import DBRef
from flask_cors import CORS
import logging
import os


logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  


def get_db_connection():
    mongo_uri = os.environ.get('MONGO_URI', 'mongodb://root:example@mongo:27017/usersdb?authSource=admin')
    try:
        client = MongoClient(mongo_uri)
        db = client['usersdb']
        logger.info("Successfully connected to MongoDB")
        return db
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        return None


def find_similar_incidents(new_incident, top_n=3):
    db = get_db_connection()
    if db is None:
        return []
    
    try:
        incidents = list(db.incidents.find())
        solutions = list(db.solutions.find())
        
        logger.info(f"Retrieved {len(incidents)} incidents and {len(solutions)} solutions")
        
        if not incidents:
            return []
        
        # Prepare data for similarity comparison
        incident_texts = []
        for incident in incidents:
            title = incident.get('title', '')
            description = incident.get('description', '')
            category = incident.get('category', '')
            text = f"{title} {description} {category}"
            incident_texts.append(text)
        
        # Add the new incident text
        new_incident_text = f"{new_incident.get('title', '')} {new_incident.get('description', '')} {new_incident.get('category', '')}"
        all_texts = incident_texts + [new_incident_text]
        
        # Calculate TF-IDF vectors
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(all_texts)
        
        # Calculate similarity between new incident and existing incidents
        new_incident_vector = tfidf_matrix[-1]
        incident_vectors = tfidf_matrix[:-1]
        similarity_scores = cosine_similarity(new_incident_vector, incident_vectors).flatten()
        
        # Get top N similar incidents
        similar_indices = similarity_scores.argsort()[-top_n:][::-1]
        
        # Prepare response with similar incidents and their solutions
        results = []
        for idx in similar_indices:
            if similarity_scores[idx] > 0.05:  # Threshold for relevance
                incident = incidents[idx]
                incident_id = incident.get('_id')
                
                # Find solutions for this incident
                incident_solutions = []
                for sol in solutions:
                    sol_incident = sol.get('incident')
                    
                    # Handle DBRef object - Spring Data MongoDB references
                    if isinstance(sol_incident, DBRef) and str(sol_incident.id) == str(incident_id):
                        incident_solutions.append(sol)
                
                result = {
                    'incident': {
                        'id': str(incident.get('_id')),
                        'title': incident.get('title'),
                        'description': incident.get('description'),
                        'category': incident.get('category'),
                        'status': incident.get('status')
                    },
                    'solutions': [{
                        'id': str(sol.get('_id')),
                        'description': sol.get('description'),
                        'creation_date': sol.get('creationDate')
                    } for sol in incident_solutions],
                    'similarity_score': float(similarity_scores[idx])
                }
                results.append(result)
        
        return results
    except Exception as e:
        logger.error(f"Error finding similar incidents: {e}")
        return []

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

@app.route('/similar-incidents', methods=['POST'])
def get_similar_incidents():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        top_n = data.get('top_n', 3)
        results = find_similar_incidents(data, top_n)
        
        return jsonify({
            'success': True,
            'similar_incidents': results
        })
    
    except Exception as e:
        logger.error(f"Error finding similar incidents: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/suggest-solution', methods=['POST'])
def suggest_solution():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        similar_incidents = find_similar_incidents(data, top_n=1)
        
        if not similar_incidents:
            return jsonify({
                'success': True,
                'message': 'No similar incidents found',
                'suggestion': None
            })
        
        most_similar = similar_incidents[0]
        solutions = most_similar.get('solutions', [])
        
        if not solutions:
            return jsonify({
                'success': True,
                'message': 'Similar incident found but no solutions available',
                'incident': most_similar['incident'],
                'suggestion': None
            })
        
        # If multiple solutions, return the most recent one
        best_solution = sorted(solutions, key=lambda x: x.get('creation_date', ''), reverse=True)[0]
        
        return jsonify({
            'success': True,
            'incident': most_similar['incident'],
            'suggestion': best_solution,
            'similarity_score': most_similar['similarity_score']
        })
        
    except Exception as e:
        logger.error(f"Error suggesting solution: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/all-incidents', methods=['GET'])
def get_all_incidents():
    db = get_db_connection()
    if db is None:
        return jsonify({'success': False, 'error': 'Database connection failed'}), 500
    
    try:
        incidents = list(db.incidents.find())
        result = []
        
        for incident in incidents:
            result.append({
                'id': str(incident.get('_id')),
                'title': incident.get('title', ''),
                'description': incident.get('description', ''),
                'category': incident.get('category', ''),
                'status': incident.get('status', '')
            })
        
        return jsonify({'success': True, 'incidents': result})
    
    except Exception as e:
        logger.error(f"Error retrieving incidents: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)