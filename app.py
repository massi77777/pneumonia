import streamlit as st
from utils.prediction import predict_pneumonia

st.set_page_config(
    page_title="Chest X-Ray Screening",
    page_icon="🫁",
    layout="centered",
)

# ---------------------------------------------------------------------------
# Design tokens + full page styling (self-contained, no config.toml needed)
# Palette: dark radiology-room graphite with a cyan light-box accent.
# Type: Space Grotesk (display), Inter (body), IBM Plex Mono (data/numbers).
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@500;600&display=swap');

    :root {
        --bg: #0B1417;
        --panel: #131E22;
        --panel-2: #1B2A2F;
        --border: #24373D;
        --accent: #3FE0C5;
        --accent-dim: #2A9D8F;
        --amber: #E8A33D;
        --coral: #F1685F;
        --mint: #4FD189;
        --text: #E7F1F0;
        --muted: #86A0A0;
    }

    /* Full app background override (so we don't need a config.toml file) */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"], .stApp {
        background-color: var(--bg);
    }
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: var(--text);
    }
    .block-container {
        max-width: 720px;
        padding-top: 2.2rem;
        padding-bottom: 3rem;
    }

    /* Header ------------------------------------------------------------ */
    .eyebrow {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.18em;
        color: var(--accent);
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    .page-title {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 2.15rem;
        line-height: 1.15;
        margin-bottom: 0.4rem;
    }
    .page-subtitle {
        color: var(--muted);
        font-size: 0.96rem;
        margin-bottom: 1.4rem;
    }

    /* Model readout strip -------------------------------------------------- */
    .readout {
        display: flex;
        gap: 1.6rem;
        border-top: 1px solid var(--border);
        border-bottom: 1px solid var(--border);
        padding: 0.7rem 0;
        margin-bottom: 1.6rem;
        flex-wrap: wrap;
    }
    .readout-item .readout-label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.65rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: var(--muted);
    }
    .readout-item .readout-value {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.92rem;
        font-weight: 600;
        color: var(--accent);
        margin-top: 0.15rem;
    }

    /* Disclaimer strip ---------------------------------------------------- */
    .disclaimer {
        border-left: 3px solid var(--amber);
        background: var(--panel);
        padding: 0.85rem 1rem;
        border-radius: 4px;
        font-size: 0.86rem;
        color: var(--muted);
        margin-bottom: 1.8rem;
    }
    .disclaimer b { color: var(--amber); }

    /* Section labels ------------------------------------------------------ */
    .section-label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--muted);
        margin: 1.8rem 0 0.7rem 0;
    }

    /* File uploader dropzone ------------------------------------------------ */
    [data-testid="stFileUploaderDropzone"] {
        background: var(--panel) !important;
        border: 1px dashed var(--border) !important;
        border-radius: 6px !important;
    }
    [data-testid="stFileUploaderDropzone"]:hover {
        border-color: var(--accent) !important;
    }

    /* Uploaded image: viewfinder frame with a scanning light signature ---- */
    [data-testid="stImage"] {
        position: relative;
        overflow: hidden;
        background: var(--panel-2);
        border: 1px solid var(--border);
        border-radius: 6px;
        padding: 10px;
    }
    [data-testid="stImage"]::after {
        content: "";
        position: absolute;
        left: 0;
        right: 0;
        height: 2px;
        top: 0;
        background: linear-gradient(90deg, transparent, var(--accent), transparent);
        box-shadow: 0 0 14px var(--accent);
        animation: scan 3.2s ease-in-out infinite;
    }
    @keyframes scan {
        0%   { top: 0%; }
        50%  { top: 100%; }
        100% { top: 0%; }
    }

    /* Run analysis button --------------------------------------------------- */
    .stButton > button {
        font-family: 'IBM Plex Mono', monospace;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        font-size: 0.8rem;
        background: var(--accent);
        color: #0B1417;
        border: none;
        border-radius: 4px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        margin-top: 0.9rem;
        width: 100%;
    }
    .stButton > button:hover {
        background: var(--accent-dim);
        color: white;
    }

    /* Result card ------------------------------------------------------------ */
    .result-card {
        border-radius: 6px;
        padding: 1.2rem 1.4rem;
        margin-top: 0.6rem;
        background: var(--panel);
        border: 1px solid var(--border);
        border-left: 4px solid var(--flag-color);
    }
    .result-top {
        display: flex;
        align-items: center;
        gap: 0.55rem;
    }
    .status-dot {
        width: 9px;
        height: 9px;
        border-radius: 50%;
        background: var(--flag-color);
        box-shadow: 0 0 8px var(--flag-color);
    }
    .result-label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--muted);
    }
    .result-value {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 1.6rem;
        color: var(--flag-color);
        margin: 0.2rem 0 0 1.35rem;
    }

    /* Confidence gauge --------------------------------------------------------- */
    .gauge-wrap { margin-top: 1.1rem; }
    .gauge-track {
        width: 100%;
        height: 8px;
        border-radius: 4px;
        background: var(--panel-2);
        border: 1px solid var(--border);
        overflow: hidden;
    }
    .gauge-fill { height: 100%; background: var(--flag-color); }
    .gauge-number {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--flag-color);
        margin-top: 0.55rem;
    }
    .gauge-caption {
        font-size: 0.78rem;
        color: var(--muted);
        margin-top: 0.5rem;
        line-height: 1.45;
    }

    /* Footer ------------------------------------------------------------------- */
    .footer-note {
        margin-top: 2.5rem;
        padding-top: 1rem;
        border-top: 1px solid var(--border);
        font-size: 0.76rem;
        color: var(--muted);
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown('<div class="eyebrow">AI-Assisted Screening · Educational Demo</div>', unsafe_allow_html=True)
st.markdown('<div class="page-title">🫁 Chest X-Ray Pneumonia Screening</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="page-subtitle">Upload a chest X-ray image and the model will flag it as Normal or Pneumonia.</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="readout">
        <div class="readout-item">
            <div class="readout-label">Base model</div>
            <div class="readout-value">MobileNetV2</div>
        </div>
        <div class="readout-item">
            <div class="readout-label">Recall · Pneumonia</div>
            <div class="readout-value">97%</div>
        </div>
        <div class="readout-item">
            <div class="readout-label">Test accuracy</div>
            <div class="readout-value">88%</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="disclaimer">
        <b>Not a medical device.</b> This tool is for educational purposes only.
        It is not a diagnosis and must not be used to make real medical decisions.
        Always consult a qualified doctor.
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Upload + inference
# ---------------------------------------------------------------------------
st.markdown('<div class="section-label">01 · Upload image</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "Choose an X-ray image", type=["jpg", "jpeg", "png"], label_visibility="collapsed"
)

if uploaded_file is not None:
    col_l, col_c, col_r = st.columns([1, 3, 1])
    with col_c:
        st.image(uploaded_file, use_container_width=True)

    st.markdown('<div class="section-label">02 · Run screening</div>', unsafe_allow_html=True)
    run_clicked = st.button("Run analysis")

    if run_clicked:
        with st.spinner("Analyzing image..."):
            result, confidence = predict_pneumonia(uploaded_file)

        flag_color = "var(--coral)" if result == "PNEUMONIA" else "var(--mint)"

        st.markdown('<div class="section-label">03 · Result</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="result-card" style="--flag-color:{flag_color};">
                <div class="result-top">
                    <div class="status-dot"></div>
                    <div class="result-label">Predicted class</div>
                </div>
                <div class="result-value">{result}</div>
                <div class="gauge-wrap">
                    <div class="gauge-track">
                        <div class="gauge-fill" style="width:{confidence}%;"></div>
                    </div>
                    <div class="gauge-number">{confidence:.1f}% confidence</div>
                    <div class="gauge-caption">
                        This score is an internal number from the model based on training data,
                        not a real medical probability.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown(
    '<div class="footer-note">Pneumonia Detection Demo · Built with TensorFlow &amp; Streamlit · For learning purposes only</div>',
    unsafe_allow_html=True,
)
