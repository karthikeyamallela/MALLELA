import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO

from model.preprocessing import preprocess_data
from model.quantum_encoding import angle_encoding
from model.classifier import train_and_test_classifier

from sklearn.model_selection import train_test_split

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="QUANTUMIDS - Next-Gen Threat Detection",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------------------------------
# Custom CSS for QUANTUMIDS theme
# -------------------------------------------------
st.markdown("""
<style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Dark theme background - Much darker */
    .stApp {
        background: #000000 !important;
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(0, 255, 255, 0.02) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(138, 43, 226, 0.02) 0%, transparent 50%);
        background-size: 100% 100%, 100% 100%;
    }
    
    /* Make all Streamlit elements dark */
    .stApp > div {
        background: #000000 !important;
    }
    
    section[data-testid="stSidebar"],
    div[data-testid="stToolbar"] {
        background: #000000 !important;
    }
    
    @keyframes circuitPulse {
        0%, 100% { background-position: 0% 0%, 0% 0%, 0% 0%; }
        50% { background-position: 0% 0%, 0% 0%, 100% 0%; }
    }
    
    /* Main container - Darker */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background: #000000 !important;
        max-width: 1200px;
    }
    
    /* Make all text areas dark */
    .element-container {
        background: rgba(10, 10, 15, 0.8) !important;
    }
    
    /* Dataframe styling */
    .dataframe {
        background: #0a0a0a !important;
        color: #ffffff !important;
    }
    
    /* Info boxes darker */
    .stInfo {
        background: rgba(10, 10, 20, 0.9) !important;
        border: 1px solid rgba(0, 255, 255, 0.3) !important;
    }
    
    /* Error boxes darker */
    .stError {
        background: rgba(40, 10, 10, 0.9) !important;
        border: 1px solid rgba(255, 0, 0, 0.3) !important;
    }
    
    /* Success boxes darker */
    .stSuccess {
        background: rgba(10, 40, 10, 0.9) !important;
        border: 1px solid rgba(0, 255, 0, 0.3) !important;
    }
    
    /* QUANTUMIDS Logo */
    .quantumids-logo {
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 1rem;
        letter-spacing: 2px;
    }
    
    .quantumids-logo .highlight {
        color: #00ffff;
        text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff;
    }
    
    /* System Status */
    .system-status {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        border: 2px solid #00ffff;
        border-radius: 4px;
        background: rgba(0, 255, 255, 0.1);
        margin: 1rem 0;
    }
    
    .status-dot {
        display: inline-block;
        width: 10px;
        height: 10px;
        background: #00ffff;
        border-radius: 50%;
        margin-right: 8px;
        box-shadow: 0 0 10px #00ffff;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .status-text {
        color: #00ffff;
        font-weight: 600;
        font-size: 0.9rem;
        letter-spacing: 1px;
    }
    
    /* Main Heading */
    .main-heading {
        font-size: 4rem;
        font-weight: 800;
        text-align: center;
        margin: 2rem 0;
        line-height: 1.2;
    }
    
    .main-heading .gradient-text {
        background: linear-gradient(90deg, #00ffff 0%, #8a2be2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Sub-heading */
    .sub-heading {
        text-align: center;
        color: #888888;
        font-size: 1.1rem;
        margin-bottom: 3rem;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #00ffff 0%, #00cccc 100%);
        color: #000000;
        font-weight: 700;
        font-size: 1.1rem;
        padding: 0.75rem 2rem;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.4);
        width: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #00cccc 0%, #00ffff 100%);
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.6);
        transform: translateY(-2px);
    }
    
    .init-button {
        background: transparent !important;
        border: 2px solid #00ffff !important;
        color: #00ffff !important;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.3) !important;
    }
    
    .init-button:hover {
        background: rgba(0, 255, 255, 0.1) !important;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.5) !important;
    }
    
    /* Footer */
    .footer-text {
        text-align: center;
        color: #666;
        font-size: 0.85rem;
        margin-top: 4rem;
        padding: 1rem;
        border-top: 1px solid rgba(0, 255, 255, 0.2);
    }
    
    /* Dashboard Styles */
    .dashboard-container {
        background: rgba(20, 20, 30, 0.6);
        border: 1px solid rgba(0, 255, 255, 0.3);
        border-radius: 8px;
        padding: 2rem;
        margin: 1rem 0;
    }
    
    .metric-card {
        background: rgba(0, 255, 255, 0.1);
        border: 1px solid #00ffff;
        border-radius: 8px;
        padding: 1.5rem;
        text-align: center;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #00ffff;
        text-shadow: 0 0 10px #00ffff;
    }
    
    .metric-label {
        color: #b0b0b0;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* File uploader styling */
    .stFileUploader > div > div {
        background: rgba(20, 20, 30, 0.8);
        border: 2px dashed #00ffff;
        border-radius: 8px;
        padding: 2rem;
    }
    
    /* Text colors - Darker */
    h1, h2, h3 {
        color: #ffffff !important;
    }
    
    p, label {
        color: #888888 !important;
    }
    
    /* Selectbox styling - Darker */
    .stSelectbox > div > div {
        background: rgba(10, 10, 15, 0.9) !important;
        border: 1px solid rgba(0, 255, 255, 0.3) !important;
        color: #ffffff !important;
    }
    
    /* Input fields darker */
    .stTextInput > div > div > input {
        background: rgba(10, 10, 15, 0.9) !important;
        color: #ffffff !important;
        border: 1px solid rgba(0, 255, 255, 0.3) !important;
    }
    
    /* File uploader darker */
    .uploadedFile {
        background: rgba(10, 10, 15, 0.9) !important;
        color: #ffffff !important;
    }
    
    /* Tables darker */
    table {
        background: #0a0a0a !important;
        color: #ffffff !important;
    }
    
    /* Metrics darker */
    [data-testid="stMetricValue"] {
        color: #00ffff !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #888888 !important;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Initialize session state
# -------------------------------------------------
if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'system_initialized' not in st.session_state:
    st.session_state.system_initialized = False

# -------------------------------------------------
# Landing Page
# -------------------------------------------------
if st.session_state.page == 'landing':
    # Header with logo and initialize button
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown('<div class="quantumids-logo">QUANTUM<span class="highlight">IDS</span></div>', unsafe_allow_html=True)
    
    with col2:
        if st.button("Initialize System", key="init_btn"):
            st.session_state.system_initialized = True
    
    # System Status
    if st.session_state.system_initialized:
        st.markdown("""
        <div class="system-status">
            <span class="status-dot"></span>
            <span class="status-text">SYSTEM V2.0 ONLINE</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Main Heading
    st.markdown("""
    <div class="main-heading">
        NEXT-GEN <span class="gradient-text">THREAT</span> DETECTED
    </div>
    """, unsafe_allow_html=True)
    
    # Sub-heading
    st.markdown("""
    <div class="sub-heading">
        Advanced heuristic analysis powered by quantum algorithms. 
        Secure your infrastructure with real-time anomaly detection.
    </div>
    """, unsafe_allow_html=True)
    
    # Access Dashboard Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Access Dashboard →", key="dashboard_btn"):
            st.session_state.page = 'dashboard'
            st.rerun()
    
    # Footer
    st.markdown("""
    <div class="footer-text">
        SECURE CONNECTION ESTABLISHED // ENCRYPTED VIA TLS 1.3
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# Dashboard Page
# -------------------------------------------------
elif st.session_state.page == 'dashboard':
    # Header
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown('<div class="quantumids-logo">QUANTUM<span class="highlight">IDS</span> DASHBOARD</div>', unsafe_allow_html=True)
    
    with col2:
        if st.button("← Back to Home", key="back_btn"):
            st.session_state.page = 'landing'
            st.rerun()
    
    # System Status
    st.markdown("""
    <div class="system-status">
        <span class="status-dot"></span>
        <span class="status-text">SYSTEM V2.0 ONLINE</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Upload Section
    st.markdown("### 📤 Threat Data Upload")
    uploaded_file = st.file_uploader(
        "Upload Dataset for Analysis", 
        type=["csv", "xlsx", "xls", "json"],
        help="Supports CSV, Excel, and JSON files. For NSL-KDD: CSV with 41 features + label column"
    )
    
    if uploaded_file:
        # Detect file type and read accordingly
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        try:
            if file_extension == 'csv':
                # Read file content into memory first to avoid file pointer issues
                file_bytes = uploaded_file.read()
                
                # Try different encodings
                encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
                df = None
                last_error = None
                
                for encoding in encodings:
                    try:
                        # Convert bytes to string
                        file_content = file_bytes.decode(encoding)
                        
                        # Try reading without header first (NSL-KDD format)
                        # Handle pandas version compatibility
                        try:
                            # pandas >= 1.3.0
                            df = pd.read_csv(
                                StringIO(file_content),
                                header=None,
                                sep=',',
                                engine='python',
                                on_bad_lines='skip'
                            )
                        except TypeError:
                            # pandas < 1.3.0
                            df = pd.read_csv(
                                StringIO(file_content),
                                header=None,
                                sep=',',
                                engine='python',
                                error_bad_lines=False,
                                warn_bad_lines=False
                            )
                        
                        if not df.empty:
                            break
                    except (UnicodeDecodeError, pd.errors.ParserError) as e:
                        last_error = e
                        continue
                
                if df is None or df.empty:
                    raise ValueError(f"Could not parse CSV file. Last error: {str(last_error)}")
                    
            elif file_extension in ['xlsx', 'xls']:
                df = pd.read_excel(uploaded_file, header=None, engine='openpyxl')
            elif file_extension == 'json':
                df = pd.read_json(uploaded_file)
            else:
                st.error(f"Unsupported file type: {file_extension}")
                st.stop()
                
            # Final validation
            if df.empty:
                raise ValueError("File appears to be empty or could not be parsed")
                
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
            st.info("💡 **Troubleshooting Tips:**\n- Ensure the file is not corrupted\n- Check that the file has proper comma separators\n- For NSL-KDD format, the file should have 41 features + 1 label column\n- Try re-saving the CSV file with UTF-8 encoding\n- Ensure the file is not empty")
            st.stop()
        
        st.markdown("---")
        
        # Dataset Preview
        st.markdown("### 📄 Dataset Preview")
        st.dataframe(df.head(), use_container_width=True)
        st.info(f"**Dataset Shape:** {df.shape[0]} rows × {df.shape[1]} columns")
        
        # Column Selection
        st.markdown("### ⚙️ Configuration")
        
        # Create column options (handle both named and unnamed columns)
        if isinstance(df.columns, pd.RangeIndex):
            # Unnamed columns (numeric indices)
            label_column_options = list(range(df.shape[1]))
            default_idx = df.shape[1] - 1  # Default to last column (NSL-KDD format)
        else:
            # Named columns
            label_column_options = list(df.columns)
            default_idx = len(label_column_options) - 1  # Default to last column
        
        # Try to auto-detect label column (column with 'normal'/'attack')
        for i, col in enumerate(df.columns):
            if df[col].dtype == 'object':
                unique_vals = df[col].astype(str).str.lower().unique()
                if 'normal' in unique_vals or 'attack' in unique_vals:
                    default_idx = i
                    break
        
        label_col = st.selectbox(
            "Select Label Column (target variable)",
            options=label_column_options,
            index=default_idx,
            help="Column containing 'normal' or 'attack' labels"
        )
        
        # Process Button
        if st.button("🚀 Start Quantum Analysis", type="primary"):
            with st.spinner("🔄 Processing data with quantum algorithms..."):
                # Preprocessing
                try:
                    X, y = preprocess_data(df, label_column=label_col)
                    st.success("✅ Preprocessing completed")
                except Exception as e:
                    st.error(f"❌ Preprocessing error: {str(e)}")
                    st.info("💡 **Tip:** Ensure your dataset has:\n- Features (numeric or categorical)\n- Label column with 'normal' and 'attack' values")
                    st.stop()
                
                # Ensure BOTH classes exist
                class_0_idx = np.where(y == 0)[0]
                class_1_idx = np.where(y == 1)[0]
                
                if len(class_0_idx) == 0 or len(class_1_idx) == 0:
                    st.error("❌ Dataset contains only one class. Cannot train classifier.")
                    st.stop()
                
                # Take equal samples from both classes
                n_samples = min(len(class_0_idx), len(class_1_idx), 100)
                
                selected_idx = np.concatenate([
                    class_0_idx[:n_samples],
                    class_1_idx[:n_samples]
                ])
                
                np.random.shuffle(selected_idx)
                
                X_small = X[selected_idx]
                y_small = y[selected_idx]
                
                # Quantum-Inspired Encoding
                st.info("⚛️ Applying quantum-inspired encoding...")
                encoded_features = []
                for row in X_small:
                    quantum_vec = angle_encoding(row[:5])  # first 5 features
                    encoded_features.append(quantum_vec)
                
                encoded_features = np.array(encoded_features)
                
                # Classification
                st.info("🤖 Training quantum-enhanced classifier...")
                accuracy = train_and_test_classifier(encoded_features, y_small)
                
                # Results
                st.markdown("---")
                st.markdown("### 📊 Detection Performance")
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{accuracy * 100:.2f}%</div>
                        <div class="metric-label">Detection Accuracy</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Additional metrics
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Normal Samples", len(class_0_idx))
                with col2:
                    st.metric("Attack Samples", len(class_1_idx))
                
                st.success("🎉 Threat detection analysis completed successfully!")
    
    else:
        st.info("⬆️ Upload a dataset file (CSV, Excel, or JSON) to start quantum threat detection analysis")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div class="footer-text">
        SECURE CONNECTION ESTABLISHED // ENCRYPTED VIA TLS 1.3
    </div>
    """, unsafe_allow_html=True)
