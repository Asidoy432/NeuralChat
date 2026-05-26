# ◈ NeuralChat AI — Lab 10.0 (Streamlit)

Multi-modal AI app built with **Streamlit + Python**.

| Feature | Powered by |
|---|---|
| 💬 Chat | Claude Sonnet (Anthropic API) |
| 🎨 Image Gen | Amazon Nova Canvas via AppDeploy |

---

## 📁 File Structure

```
NeuralChat-Streamlit/
├── app.py                           ← Main Streamlit app
├── requirements.txt                 ← Python dependencies
├── .gitignore                       ← Keeps secrets off GitHub
├── README.md                        ← This file
└── .streamlit/
    ├── config.toml                  ← Dark theme
    └── secrets.toml.example         ← API key template (safe to commit)
```

> ⚠️ `.streamlit/secrets.toml` is in `.gitignore` — never commit it!

---

## 🚀 Deploy on Streamlit Cloud (Free)

### Step 1 — Push to GitHub

1. Go to [github.com/new](https://github.com/new) and create a new repo
2. Upload all files — including the `.streamlit/` folder

```bash
git init
git add .
git commit -m "Initial NeuralChat deploy"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

---

### Step 2 — Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click **"New app"**
4. Set:
   - Repository → your repo
   - Branch → `main`
   - Main file path → `app.py`
5. Click **"Advanced settings"** → **Secrets**
6. Paste this:

```toml
ANTHROPIC_API_KEY = "sk-ant-api03-your-actual-key-here"
```

7. Click **Deploy!**

---

## 🔑 Get Your Anthropic API Key

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up / Log in
3. Click **API Keys** → **Create Key**
4. Copy the key — it only shows once!

> New accounts get **$5 free credits** — enough for hundreds of messages.

---

## 💻 Run Locally

```bash
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit .streamlit/secrets.toml with your real key
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501)
