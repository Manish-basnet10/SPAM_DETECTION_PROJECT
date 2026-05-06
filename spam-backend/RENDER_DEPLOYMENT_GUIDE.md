# Render Deployment Guide for Spam Detection Flask App

## ✅ What Was Fixed

### 1. Updated requirements.txt
Added the following critical dependencies:
- **gunicorn==21.2.0** - Production WSGI server (was MISSING - main cause of deployment failure)
- **Flask-CORS==4.0.0** - CORS support for API
- **python-dotenv==1.0.0** - Environment variable support
- Updated pandas, scikit-learn, and numpy with pinned versions for compatibility

### 2. App Configuration
- ✓ Flask app instance named `app` exists and is properly configured
- ✓ Database URL correctly reads from `DATABASE_URL` environment variable
- ✓ `app.run()` is safely wrapped in `if __name__ == "__main__"` guard (won't interfere with gunicorn)
- ✓ SQLAlchemy configured with proper track modifications setting

### 3. Created .gitignore
- Excludes `.env`, `__pycache__`, virtual environments, and IDE files
- Protects sensitive credentials from being committed

---

## 🚀 Pre-Deployment Commands (Run Locally FIRST)

### Step 1: Install Dependencies Locally
```powershell
cd spam-backend
pip install -r requirements.txt
```

### Step 2: Train the Model
This generates `model.pkl` and `vectorizer.pkl` files needed for predictions:
```powershell
python model.py
```
Expected output:
```
Sample dataset created at C:\...
Model accuracy: 0.9XXX
Classification report:
...
Model saved to ...
```

### Step 3: Test with Gunicorn Locally
```powershell
gunicorn app:app --bind 0.0.0.0:5000
```
Then visit: http://localhost:5000

If successful, you should see the home page.

### Step 4: Verify Database Connection
Create a `.env` file in `spam-backend/` folder:
```
DATABASE_URL=postgresql://postgres:Aastha21%40@localhost:5432/spam_detection_db
```

Test the app locally with:
```powershell
python app.py
```

---

## 📤 Git Preparation Commands

Before pushing to GitHub:

```powershell
# From root of spam-project folder
git add .
git status  # Review what will be committed

# Make sure you see:
# - requirements.txt (updated)
# - .gitignore (new)
# - model.pkl and vectorizer.pkl files
# - NO .env file (excluded by .gitignore)

git commit -m "Fix Render deployment: add gunicorn, Flask-CORS, python-dotenv and update dependencies"
git push origin main  # or your branch name
```

---

## 🌐 Render Deployment Configuration

### Step 1: Create a New Web Service on Render
1. Go to https://dashboard.render.com/
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Select the branch to deploy

### Step 2: Configure the Build and Start Commands
- **Build Command**: `pip install -r spam-backend/requirements.txt`
- **Start Command**: `cd spam-backend && gunicorn app:app`

### Step 3: Set Environment Variables
In Render dashboard, go to Environment section and add:

```
DATABASE_URL=postgresql://[user]:[password]@[host]:[port]/[database]
```

To get your PostgreSQL connection string:
1. Create a PostgreSQL database on Render (or use existing)
2. Copy the internal connection string
3. Paste it into the `DATABASE_URL` environment variable

Example format:
```
postgresql://postgres:password123@dpg-xxxxx-a.oregon-postgres.render.com:5432/spamdb
```

### Step 4: Deploy
Click "Deploy" and monitor the logs. You should see:
```
Collecting Flask==3.0.2
...
Collecting gunicorn==21.2.0
...
Successfully installed Flask-3.0.2 ...
Successfully installed gunicorn-21.2.0 ...
[TIMESTAMP] [INFO] Starting gunicorn 21.2.0
[TIMESTAMP] [INFO] Listening at: http://0.0.0.0:10000 (xxxx)
```

---

## ✅ Verification Checklist

- [ ] `requirements.txt` includes gunicorn and all dependencies with versions
- [ ] `.gitignore` created in spam-backend folder
- [ ] `app.py` has Flask instance named `app`
- [ ] `model.pkl` and `vectorizer.pkl` generated locally
- [ ] Gunicorn runs successfully locally: `gunicorn app:app`
- [ ] All files committed to Git (except .env and __pycache__)
- [ ] Render environment variable `DATABASE_URL` is set
- [ ] Render Build Command configured correctly
- [ ] Render Start Command configured correctly

---

## 🔧 Troubleshooting

### If deployment still fails with "Exited with status 1":

1. **Check Render logs**: View full build and runtime logs
2. **Verify model files exist**: 
   - Run `python model.py` locally
   - Commit model.pkl and vectorizer.pkl to Git
3. **Check DATABASE_URL**: 
   - Verify it's set in Render Environment variables
   - Test connection locally with .env file first
4. **Review requirements.txt**:
   - Make sure gunicorn is listed
   - Make sure no conflicting versions

### If app starts but prediction fails:

1. Ensure model.pkl and vectorizer.pkl are in the app directory
2. Check that Flask-SQLAlchemy can connect to PostgreSQL
3. Review Render runtime logs for specific error messages

---

## 📝 Updated requirements.txt Content

```
Flask==3.0.2
Flask-SQLAlchemy==3.1.1
Flask-CORS==4.0.0
gunicorn==21.2.0
psycopg2-binary==2.9.9
pandas==2.2.0
scikit-learn==1.4.1
numpy==1.26.4
python-dotenv==1.0.0
```

---

## 🎯 Summary of Changes

| Component | Status | Notes |
|-----------|--------|-------|
| requirements.txt | ✅ Updated | Added gunicorn, Flask-CORS, python-dotenv; pinned all versions |
| app.py | ✅ Production Ready | No changes needed; properly configured |
| .gitignore | ✅ Created | Protects sensitive files |
| Model files | ⚠️ Action Needed | Run `python model.py` to generate |
| Environment Setup | ⚠️ Action Needed | Set DATABASE_URL on Render |

