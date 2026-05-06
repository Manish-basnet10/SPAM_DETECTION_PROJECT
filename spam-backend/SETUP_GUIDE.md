# Spam Email Detection System - Setup & Run Guide

## Prerequisites
- PostgreSQL installed and running ✓
- Database created: `spam_detection_db` ✓
- Table created: `predictions(id, message, result, created_at)` ✓
- Model files: `model.pkl` and `vectorizer.pkl` ✓

## Database Configuration
```
URL: postgresql://postgres:Aastha21@localhost:5432/spam_detection_db
Username: postgres
Password: Aastha21@
Port: 5432
```

## Installation Steps

### 1. Install Python Dependencies
```bash
cd spam-backend
pip install -r requirements.txt
```

**Packages installed:**
- Flask==3.0.2 - Web framework
- Flask-SQLAlchemy==3.1.1 - ORM for database operations
- psycopg2-binary==2.9.9 - PostgreSQL adapter
- pandas==2.2.2 - Data manipulation
- scikit-learn==1.4.2 - Machine learning models

### 2. Verify Model Files
Both files must exist in the `spam-backend/` directory:
- ✓ `model.pkl` - Trained ML model
- ✓ `vectorizer.pkl` - Text vectorizer

## Running the Application

### Start the Flask Development Server
```bash
cd spam-backend
python app.py
```

**Expected Output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Access the Application
Open your browser and go to: **http://127.0.0.1:5000**

## Application Routes

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Home page with email input form |
| `/predict` | POST | Process email and predict spam/ham |
| `/history` | GET | View all predictions stored in database |

## Application Workflow

1. **User enters email text** on the home page (`/`)
2. **Form submits** to `/predict` route
3. **Flask processes the email:**
   - Validates input
   - Loads ML model and vectorizer
   - Transforms text using TF-IDF vectorizer
   - Predicts: "Spam" or "Not Spam"
4. **Saves prediction** to PostgreSQL database (predictions table)
5. **Displays result** with the input email text
6. **User can view history** on `/history` page showing all past predictions

## Project Structure
```
spam-backend/
├── app.py                 # Main Flask application
├── model.pkl              # Trained ML model
├── vectorizer.pkl         # TF-IDF vectorizer for text processing
├── requirements.txt       # Python dependencies
├── templates/
│   ├── index.html         # Home page with form
│   ├── result.html        # Prediction result display
│   └── history.html       # Prediction history table
├── static/
│   └── style.css          # Unified CSS styling
└── data/
    └── spam.csv           # Training dataset
```

## Features

✓ **Web Interface**
- Modern, responsive design
- Email text input form
- Clear prediction results (Spam/Not Spam indicator)
- Prediction history with timestamps

✓ **Database Integration**
- PostgreSQL for persistent storage
- SQLAlchemy ORM for safe database operations
- Automatic schema creation on first run

✓ **Machine Learning**
- Pre-trained Multinomial Naive Bayes model
- TF-IDF text vectorization
- Binary classification (Spam/Not Spam)

✓ **Error Handling**
- Input validation
- Model file existence checks
- Database connection error handling
- Clear error messages for users

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution:** Run `pip install -r requirements.txt` again

### Issue: "could not translate host name to address"
**Solution:** Ensure PostgreSQL is running and accessible on localhost:5432

### Issue: "model.pkl not found"
**Solution:** Ensure `model.pkl` and `vectorizer.pkl` are in the `spam-backend/` directory

### Issue: Database connection refused
**Solution:** 
```sql
-- Check if database and table exist:
psql -U postgres -d spam_detection_db -c "\dt"
```

## Database Schema

### `predictions` Table
```sql
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    message TEXT NOT NULL,
    result VARCHAR(20) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

## Example Usage

### Spam Example
```
Input: "WIN a free iPhone now! Click this link immediately!!!"
Output: SPAM
```

### Not Spam Example
```
Input: "Hi, could you review the document I sent? Thanks!"
Output: NOT SPAM
```

## Performance Notes

- Model loading happens on app startup (one-time operation)
- Database queries are optimized with ordering
- Small input sizes ensure fast prediction times (<100ms)
- History page loads all predictions (consider pagination for large datasets)

---

**Ready to go!** Start the app with `python app.py` and navigate to http://127.0.0.1:5000
