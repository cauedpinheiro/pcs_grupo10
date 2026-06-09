import streamlit as st
import numpy as np
from PIL import Image

try:
    from ai_edge_litert.interpreter import Interpreter
except ImportError:
    try:
        import tflite_runtime.interpreter as tflite
        Interpreter = tflite.Interpreter
    except ImportError:
        from tensorflow.lite.python.interpreter import Interpreter

# ── Página ──────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Resíduo — Classificador de Resíduos",
    page_icon="♻️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ── CSS personalizado ────────────────────────────────────────────────────────
def inject_css(dark: bool):
    if dark:
        bg        = "#181c14"
        surface   = "#222c1a"
        green     = "#7bbf54"
        green_lt  = "#1e2d18"
        green_mid = "#4a7a2c"
        brown     = "#c4956a"
        brown_lt  = "#2a1f14"
        text      = "#d8ecc4"
        muted     = "#8aaa70"
        border    = "rgba(123,191,84,0.18)"
    else:
        bg        = "#faf7f2"
        surface   = "#ffffff"
        green     = "#5a8a3c"
        green_lt  = "#e8f3e0"
        green_mid = "#a3c97a"
        brown     = "#7a5c3a"
        brown_lt  = "#f2ebe0"
        text      = "#2c3e1f"
        muted     = "#6b7c5a"
        border    = "rgba(90,138,60,0.18)"

    st.markdown(f"""
    <style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {{
        background-color: {bg} !important;
    }}
    [data-testid="stAppViewContainer"] > .main {{
        background-color: {bg} !important;
    }}
    section[data-testid="stMain"] > div {{
        padding-top: 1.5rem;
    }}
    #MainMenu, header, footer {{ visibility: hidden; }}
    .eco-topbar {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: {surface};
        border: 0.5px solid {border};
        border-radius: 14px;
        padding: 12px 18px;
        margin-bottom: 22px;
    }}
    .eco-logo {{ display: flex; align-items: center; gap: 10px; }}
    .eco-logo-icon {{
        width: 36px; height: 36px;
        background: {green_lt};
        border-radius: 10px;
        border: 0.5px solid {border};
        display: flex; align-items: center; justify-content: center;
        font-size: 20px;
    }}
    .eco-logo-name {{ font-size: 16px; font-weight: 600; color: {text}; }}
    .eco-logo-sub  {{ font-size: 11px; color: {muted}; }}
    .eco-card {{
        background: {surface};
        border: 0.5px solid {border};
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 16px;
    }}
    .eco-section-label {{
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.08em;
        color: {muted};
        text-transform: uppercase;
        margin-bottom: 10px;
    }}
    .eco-result-recycle {{
        background: {green_lt};
        border: 0.5px solid {green_mid};
        border-radius: 12px;
        padding: 16px 18px;
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 14px;
    }}
    .eco-result-organic {{
        background: {brown_lt};
        border: 0.5px solid rgba(122,92,58,0.3);
        border-radius: 12px;
        padding: 16px 18px;
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 14px;
    }}
    .eco-result-icon {{ font-size: 36px; }}
    .eco-result-label {{
        font-size: 20px;
        font-weight: 700;
        color: {green};
    }}
    .eco-result-label-org {{
        font-size: 20px;
        font-weight: 700;
        color: {brown};
    }}
    .eco-result-sub {{ font-size: 13px; color: {muted}; margin-top: 2px; }}
    .eco-tip {{
        background: {green_lt};
        border: 0.5px solid {border};
        border-radius: 10px;
        padding: 12px 14px;
        font-size: 13px;
        color: {text};
        line-height: 1.6;
        margin-top: 10px;
    }}
    div[data-testid="stButton"] > button {{
        background: {green} !important;
        color: #fff !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 10px 0 !important;
        width: 100%;
        font-size: 14px !important;
    }}
    div[data-testid="stButton"] > button:hover {{ opacity: 0.88 !important; }}
    [data-testid="stFileUploader"] {{
        background: {surface};
        border: 1.5px dashed {green_mid};
        border-radius: 14px;
        padding: 8px;
    }}
    [data-testid="stProgress"] > div > div {{
        background-color: {green} !important;
    }}
    [data-testid="stRadio"] label {{ color: {text} !important; font-size: 14px !important; }}
    [data-testid="stExpander"] {{
        background: {surface};
        border: 0.5px solid {border} !important;
        border-radius: 12px !important;
    }}
    [data-testid="stImage"] img {{ border-radius: 12px; border: 0.5px solid {border}; }}
    </style>
    """, unsafe_allow_html=True)


# ── Estado do tema ───────────────────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

inject_css(st.session_state.dark_mode)

