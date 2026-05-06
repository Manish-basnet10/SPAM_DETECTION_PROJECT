import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Load dataset (Kaggle SMS Spam dataset)
data = pd.read_csv("spam.txt", sep=",", names=["label", "message"], encoding="latin-1", skiprows=1, usecols=[0, 1])

# Remove missing rows
data = data.dropna()

# Convert everything in message column to string
data["message"] = data["message"].astype(str)

# Keep only ham and spam labels
data = data[data["label"].isin(["ham", "spam"])]

# Convert labels to numbers
data["label"] = data["label"].map({"ham": 0, "spam": 1})

# Remove any rows with NaN labels (from mapping)
data = data.dropna()

# Features and labels
X = data["message"]
y = data["label"]

# Convert text to numerical vectors
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(X)

# Train model
model = MultinomialNB()
model.fit(X, y)

# Save trained model
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("Model trained successfully!")