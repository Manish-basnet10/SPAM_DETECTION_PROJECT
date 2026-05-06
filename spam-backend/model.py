import pickle
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

DATASET_PATH = Path("data/spam.csv")
MODEL_PATH = Path("model.pkl")


def create_sample_dataset():
    sample_rows = [
        ("ham", "Hey, are we still meeting at 6 pm?"),
        ("spam", "WIN a free iPhone now! Click this link."),
        ("ham", "Please send me the report by tonight."),
        ("spam", "Congratulations! You won 5000 dollars. Claim now."),
        ("ham", "Can you call me when you are free?"),
        ("spam", "Limited time offer! Lowest loan rates guaranteed."),
        ("ham", "Happy birthday! Have a great day."),
        ("spam", "Get cheap meds without prescription. Order now."),
    ]
    sample_df = pd.DataFrame(sample_rows, columns=["label", "message"])
    DATASET_PATH.parent.mkdir(parents=True, exist_ok=True)
    sample_df.to_csv(DATASET_PATH, index=False)
    print(f"Sample dataset created at {DATASET_PATH.resolve()}")


def load_dataset():
    if not DATASET_PATH.exists():
        print("Dataset not found. Creating a small sample dataset first...")
        create_sample_dataset()

    df = pd.read_csv(DATASET_PATH)
    required_columns = {"label", "message"}
    if not required_columns.issubset(df.columns):
        raise ValueError("Dataset must contain columns: label, message")

    df = df.dropna(subset=["label", "message"]).copy()
    df["label"] = df["label"].str.lower().str.strip()
    df["message"] = df["message"].astype(str)
    return df


def train_and_save():
    df = load_dataset()

    x_train, x_test, y_train, y_test = train_test_split(
        df["message"],
        df["label"],
        test_size=0.2,
        random_state=42,
        stratify=df["label"] if df["label"].nunique() > 1 else None,
    )

    vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
    x_train_vec = vectorizer.fit_transform(x_train)
    x_test_vec = vectorizer.transform(x_test)

    model = MultinomialNB()
    model.fit(x_train_vec, y_train)

    predictions = model.predict(x_test_vec)
    accuracy = accuracy_score(y_test, predictions)

    print(f"Model accuracy: {accuracy:.4f}")
    print("Classification report:")
    print(classification_report(y_test, predictions, zero_division=0))

    bundle = {"model": model, "vectorizer": vectorizer}
    with open(MODEL_PATH, "wb") as model_file:
        pickle.dump(bundle, model_file)

    print(f"Model saved to {MODEL_PATH.resolve()}")


if __name__ == "__main__":
    train_and_save()
