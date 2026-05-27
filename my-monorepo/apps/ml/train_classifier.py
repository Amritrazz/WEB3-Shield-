import os
import pandas as pd
from sklearn.model_selection import train_test_split
import xgboost as xgb
from feature_engineering import transform_dataframe

def execute_classifier_pipeline():
    print("[ML Pipeline] Loading cached data splits...")
    csv_path = 'data/raw/phishtank_latest.csv'
    
    if not os.path.exists(csv_path):
        print("⚠️ Data files missing. Running collection script first...")
        from data.collect_phishtank import download_phishtank
        download_phishtank()

    df = pd.read_csv(csv_path)
    
    # If using the live phishtank download, explicitly flag everything as phishing
    if 'is_phishing' not in df.columns:
        df['is_phishing'] = 1
        # Append safe baseline sites for counter balance balance
        safe_df = pd.DataFrame({
            'url': ['https://google.com', 'https://github.com', 'https://ethereum.org', 'https://uniswap.org'],
            'is_phishing': [0, 0, 0, 0]
        })
        df = pd.concat([df[['url', 'is_phishing']], safe_df], ignore_index=True)
    
    print("[ML Pipeline] Transforming text components into numerical arrays...")
    X = transform_dataframe(df, 'url')
    y = df['is_phishing']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    
    print("[ML Pipeline] Compiling gradient boosted XGBoost structural model...")
    classifier = xgb.XGBClassifier(
        objective='binary:logistic',
        max_depth=4,
        learning_rate=0.1,
        n_estimators=50,
        eval_metric='logloss'
    )
    classifier.fit(X_train, y_train)
    
    os.makedirs('models', exist_ok=True)
    classifier.save_model('models/phishing_classifier.json')
    print("[ML Pipeline] Success! Model binary saved to: models/phishing_classifier.json")
    
    X_test.to_csv('data/X_test.csv', index=False)
    y_test.to_csv('data/y_test.csv', index=False)

if __name__ == '__main__':
    execute_classifier_pipeline()