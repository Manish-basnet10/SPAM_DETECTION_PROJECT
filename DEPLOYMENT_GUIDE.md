# Spam Email Detection System - Complete Deployment Guide

## 🎯 System Overview

This is a full-stack Spam Email Detection System with:
- **Backend**: Python Flask + PostgreSQL + SQLAlchemy
- **Frontend**: React (optional, backend works standalone)
- **ML Model**: Trained Multinomial Naive Bayes with TF-IDF vectorization
- **Database**: PostgreSQL with predictions table

---

## ✅ Prerequisites Checklist

- ✓ Python 3.13+ installed
- ✓ PostgreSQL running on localhost:5432
- ✓ Database created: `spam_detection_db`
- ✓ Table created: `predictions`
- ✓ Model files: `model.pkl`, `vectorizer.pkl`
- ✓ All Python packages installed

---

## 📦 Quick Start (5 minutes)

### 1. Navigate to Backend Directory
```bash
cd spam-backend
```

### 2. Install Dependencies (if not already done)
```bash
pip install -r requirements.txt
```

**Installed Packages:**
- Flask 3.0.2
- Flask-SQLAlchemy 3.1.1
- psycopg2-binary (PostgreSQL adapter)
- scikit-learn (ML models)
- pandas (data handling)

### 3. Run the Application
```bash
python app.py
```

**Expected Output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Debugger PIN: XXX-XXX-XXX
```

### 4. Access the Application
Open browser: **http://127.0.0.1:5000**

---

## 🗄️ Database Configuration

### Connection Details
```
URL: postgresql://postgres:Aastha21%40@localhost:5432/spam_detection_db
Username: postgres
Password: Aastha21@
Host: localhost
Port: 5432
Database: spam_detection_db
```

**Important:** The `@` in password is URL-encoded as `%40`

### Table Schema
```sql
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    message TEXT NOT NULL,
    result VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);
```

**Columns:**
- `id`: Auto-incrementing primary key
- `message`: Email text submitted by user
- `result`: Prediction result ("Spam" or "Not Spam")
- `created_at`: Timestamp when prediction was made (UTC)

---

## 🚀 Application Routes

| Route | Method | Purpose | Input | Output |
|-------|--------|---------|-------|--------|
| `/` | GET | Home page | - | HTML form |
| `/predict` | POST | Process email | `message` (form data) | HTML result page |
| `/history` | GET | View all predictions | - | HTML history table |

### Route Details

#### GET `/` (Home)
- Renders `templates/index.html`
- Displays email input form
- Links to history page

#### POST `/predict`
- Accepts form data with `message` parameter
- Validates input (non-empty)
- Checks if model is loaded
- Transforms text using vectorizer
- Predicts spam/ham using model
- Saves prediction to PostgreSQL
- Redirects to result page

#### GET `/history`
- Queries all predictions from database
- Ordered by most recent first
- Displays in HTML table with:
  - Prediction ID
  - Email text
  - Result (Spam/Not Spam)
  - Timestamp

---

## 🧠 Machine Learning Pipeline

### Model Loading
```python
# Loads both model and vectorizer from pickle files
model_bundle = {
    "model": MultinomialNB(),        # Trained classifier
    "vectorizer": TfidfVectorizer()  # Text transformer
}
```

### Prediction Flow
1. **Input**: Raw email text
2. **Vectorization**: TF-IDF transformation
3. **Classification**: Multinomial Naive Bayes prediction
4. **Output**: "Spam" or "Not Spam"

### Model Files
- `model.pkl` (size: ~10KB) - Trained classifier
- `vectorizer.pkl` (size: ~20KB) - Text vectorizer

### Training Data
- Training dataset: `data/spam.csv`
- Labels: "ham" or "spam"
- Feature: Email text messages

---

## 📁 Project Structure

```
spam-backend/
├── app.py                          # Main Flask application
├── model.pkl                       # Trained ML model
├── vectorizer.pkl                  # TF-IDF vectorizer
├── requirements.txt                # Python dependencies
├── model.py                        # Model training script
│
├── templates/                      # HTML templates
│   ├── index.html                  # Home page with form
│   ├── result.html                 # Prediction result display
│   └── history.html                # Prediction history table
│
├── static/                         # CSS and assets
│   └── style.css                   # Unified stylesheet
│
├── data/                           # Training data
│   └── spam.csv                    # Training dataset
│
└── __pycache__/                    # Python cache
```

---

## 🧪 Testing the Application

### Test 1: Home Page
```bash
curl http://127.0.0.1:5000/
# Should return HTML form
```

### Test 2: Make a Prediction (Spam)
```bash
curl -X POST http://127.0.0.1:5000/predict \
  -d "message=WIN a free iPhone now! Click this link immediately!!!"
# Should return result page with "Spam"
```

### Test 3: Make a Prediction (Not Spam)
```bash
curl -X POST http://127.0.0.1:5000/predict \
  -d 'message=Hi, could you review the document I sent? Thanks!'
# Should return result page with "Not Spam"
```

### Test 4: View History
```bash
curl http://127.0.0.1:5000/history
# Should return HTML table with all predictions
```

### Test 5: Invalid Input
```bash
curl -X POST http://127.0.0.1:5000/predict \
  -d "message="
