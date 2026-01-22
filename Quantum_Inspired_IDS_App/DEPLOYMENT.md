# 🚀 QUANTUMIDS Deployment Guide

## Quick Deployment to Streamlit Cloud (Recommended)

### Step 1: Prepare Your Repository

1. **Initialize Git** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "QUANTUMIDS v2.0 - Ready for deployment"
   ```

2. **Push to GitHub**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy on Streamlit Cloud

1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Sign in with your **GitHub account**
3. Click **"New app"**
4. Fill in the details:
   - **Repository**: Select your repository
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL**: Choose your custom URL (optional)
5. Click **"Deploy"**

### Step 3: Wait for Deployment

- Streamlit Cloud will automatically:
  - Install all dependencies from `requirements.txt`
  - Build your app
  - Deploy it to a public URL

### Step 4: Access Your App

Your app will be live at: `https://YOUR-APP-NAME.streamlit.app`

---

## Alternative Deployment Options

### Option 2: Heroku

1. **Install Heroku CLI**: [heroku.com/cli](https://devcenter.heroku.com/articles/heroku-cli)

2. **Login and Create App**:
   ```bash
   heroku login
   heroku create your-app-name
   ```

3. **Deploy**:
   ```bash
   git push heroku main
   ```

4. **Open App**:
   ```bash
   heroku open
   ```

### Option 3: Docker

1. **Build Docker Image**:
   ```bash
   docker build -t quantumids .
   ```

2. **Run Container**:
   ```bash
   docker run -p 8501:8501 quantumids
   ```

3. **Access**: `http://localhost:8501`

### Option 4: AWS/Azure/GCP

Use the provided `Dockerfile` with your cloud provider's container service.

---

## Pre-Deployment Checklist

✅ **All files committed to Git**
- `app.py`
- `model/` directory
- `requirements.txt`
- `.streamlit/config.toml`
- `README.md`

✅ **Dependencies verified**
- All packages in `requirements.txt` are correct
- No missing imports

✅ **Tested locally**
- App runs without errors: `streamlit run app.py`
- File upload works
- Analysis completes successfully

✅ **Configuration files present**
- `.streamlit/config.toml` exists
- `Procfile` exists (for Heroku)
- `Dockerfile` exists (for Docker)

---

## Troubleshooting Deployment

### Issue: App won't start
- **Check**: All dependencies in `requirements.txt`
- **Check**: `app.py` is in root directory
- **Check**: No syntax errors in code

### Issue: Import errors
- **Solution**: Verify all imports are in `requirements.txt`
- **Solution**: Check Python version (needs 3.8+)

### Issue: File upload not working
- **Check**: File size limits (Streamlit Cloud: 200MB)
- **Check**: File format is supported (CSV, XLSX, JSON)

### Issue: Memory errors
- **Solution**: Reduce sample size in `app.py` (line 496: change `100` to smaller number)

---

## Post-Deployment

1. **Test all features**:
   - Landing page loads
   - Dashboard accessible
   - File upload works
   - Analysis completes

2. **Monitor**:
   - Check Streamlit Cloud dashboard for errors
   - Monitor app usage

3. **Update**:
   - Push changes to GitHub
   - Streamlit Cloud auto-updates

---

## Support

For issues, check:
- Streamlit Cloud logs
- GitHub Issues
- Streamlit documentation: [docs.streamlit.io](https://docs.streamlit.io)

---

**Ready to deploy! 🚀**

