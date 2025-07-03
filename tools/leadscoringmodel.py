

import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder
import joblib

def preprocess_leads(df):
    # Encode title seniority (higher value = more senior)
    seniority_keywords = {
        "founder": 5,
        "chief": 5,
        "vp": 4,
        "head": 4,
        "director": 3,
        "manager": 2,
        "associate": 1
    }
    def get_seniority(title):
        title = title.lower()
        for key, val in seniority_keywords.items():
            if key in title:
                return val
        return 0
    df['title_seniority'] = df['Title'].fillna('').apply(get_seniority)

    # Domain reputation (rule-based: .com=3, .org=2, .xyz/.online=1)
    def get_domain_score(domain):
        if pd.isna(domain): return 0
        domain = domain.lower()
        if domain.endswith('.com'): return 3
        if domain.endswith('.org') or domain.endswith('.net'): return 2
        return 1
    df['domain_score'] = df['Domain'].apply(get_domain_score)

    # Email confidence (already verified = 1, guessed = 0.5, unknown = 0)
    df['email_confidence'] = df['EmailVerified'].map({'yes': 1, 'no': 0, 'guess': 0.5}).fillna(0)

    # LinkedIn completeness (has LinkedIn link or not)
    df['linkedin_score'] = df['LinkedIn'].apply(lambda x: 1 if isinstance(x, str) and 'linkedin.com' in x else 0)

    return df[['title_seniority', 'domain_score', 'email_confidence', 'linkedin_score']], df['LeadScore']

def train_model(input_csv, model_output_path):
    df = pd.read_csv(input_csv)
    X, y = preprocess_leads(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = GradientBoostingRegressor()
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    rmse = mean_squared_error(y_test, preds) ** 0.5
    print(f"Model trained. RMSE: {rmse:.2f}")

    joblib.dump(model, model_output_path)
    print(f"Model saved to {model_output_path}")

def predict_score(row, model_path):
    model = joblib.load(model_path)
    X, _ = preprocess_leads(pd.DataFrame([row]))
    return model.predict(X)[0]

if __name__ == "__main__":
    mode = input("Choose mode - train (t) or predict (p): ").strip().lower()

    if mode == 't':
        input_file = input("Enter training CSV with labeled LeadScore column: ")
        output_model = input("Enter output model filename (.pkl): ")
        train_model(input_file, output_model)
    elif mode == 'p':
        model_file = input("Enter trained model filename: ")
        title = input("Enter title: ")
        domain = input("Enter domain: ")
        email_verified = input("Enter email verification status (yes/guess/no): ")
        linkedin = input("Enter LinkedIn URL (or leave blank): ")

        test_row = {
            'Title': title,
            'Domain': domain,
            'EmailVerified': email_verified,
            'LinkedIn': linkedin,
            'LeadScore': 0  # Dummy
        }
        score = predict_score(test_row, model_file)
        print(f"Predicted lead score: {score:.2f}")
    else:
        print("Invalid mode selected.")