# Should show error: "Please enter email text before submitting"
```

---

## 🎨 Frontend Templates

### index.html (Home)
```html
- Form with textarea for email input
- Submit button
- Link to history page
- Clean, modern styling
```

### result.html (Prediction Result)
```html
- Large, color-coded result (Red for Spam, Green for Not Spam)
- Original email text preview
- Button to try another prediction
- Button to view history
```

### history.html (All Predictions)
```html
- Responsive table with columns:
  - ID
  - Email Text (truncated with preview)
  - Result (color-coded)
  - Timestamp
- Back to home button
- Message if no predictions yet
```

---

## 🎯 User Workflow

```
1. User visits http://127.0.0.1:5000/
   ↓
2. Sees email input form (index.html)
   ↓
3. Enters email text and clicks "Predict"
   ↓
4. Form submits to /predict (POST)
   ↓
5. Flask:
   - Validates input
   - Loads model & vectorizer
   - Transforms text
   - Predicts result
   - Saves to PostgreSQL
   ↓
6. Shows result page (result.html)
   - Red "SPAM" or Green "NOT SPAM"
   - Original email shown
   - Options: Try Another / View History
   ↓
7. User can view /history
   - See all past predictions
   - Most recent first
   - Timestamps in UTC
```

---

## 🔧 Configuration & Customization

### Change Database Connection
Edit `app.py` line 12-16:
```python
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password%40@host:port/database"
)
```

### Use Environment Variables
```bash
# Linux/Mac
export DATABASE_URL="postgresql://user:pass@localhost/db"
python app.py

# Windows PowerShell
$env:DATABASE_URL = "postgresql://user:pass@localhost/db"
python app.py
```

### Enable/Disable Debug Mode
In `app.py` line 103:
```python
app.run(debug=True)   # Enable debug
app.run(debug=False)  # Disable debug (production)
```

---

## 🐛 Troubleshooting

### Issue: "Connection refused"
**Cause**: PostgreSQL not running
**Solution**: 
```bash
# Windows
Start-Service PostgreSQL
# or use pgAdmin/Services to start PostgreSQL
```

### Issue: "password authentication failed"
**Cause**: Wrong password or @ not URL-encoded
**Solution**: 
- Check password is `Aastha21@` 
- Ensure @ is encoded as `%40` in connection string
- Verify PostgreSQL user exists

### Issue: "model.pkl not found"
**Cause**: Model files not in spam-backend directory
**Solution**:
```bash
# Train the model
python model.py
# Or copy model.pkl and vectorizer.pkl to spam-backend/
```

### Issue: "No module named 'flask'"
**Cause**: Dependencies not installed
**Solution**:
```bash
pip install -r requirements.txt
```

### Issue: Port 5000 already in use
**Cause**: Another app using port 5000
**Solution**: 
```bash
# Change port in app.py line 103:
app.run(debug=True, port=5001)
```

### Issue: Templates not found
**Cause**: Running app from wrong directory
**Solution**:
```bash
cd spam-backend
python app.py
```

---

## 📊 Example Predictions

### Spam Examples
- "WIN a free iPhone now! Click this link immediately!!!"
- "Congratulations! You won 5000 dollars. Claim now."
- "Get cheap meds without prescription. Order now."
- "Limited time offer! Lowest loan rates guaranteed."

### Not Spam Examples
- "Hi, are we still meeting at 6 pm?"
- "Can you call me when you are free?"
- "Please send me the report by tonight."
- "Happy birthday! Have a great day."

---

## 📈 Database Monitoring

### Check table exists:
```bash
psql -U postgres -d spam_detection_db
\dt
```

### View all predictions:
```sql
SELECT * FROM predictions ORDER BY created_at DESC;
```

### Count predictions by type:
```sql
SELECT result, COUNT(*) FROM predictions GROUP BY result;
```

### Delete old predictions:
```sql
DELETE FROM predictions WHERE created_at < NOW() - INTERVAL '30 days';
```

---

## 🚀 Production Deployment

### Use Gunicorn (instead of Flask dev server):
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Use Nginx as reverse proxy
### Set `debug=False` in app.py
### Use environment variables for secrets
### Enable HTTPS/SSL
### Set up database backups

---

## 📝 Files Summary

| File | Purpose | Status |
|------|---------|--------|
| app.py | Main Flask application | ✓ Ready |
| model.pkl | ML model | ✓ Ready |
| vectorizer.pkl | Text vectorizer | ✓ Ready |
| requirements.txt | Python dependencies | ✓ Ready |
| templates/index.html | Home page | ✓ Ready |
| templates/result.html | Result page | ✓ Ready |
| templates/history.html | History page | ✓ Ready |
| static/style.css | Styling | ✓ Ready |

---

## ✨ Key Features

✓ **Web Interface**: Clean, responsive design  
✓ **Real-time Predictions**: Instant spam detection  
✓ **Database Storage**: All predictions saved to PostgreSQL  
✓ **History View**: Access all past predictions  
✓ **Error Handling**: Graceful error messages  
✓ **Mobile Friendly**: Works on phones/tablets  
✓ **Easy Deployment**: Simple setup and run  

---

## 📞 Support

For issues:
1. Check the Troubleshooting section above
2. Verify database is running and accessible
3. Check model.pkl and vectorizer.pkl exist
4. Ensure all packages installed: `pip install -r requirements.txt`
5. Check Flask is running on http://127.0.0.1:5000

---

**System Status**: ✅ **READY TO USE**

Start with: `python app.py` → Open: `http://127.0.0.1:5000`