# ── Topbar ───────────────────────────────────────────────────────────────────
col_logo, col_theme = st.columns([3, 1])
with col_logo:
    st.markdown("""
    <div class="eco-topbar">
      <div class="eco-logo">
        <div class="eco-logo-icon">♻️</div>
        <div>
          <div class="eco-logo-name">Resíduo</div>
          <div class="eco-logo-sub">classificador inteligente de resíduos</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

with col_theme:
    st.write("")
    label = "🌙 Escuro" if not st.session_state.dark_mode else "☀️ Claro"
    if st.button(label, use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# ── Carrega modelo TFLite ─────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    interpreter = Interpreter(model_path="model/model_unquant.tflite")
    interpreter.allocate_tensors()
    input_details  = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    with open("model/labels.txt", "r", encoding="utf-8") as f:
        labels = [line.strip().split(" ", 1)[-1] for line in f.readlines()]
    return interpreter, input_details, output_details, labels

try:
    interpreter, input_details, output_details, labels = load_model()
    model_ok = True
except Exception as e:
    model_ok = False
    st.error(f"Modelo não encontrado. Certifique-se que `model/model.tflite` e `model/labels.txt` existem. ({e})")

# ── Predição ──────────────────────────────────────────────────────────────────
def predict(image: Image.Image):
    img = image.convert("RGB").resize((224, 224))
    arr = np.array(img, dtype=np.float32)
    arr = (arr / 127.5) - 1.0
    arr = np.expand_dims(arr, axis=0)

    interpreter.set_tensor(input_details[0]["index"], arr)
    interpreter.invoke()
    preds = interpreter.get_tensor(output_details[0]["index"])[0]

    idx  = int(np.argmax(preds))
    conf = float(preds[idx]) * 100
    return labels[idx], conf, preds

# ── Interface ─────────────────────────────────────────────────────────────────
st.markdown('<div class="eco-section-label">como deseja enviar a imagem?</div>', unsafe_allow_html=True)

source = st.radio(
    "",
    ["📁 Fazer upload de arquivo", "📷 Usar câmera"],
    horizontal=True,
    label_visibility="collapsed"
)

image = None

if source == "📁 Fazer upload de arquivo":
    uploaded = st.file_uploader(
        "Selecione uma foto do resíduo",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed"
    )
    if uploaded:
        image = Image.open(uploaded)
else:
    captured = st.camera_input("Tire uma foto do resíduo", label_visibility="collapsed")
    if captured:
        image = Image.open(captured)

# ── Resultado ─────────────────────────────────────────────────────────────────
if image and model_ok:
    col_img, col_res = st.columns([1, 1], gap="medium")

    with col_img:
        st.markdown('<div class="eco-section-label">imagem enviada</div>', unsafe_allow_html=True)
        st.image(image, use_column_width=True)

    with col_res:
        st.markdown('<div class="eco-section-label">resultado</div>', unsafe_allow_html=True)

        with st.spinner("Analisando..."):
            label, confidence, all_probs = predict(image)

        is_recycle = any(w in label.upper() for w in ["RECICL", "SECO", "INORG", "PLASTIC", "PAPEL", "VIDRO", "METAL"])

        if is_recycle:
            st.markdown(f"""
            <div class="eco-result-recycle">
              <div class="eco-result-icon">♻️</div>
              <div>
                <div class="eco-result-label">{label}</div>
                <div class="eco-result-sub">lixo seco · coleta seletiva</div>
              </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div class="eco-tip">
              💡 Descarte no <strong>lixo amarelo ou azul</strong> (coleta seletiva).
              Remova tampas, rótulos e resíduos de alimentos se possível.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="eco-result-organic">
              <div class="eco-result-icon">🌱</div>
              <div>
                <div class="eco-result-label-org">{label}</div>
                <div class="eco-result-sub">lixo orgânico · compostável</div>
              </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div class="eco-tip">
              🌿 Descarte no <strong>lixo marrom ou verde</strong> (orgânico).
              Restos de alimentos podem ser compostados.
            </div>
            """, unsafe_allow_html=True)

        st.write("")
        st.metric("Confiança da análise", f"{confidence:.1f}%")

    with st.expander("Ver probabilidades detalhadas"):
        for lbl, prob in zip(labels, all_probs):
            st.write(f"**{lbl}**")
            st.progress(float(prob), text=f"{prob*100:.1f}%")

elif not image:
    st.markdown("""
    <div class="eco-card" style="text-align:center; padding: 32px 20px;">
      <div style="font-size: 42px; margin-bottom: 10px;">📸</div>
      <div style="font-size: 15px; font-weight: 500;">envie uma foto para começar</div>
      <div style="font-size: 13px; margin-top: 6px;">
        use upload ou câmera para classificar seu resíduo
      </div>
    </div>
    """, unsafe_allow_html=True)
