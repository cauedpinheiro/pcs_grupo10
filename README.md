# ♻️ Resíduo — Classificador Inteligente de Resíduos

Aplicação web desenvolvida para o **Projeto Computacional Supervisionado (Grupo 10)** da faculdade. O objetivo é ajudar usuários a identificar corretamente se um resíduo é **reciclável** ou **orgânico** por meio de visão computacional, simplesmente tirando uma foto ou fazendo upload de uma imagem.

---

## 🌿 Sobre o projeto

O descarte incorreto de resíduos é um dos principais problemas ambientais urbanos. Este projeto utiliza um modelo de aprendizado de máquina treinado com imagens reais para classificar resíduos em tempo real, orientando o usuário sobre o descarte correto de forma simples e acessível.

---

## 🚀 Funcionalidades

- 📷 Captura de imagem pela câmera do dispositivo
- 📁 Upload de imagem (jpg, png, webp)
- 🤖 Classificação automática em **Reciclável** ou **Orgânico**
- 📊 Exibição do nível de confiança da análise
- 🌙 Alternância entre tema claro e escuro
- 💡 Dicas de descarte correto para cada tipo de resíduo

---

## 🧠 Tecnologias utilizadas

| Tecnologia | Função |
|---|---|
| [Streamlit](https://streamlit.io) | Interface web |
| [Teachable Machine](https://teachablemachine.withgoogle.com) | Treinamento do modelo de visão computacional |
| [TensorFlow Lite](https://www.tensorflow.org/lite) / [ai-edge-litert](https://pypi.org/project/ai-edge-litert/) | Execução do modelo de IA |
| [Pillow](https://pillow.readthedocs.io) | Processamento de imagens |
| [NumPy](https://numpy.org) | Manipulação de arrays |
| [Streamlit Community Cloud](https://share.streamlit.io) | Deploy e hospedagem |

---

## 📁 Estrutura do repositório

```
pcs_grupo10/
├── app.py                  # Aplicação principal (Streamlit)
├── requirements.txt        # Dependências Python
├── runtime.txt             # Versão do Python
├── .streamlit/
│   └── config.toml         # Configurações visuais do Streamlit
└── model/
    ├── model_unquant.tflite  # Modelo treinado (TensorFlow Lite)
    └── labels.txt            # Classes do modelo (Reciclável / Orgânico)
```

---

## ⚙️ Como rodar localmente

**Pré-requisitos:** Python 3.11+

```bash
# Clone o repositório
git clone https://github.com/cauedpinheiro/pcs_grupo10.git
cd pcs_grupo10

# Instale as dependências
pip install -r requirements.txt

# Rode a aplicação
streamlit run app.py
```

Acesse em `http://localhost:8501`

---

## 🤖 Como o modelo foi treinado

O modelo de visão computacional foi criado no **Google Teachable Machine**:

1. Coleta de imagens para duas classes: `RECICLÁVEL` e `ORGÂNICO`
2. Treinamento supervisionado via interface do Teachable Machine
3. Exportação no formato **TensorFlow Lite (não quantizado)** — `model_unquant.tflite`
4. O modelo recebe imagens `224x224 RGB` e retorna a probabilidade para cada classe

---

## 🗑️ Classes reconhecidas

| Classe | Exemplos | Descarte |
|---|---|---|
| ♻️ **Reciclável** | Plástico, papel, vidro, metal, lata, garrafa PET | Lixo seco (amarelo/azul) |
| 🌱 **Orgânico** | Restos de alimentos, cascas, folhas | Lixo orgânico (marrom/verde) |

---

## 👥 Equipe

Desenvolvido pelo **Grupo 10**:
Cauê Dias P R dos Santos (17883981);
Luiz Guilherme de Faria Oliveira (17909126);
Guylhermme Renzo S C da Silva (17863276);


Projeto Semestral da disciplina de PCS3100 (Introdução à Engenharia de Computação)
---

## 📄 Licença

Este projeto é de uso acadêmico.
