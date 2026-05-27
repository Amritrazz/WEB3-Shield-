try:
    import xgboost as xgb
except ImportError as e:
    raise ImportError("xgboost is not installed. Install it with: pip install xgboost") from e

import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix

def run_performance_metrics():
    print("[Evaluation Engine] Reading validation target matrices...")
    try:
        X_test = pd.read_csv('data/X_test.csv')
        y_test = pd.read_csv('data/y_test.csv')
    except FileNotFoundError:
        print("❌ Test logs missing. Run train_classifier.py first!")
        return

    classifier = xgb.XGBClassifier()
    classifier.load_model('models/phishing_classifier.json')
    predictions = classifier.predict(X_test)
    
    print("\n📊 MACHINE LEARNING MODEL PERFORMANCE EVALUATION MATRIX:")
    print("="*60)
    print(classification_report(y_test, predictions))
    print("="*60)
    print("CONFUSION MATRIX LAYOUT:")
    print(confusion_matrix(y_test, predictions))

if __name__ == '__main__':
    run_performance_metrics()