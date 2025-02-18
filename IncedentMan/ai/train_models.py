import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt
import seaborn as sns


os.makedirs('models', exist_ok=True)

def train_classifiers():
    
    print("Loading data...")
    df = pd.read_csv('data/incident_data.csv')
    
    # Basic data exploration
    print(f"Dataset shape: {df.shape}")
    print(f"\nCategory distribution:\n{df['category'].value_counts()}")
    print(f"\nPriority distribution:\n{df['priority'].value_counts()}")
    
    # Split data
    print("\nSplitting data into train and test sets...")
    X_train, X_test, y_train_cat, y_test_cat = train_test_split(
        df['description'],
        df['category'],
        test_size=0.2,
        random_state=42,
        stratify=df['category']
    )
    
    _, _, y_train_pri, y_test_pri = train_test_split(
        df['description'],
        df['priority'],
        test_size=0.2,
        random_state=42,
        stratify=df['priority']
    )
    
    # Create and train the category classifier pipeline
    print("\nTraining category classifier...")
    category_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1, 2), stop_words='english')),
        ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    
    category_pipeline.fit(X_train, y_train_cat)
    
    # Create and train the priority classifier pipeline
    print("\nTraining priority classifier...")
    priority_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1, 2), stop_words='english')),
        ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    
    priority_pipeline.fit(X_train, y_train_pri)
    
    # Evaluate category classifier
    print("\nEvaluating category classifier...")
    y_pred_cat = category_pipeline.predict(X_test)
    cat_report = classification_report(y_test_cat, y_pred_cat, output_dict=True)
    print(classification_report(y_test_cat, y_pred_cat))
    
    # Visualize category confusion matrix
    plt.figure(figsize=(10, 8))
    cm = confusion_matrix(y_test_cat, y_pred_cat)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=sorted(df['category'].unique()),
                yticklabels=sorted(df['category'].unique()))
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix - Categories')
    plt.tight_layout()
    plt.savefig('models/category_confusion_matrix.png')
    plt.close()
    
    # Evaluate priority classifier
    print("\nEvaluating priority classifier...")
    y_pred_pri = priority_pipeline.predict(X_test)
    pri_report = classification_report(y_test_pri, y_pred_pri, output_dict=True)
    print(classification_report(y_test_pri, y_pred_pri))
    
    # Visualize priority confusion matrix
    plt.figure(figsize=(10, 8))
    cm = confusion_matrix(y_test_pri, y_pred_pri)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Greens',
                xticklabels=sorted(df['priority'].unique()),
                yticklabels=sorted(df['priority'].unique()))
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix - Priorities')
    plt.tight_layout()
    plt.savefig('models/priority_confusion_matrix.png')
    plt.close()
    
    # Save models and reports
    print("\nSaving models and performance reports...")
    joblib.dump(category_pipeline, 'models/category_classifier.joblib')
    joblib.dump(priority_pipeline, 'models/priority_classifier.joblib')
    
    # Save performance metrics
    pd.DataFrame(cat_report).transpose().to_csv('models/category_performance.csv')
    pd.DataFrame(pri_report).transpose().to_csv('models/priority_performance.csv')
    
    # Feature importance for category classifier
    tfidf_cat = category_pipeline.named_steps['tfidf']
    clf_cat = category_pipeline.named_steps['clf']
    feature_names = tfidf_cat.get_feature_names_out()
    
    # Get top features for each category
    print("\nTop features for each category:")
    for i, category in enumerate(sorted(df['category'].unique())):
        top_indices = np.argsort(clf_cat.feature_importances_)[-10:]
        top_features = [feature_names[j] for j in top_indices]
        print(f"\n{category}: {', '.join(top_features)}")
    
    print("\nTraining complete! Models saved in the 'models' directory.")

if __name__ == "__main__":
    train_classifiers()