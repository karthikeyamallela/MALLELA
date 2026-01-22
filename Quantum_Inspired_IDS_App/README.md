# 🔐 QUANTUMIDS - Next-Gen Threat Detection

A Quantum-Inspired Intrusion Detection System (IDS) powered by quantum algorithms for advanced cyber threat detection.

## 🌟 Features

- **Quantum-Inspired Processing**: Uses Qiskit for quantum-inspired feature encoding
- **Real-Time Detection**: Analyze network traffic patterns with high accuracy
- **Flexible Data Input**: Supports CSV, Excel, and JSON file formats
- **Modern Dark UI**: Sleek, dark-themed interface optimized for security operations
- **NSL-KDD Compatible**: Optimized for NSL-KDD dataset format

## 🚀 Quick Start

### Local Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Quantum_Inspired_IDS_App
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Access the app**
   - Open your browser to `http://localhost:8501`
   - Click "Initialize System"
   - Click "Access Dashboard"
   - Upload your dataset and start analysis

## 📦 Deployment to Web

### Option 1: Streamlit Cloud (Recommended - Free)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository
   - Set Main file path: `app.py`
   - Click "Deploy"

3. **Your app will be live at**: `https://your-app-name.streamlit.app`

### Option 2: Heroku

1. **Create Procfile**
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Deploy**
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Option 3: Docker

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 8501
   CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. **Build and run**
   ```bash
   docker build -t quantumids .
   docker run -p 8501:8501 quantumids
   ```

## 📋 Requirements

- Python 3.8+
- pandas
- numpy
- scikit-learn
- qiskit
- streamlit
- openpyxl (for Excel support)

## 🎯 Usage

1. **Upload Dataset**: Upload your NSL-KDD or compatible dataset (CSV, Excel, or JSON)
2. **Configure**: Select the label column (auto-detected if contains 'normal'/'attack')
3. **Analyze**: Click "Start Quantum Analysis" to process the data
4. **Results**: View detection accuracy and performance metrics

## 🔧 Project Structure

```
Quantum_Inspired_IDS_App/
├── app.py                 # Main Streamlit application
├── model/
│   ├── preprocessing.py   # Data preprocessing functions
│   ├── quantum_encoding.py # Quantum-inspired encoding
│   └── classifier.py      # ML classifier
├── data/                  # Dataset files
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🛠️ Troubleshooting

### CSV Reading Errors
- Ensure file is UTF-8 encoded
- Check that file has proper comma separators
- Verify file is not empty or corrupted

### Import Errors
- Run `pip install -r requirements.txt` to install all dependencies
- Ensure Python version is 3.8 or higher

### Deployment Issues
- Check that all files are committed to Git
- Verify `requirements.txt` includes all dependencies
- Ensure `app.py` is in the root directory

## 📝 License

This project is open source and available for educational and research purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or issues, please open an issue on GitHub.

---

**SECURE CONNECTION ESTABLISHED // ENCRYPTED VIA TLS 1.3**

