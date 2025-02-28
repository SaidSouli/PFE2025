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

class IncidentClassifier:
    def __init__(self):
        """Initialize the incident classifier with necessary NLP tools"""
        # Download required NLTK resources
        for resource in ['stopwords', 'wordnet', 'punkt']:
            try:
                nltk.download(resource, quiet=True)
            except Exception as e:
                print(f"Warning: Could not download {resource}: {str(e)}")
        
        # Initialize NLP tools
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.tokenizer = RegexpTokenizer(r'\w+')
        
        # Initialize model pipelines
        self.category_pipeline = None
        self.priority_pipeline = None
        
        # Initialize metadata storage
        self.metadata = {
            'training_date': None,
            'dataset_stats': {},
            'performance_metrics': {}
        }

    def preprocess_text(self, text):
        """Preprocess incident description text"""
        if pd.isna(text):
            return ""
        
        # Convert to string and lowercase
        text = str(text).lower()
        
        # Tokenize and lemmatize
        tokens = self.tokenizer.tokenize(text)
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens 
                 if token not in self.stop_words and len(token) > 1]
        
        return ' '.join(tokens)

    def create_pipeline(self, model_type='category'):
        """Create ML pipeline based on classification type"""
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

    def train(self, data_files):
        """
        Train the incident classification models
        
        Args:
            data_files: str or list of str, paths to CSV files containing incident data
                       Each CSV should have columns: description, category, priority
        """
        try:
            # Create output directory
            os.makedirs('models', exist_ok=True)
            
            # Load and combine all data files
            print("Loading and combining data...")
            if isinstance(data_files, str):
                data_files = [data_files]
            
            dfs = []
            for file in data_files:
                if os.path.exists(file):
                    df = pd.read_csv(file)
                    dfs.append(df)
                else:
                    print(f"Warning: File not found: {file}")
            
            if not dfs:
                raise ValueError("No valid data files found")
            
            df = pd.concat(dfs, ignore_index=True)
            
            # Save dataset statistics
            self.metadata['dataset_stats'] = {
                'total_incidents': len(df),
                'category_counts': df['category'].value_counts().to_dict(),
                'priority_counts': df['priority'].value_counts().to_dict()
            }
            
            # Preprocess text
            print("Preprocessing text data...")
            df['processed_description'] = df['description'].apply(self.preprocess_text)
            
            # Prepare data for training
            X = df['processed_description']
            y_category = df['category']
            y_priority = df['priority']
            
            # Split data
            X_train, X_test, y_train_cat, y_test_cat, y_train_pri, y_test_pri = \
                train_test_split(X, y_category, y_priority,
                               test_size=0.2, random_state=42, stratify=y_category)
            
            # Train models
            print("\nTraining category classifier...")
            self.category_pipeline = self.create_pipeline('category')
            self.category_pipeline.fit(X_train, y_train_cat)
            
            print("Training priority classifier...")
            self.priority_pipeline = self.create_pipeline('priority')
            self.priority_pipeline.fit(X_train, y_train_pri)
            
            # Evaluate models
            print("\nEvaluating models...")
            self._evaluate_models(X_test, y_test_cat, y_test_pri)
            
            # Save models and metadata
            print("\nSaving models...")
            joblib.dump(self.category_pipeline, 'models/category_classifier.joblib')
            joblib.dump(self.priority_pipeline, 'models/priority_classifier.joblib')
            
            self.metadata['training_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open('models/model_metadata.json', 'w') as f:
                json.dump(self.metadata, f, indent=2)
            
            print("Training completed successfully!")
            
        except Exception as e:
            print(f"An error occurred during training: {str(e)}")
            raise

    def _evaluate_models(self, X_test, y_test_cat, y_test_pri):
        """Evaluate model performance and store metrics"""
        def get_metrics(y_true, y_pred):
            report = classification_report(y_true, y_pred, output_dict=True)
            return {
                'accuracy': report['accuracy'],
                'macro_avg_f1': report['macro avg']['f1-score'],
                'weighted_avg_f1': report['weighted avg']['f1-score']
            }
        
        # Evaluate each model
        y_pred_cat = self.category_pipeline.predict(X_test)
        y_pred_pri = self.priority_pipeline.predict(X_test)
        
        # Store metrics
        self.metadata['performance_metrics'] = {
            'category': get_metrics(y_test_cat, y_pred_cat),
            'priority': get_metrics(y_test_pri, y_pred_pri)
        }
        
        # Print reports
        print("\nCategory Classification Report:")
        print(classification_report(y_test_cat, y_pred_cat))
        print("\nPriority Classification Report:")
        print(classification_report(y_test_pri, y_pred_pri))

    def predict(self, text):
        """Make predictions for new incident descriptions"""
        if not all([self.category_pipeline, self.priority_pipeline]):
            raise ValueError("Models not trained. Please train the models first.")
        
        processed_text = self.preprocess_text(text)
        
        # Get predictions and probabilities
        category = self.category_pipeline.predict([processed_text])[0]
        category_probs = self.category_pipeline.predict_proba([processed_text])[0]
        priority = int(self.priority_pipeline.predict([processed_text])[0])
        priority_probs = self.priority_pipeline.predict_proba([processed_text])[0]
        
        result = {
            'category': category,
            'category_confidence': {cat: float(prob) for cat, prob in 
                                 zip(self.category_pipeline.classes_, category_probs)},
            'priority': priority,
            'priority_confidence': {str(pri): float(prob) for pri, prob in 
                                 zip(self.priority_pipeline.classes_, priority_probs)},
            'processed_text': processed_text
        }
        
        return result

if __name__ == "__main__":
    # Example usage
    data_files = [
        
        'data/software_incidents.csv',
        'data/hardware_incidents.csv',
        'data/security_incidents.csv',
        'data/network_incidents.csv',
        'data/database_incidents.csv'
        
        
        
        
    ]
    
    classifier = IncidentClassifier()
    classifier.train(data_files)