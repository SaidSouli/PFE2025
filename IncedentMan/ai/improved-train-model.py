import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline
import joblib
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import os
from datetime import datetime
import json

def download_nltk_resources():
    """Download required NLTK resources"""
    resources = ['stopwords', 'wordnet', 'punkt']
    for resource in resources:
        try:
            nltk.download(resource, quiet=True)
        except Exception as e:
            print(f"Warning: Could not download {resource}: {str(e)}")

class IncidentClassifier:
    def __init__(self):
        download_nltk_resources()
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.category_pipeline = None
        self.subcategory_pipeline = None
        self.priority_pipeline = None
        self.metadata = {
            'training_date': None,
            'dataset_stats': {},
            'performance_metrics': {}
        }
        
    def preprocess_text(self, text):
        """Preprocess text data"""
        if pd.isna(text):
            return ""
        text = str(text).lower()
        tokens = self.tokenizer.tokenize(text)
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens 
                 if token not in self.stop_words and len(token) > 1]
        return ' '.join(tokens)
    
    def create_pipeline(self, model_type='category'):
        """Create an optimized pipeline based on model type"""
        if model_type == 'category':
            return Pipeline([
                ('tfidf', TfidfVectorizer(
                    max_features=12000,
                    ngram_range=(1, 3),
                    stop_words='english',
                    min_df=2,
                    use_idf=True,
                    sublinear_tf=True
                )),
                ('clf', RandomForestClassifier(
                    n_estimators=200,
                    max_depth=25,
                    min_samples_split=5,
                    min_samples_leaf=2,
                    random_state=42,
                    class_weight='balanced',
                    n_jobs=-1
                ))
            ])
        elif model_type == 'subcategory':
            return Pipeline([
                ('tfidf', TfidfVectorizer(
                    max_features=15000,
                    ngram_range=(1, 3),
                    stop_words='english',
                    min_df=2,
                    use_idf=True,
                    sublinear_tf=True
                )),
                ('clf', RandomForestClassifier(
                    n_estimators=250,
                    max_depth=30,
                    min_samples_split=4,
                    min_samples_leaf=1,
                    random_state=42,
                    class_weight='balanced',
                    n_jobs=-1
                ))
            ])
        else:  # priority pipeline
            return Pipeline([
                ('tfidf', TfidfVectorizer(
                    max_features=10000,
                    ngram_range=(1, 2),
                    stop_words='english',
                    min_df=2,
                    use_idf=True
                )),
                ('clf', RandomForestClassifier(
                    n_estimators=180,
                    max_depth=20,
                    min_samples_split=4,
                    min_samples_leaf=2,
                    random_state=42,
                    class_weight='balanced',
                    n_jobs=-1
                ))
            ])
    
    def train(self, data_file, train_subcategory=True):
        """Train the incident classification models"""
        try:
            # Create output directory
            os.makedirs('models', exist_ok=True)
            
            # Load and preprocess data
            print(f"Loading data from {data_file}...")
            df = pd.read_csv(data_file)
            
            # Save basic dataset statistics
            self.metadata['dataset_stats'] = {
                'total_incidents': len(df),
                'category_counts': df['category'].value_counts().to_dict(),
                'priority_counts': df['priority'].value_counts().to_dict()
            }
            
            if 'subcategory' in df.columns:
                self.metadata['dataset_stats']['subcategory_counts'] = df['subcategory'].value_counts().to_dict()
            
            print("Preprocessing text data...")
            df['processed_description'] = df['description'].apply(self.preprocess_text)
            
            # Split data
            X = df['processed_description']
            y_category = df['category']
            y_priority = df['priority']
            
            if train_subcategory and 'subcategory' in df.columns:
                y_subcategory = df['subcategory']
                X_train, X_test, y_train_cat, y_test_cat, y_train_sub, y_test_sub, y_train_pri, y_test_pri = train_test_split(
                    X, y_category, y_subcategory, y_priority,
                    test_size=0.2,
                    random_state=42,
                    stratify=y_category
                )
            else:
                X_train, X_test, y_train_cat, y_test_cat, y_train_pri, y_test_pri = train_test_split(
                    X, y_category, y_priority,
                    test_size=0.2,
                    random_state=42,
                    stratify=y_category
                )
            
            # Train category classifier
            print("\nTraining category classifier...")
            self.category_pipeline = self.create_pipeline('category')
            self.category_pipeline.fit(X_train, y_train_cat)
            
            # Evaluate category classifier
            y_pred_cat = self.category_pipeline.predict(X_test)
            cat_report = classification_report(y_test_cat, y_pred_cat, output_dict=True)
            print("\nCategory Classification Report:")
            print(classification_report(y_test_cat, y_pred_cat))
            
            # Store performance metrics
            self.metadata['performance_metrics']['category'] = {
                'accuracy': cat_report['accuracy'],
                'macro_avg_f1': cat_report['macro avg']['f1-score'],
                'weighted_avg_f1': cat_report['weighted avg']['f1-score']
            }
            
            # Train subcategory classifier if requested
            if train_subcategory and 'subcategory' in df.columns:
                print("\nTraining subcategory classifier...")
                self.subcategory_pipeline = self.create_pipeline('subcategory')
                self.subcategory_pipeline.fit(X_train, y_train_sub)
                
                # Evaluate subcategory classifier
                y_pred_sub = self.subcategory_pipeline.predict(X_test)
                sub_report = classification_report(y_test_sub, y_pred_sub, output_dict=True)
                print("\nSubcategory Classification Report:")
                print(classification_report(y_test_sub, y_pred_sub))
                
                self.metadata['performance_metrics']['subcategory'] = {
                    'accuracy': sub_report['accuracy'],
                    'macro_avg_f1': sub_report['macro avg']['f1-score'],
                    'weighted_avg_f1': sub_report['weighted avg']['f1-score']
                }
            
            # Train priority classifier
            print("\nTraining priority classifier...")
            self.priority_pipeline = self.create_pipeline('priority')
            self.priority_pipeline.fit(X_train, y_train_pri)
            
            # Evaluate priority classifier
            y_pred_pri = self.priority_pipeline.predict(X_test)
            pri_report = classification_report(y_test_pri, y_pred_pri, output_dict=True)
            print("\nPriority Classification Report:")
            print(classification_report(y_test_pri, y_pred_pri))
            
            self.metadata['performance_metrics']['priority'] = {
                'accuracy': pri_report['accuracy'],
                'macro_avg_f1': pri_report['macro avg']['f1-score'],
                'weighted_avg_f1': pri_report['weighted avg']['f1-score']
            }
            
            # Save models
            print("\nSaving models...")
            joblib.dump(self.category_pipeline, 'models/enhanced_category_classifier.joblib')
            joblib.dump(self.priority_pipeline, 'models/enhanced_priority_classifier.joblib')
            if train_subcategory and 'subcategory' in df.columns and self.subcategory_pipeline:
                joblib.dump(self.subcategory_pipeline, 'models/enhanced_subcategory_classifier.joblib')
            
            # Save metadata
            self.metadata['training_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open('models/model_metadata.json', 'w') as f:
                json.dump(self.metadata, f, indent=2)
            
            print("Training completed successfully!")
            
        except Exception as e:
            print(f"An error occurred during training: {str(e)}")
            raise
    
    def predict(self, text):
        """Make predictions for new incident descriptions"""
        if not self.category_pipeline or not self.priority_pipeline:
            raise ValueError("Models not trained. Please train the models first.")
        
        processed_text = self.preprocess_text(text)
        
        # Get category prediction and probabilities
        category = self.category_pipeline.predict([processed_text])[0]
        category_probs = self.category_pipeline.predict_proba([processed_text])[0]
        category_scores = {cat: float(prob) for cat, prob in 
                         zip(self.category_pipeline.classes_, category_probs)}
        
        # Get subcategory prediction if model exists
        subcategory = None
        subcategory_scores = {}
        if self.subcategory_pipeline:
            subcategory = self.subcategory_pipeline.predict([processed_text])[0]
            subcategory_probs = self.subcategory_pipeline.predict_proba([processed_text])[0]
            subcategory_scores = {subcat: float(prob) for subcat, prob in 
                               zip(self.subcategory_pipeline.classes_, subcategory_probs)}
        
        # Get priority prediction and probabilities
        priority = int(self.priority_pipeline.predict([processed_text])[0])
        priority_probs = self.priority_pipeline.predict_proba([processed_text])[0]
        priority_scores = {str(pri): float(prob) for pri, prob in 
                         zip(self.priority_pipeline.classes_, priority_probs)}
        
        result = {
            'category': category,
            'category_confidence': category_scores,
            'priority': priority,
            'priority_confidence': priority_scores,
            'processed_text': processed_text
        }
        
        if subcategory:
            result['subcategory'] = subcategory
            result['subcategory_confidence'] = subcategory_scores
        
        # Check for security-related terms
        security_terms = ['breach', 'hack', 'malware', 'ransom', 'phish', 'compromise', 
                         'unauthor', 'hijack', 'suspicious', 'threat']
        
        text_lower = text.lower()
        detected_terms = [term for term in security_terms if term in text_lower]
        
        if 'hijack' in text_lower or len(detected_terms) >= 2:
            result['security_alert'] = True
            result['detected_security_terms'] = detected_terms
            
            if priority < 3 and ('hijack' in text_lower or len(detected_terms) >= 3):
                result['priority_override'] = 4
                result['override_reason'] = "Security keywords detected, priority elevated"
        
        return result

if __name__ == "__main__":
    # Check if data file exists
    data_file = 'data/enhanced_incident_data.csv'
    if not os.path.exists(data_file):
        print(f"Error: Could not find {data_file}")
        print("Please ensure the training data file exists.")
        exit(1)
    
    # Train models
    classifier = IncidentClassifier()
    classifier.train(data_file, train_subcategory=True)