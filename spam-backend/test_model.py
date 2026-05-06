#!/usr/bin/env python
"""Test the trained model with sample messages"""

import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Load model and vectorizer
model = pickle.load(open('model.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))

# Test messages
test_messages = [
    "Win free money now! Call 1234567",
    "Hi, how are you doing?",
    "URGENT: Claim your prize! Click here for FREE",
    "Hey mate, see you tomorrow",
    "Limited time offer - free iPhone! Click now"
]

print("Testing the trained model:\n")
print("-" * 60)

for msg in test_messages:
    vec = vectorizer.transform([msg])
    result = model.predict(vec)[0]
    prediction = "Spam" if result == 1 else "Not Spam"
    print(f"Message: {msg}")
    print(f"Prediction: {prediction}")
    print("-" * 60)

print("\nModel test completed successfully!")
