---

## 📊 Dataset

**Indiana University Chest X-rays**
- 3,788 frontal chest X-ray images
- Paired radiology reports (findings + impression)
- Source: [Kaggle](https://www.kaggle.com/datasets/raddar/chest-xrays-indiana-university)

---

## 📈 Evaluation Results

| Metric | Score |
|--------|-------|
| BLEU | 0.0383 |
| ROUGE-1 | 0.2199 |
| ROUGE-2 | 0.1389 |
| ROUGE-L | 0.2127 |

> Note: Low BLEU/ROUGE scores are expected in medical report generation as AI uses different but clinically equivalent wording compared to ground truth.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Vision AI | Google Gemini 2.5 Flash |
| Web UI | Gradio |
| PDF Export | ReportLab |
| Telegram Bot | python-telegram-bot v20 |
| Bot Hosting | Railway |
| Model Hosting | Hugging Face Spaces |
| Dataset | Indiana University Chest X-rays |
| Evaluation | BLEU, ROUGE |
| Notebook | Kaggle |

---

## 🚀 How to Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/ai-radiology-report-generator.git
cd ai-radiology-report-generator
```

### 2. Install dependencies
```bash
pip install gradio google-genai Pillow reportlab
```

### 3. Set your Gemini API key
```bash
export GEMINI_API_KEY="your_api_key_here"
```

### 4. Run the web app
```bash
cd huggingface_streamlit
python app.py
```

### 5. Run the Telegram bot
```bash
cd telegram_bot
export BOT_TOKEN="your_bot_token_here"
python bot.py
```

---

## ⚠️ Disclaimer

This system is developed for **research purposes only**. It is **not intended for clinical use**. Always consult a qualified radiologist for medical diagnosis.

---

## 👨‍💻 Author

**Minhajul Islam**
Student, Daffodil International University (DIU), Bangladesh
Independent AI Research Project — EMR & PACS Integration

---

## 📄 License

MIT License — feel free to use, modify, and distribute with attribution.
