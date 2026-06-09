import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf

# ── Configuração da página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Classificador de Resíduos",
    page_icon="♻️",
    layout="centered"
)

# ── Carrega modelo (cached para não recarregar a cada interação) ────────────
@st.cache_resource
def load_model():
    model = tf.keras.models.load_model("model/keras_model.h5", compile=False)
    with open("model/labels.txt", "r") as f:
        labels = [line.strip().split(" ", 1)[-1] for line in f.readlines()]
    return model, labels

model, labels = load_model()

# ── Função de predição ──────────────────────────────────────────────────────
def predict(image: Image.Image):
    # Teachable Machine usa imagens 224x224 RGB
    img = image.convert("RGB").resize((224, 224))
    arr = np.array(img, dtype=np.float32)
    arr = (arr / 127.5) - 1.0          # normalização padrão do Teachable Machine
    arr = np.expand_dims(arr, axis=0)   # batch de 1
    predictions = model.predict(arr, verbose=0)
    idx = np.argmax(predictions[0])
    confidence = float(predictions[0][idx]) * 100
    return labels[idx], confidence, predictions[0]

# ── Interface ───────────────────────────────────────────────────────────────
st.title("♻️ Classificador de Resíduos")
st.markdown("Envie ou tire uma foto do resíduo para descobrir se ele é **reciclável** ou **orgânico**.")

st.divider()

source = st.radio(
    "Como você quer enviar a imagem?",
    ["📁 Fazer upload de arquivo", "📷 Usar câmera"],
    horizontal=True
)

image = None

if source == "📁 Fazer upload de arquivo":
    uploaded = st.file_uploader(
        "Selecione uma imagem", type=["jpg", "jpeg", "png", "webp"]
    )
    if uploaded:
        image = Image.open(uploaded)

else:
    captured = st.camera_input("Tire uma foto do resíduo")
    if captured:
        image = Image.open(captured)

# ── Resultado ───────────────────────────────────────────────────────────────
if image:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.image(image, caption="Imagem enviada", use_column_width=True)

    with col2:
        with st.spinner("Analisando..."):
            label, confidence, all_probs = predict(image)

        is_recyclable = "RECICLÁVEL" in label.upper() or "RECICL" in label.upper()

        if is_recyclable:
            st.success(f"## ♻️ {label}")
            st.markdown("Este resíduo é **reciclável**. Descarte no **lixo seco** (geralmente amarelo ou azul).")
        else:
            st.warning(f"## 🌱 {label}")
            st.markdown("Este resíduo é **orgânico**. Descarte no **lixo orgânico** (geralmente marrom ou verde).")

        st.metric("Confiança", f"{confidence:.1f}%")

        with st.expander("Ver probabilidades detalhadas"):
            for lbl, prob in zip(labels, all_probs):
                st.progress(float(prob), text=f"{lbl}: {prob*100:.1f}%")