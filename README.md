# AI Radiology Report Generator

An AI-powered system that automatically generates structured radiology reports from chest X-ray images using Google Gemini Vision API. Built as part of an independent research project on EMR and PACS integration at Daffodil International University (DIU), Bangladesh.

---

## Live Demo

- Web App: https://huggingface.co/spaces/Minhajul-islam/radiology-streamlit-ui
- Telegram Bot: https://t.me/Willpower6316Bot

---

## Features

- Upload chest X-ray images (PNG, JPG, JPEG)
- AI-generated structured radiology reports
- Bilingual output in English and Bengali
- Patient information input (Name, ID, Age, Gender)
- Export report as downloadable PDF
- Telegram bot for instant report generation
- BLEU and ROUGE evaluation against ground truth reports

---

## Project Architecture

User uploads X-ray → Gradio Web UI or Telegram Bot → Google Gemini 2.5 Flash Vision API → Structured Radiology Report (Findings + Impression + Recommendation) → PDF Export or Telegram Message

---

## Project Structure

ai-radiology-report-generator/
│
├── notebooks/
│   └── radiology_pipeline.ipynb
│
├── huggingface_gradio/
│   ├── app.py
│   └── requirements.txt
│
├── huggingface_streamlit/
│   ├── app.py
│   └── requirements.txt
│
├── telegram_bot/
│   ├── bot.py
│   ├── requirements.txt
│   └── Procfile
│
└── README.md

---

## Dataset

Indiana University Chest X-rays
- 3,788 frontal chest X-ray images
- Paired radiology reports (findings + impression)
- Source: https://www.kaggle.com/datasets/raddar/chest-xrays-indiana-university

---

## Evaluation Results

| Metric | Score |
|--------|-------|
| BLEU | 0.0383 |
| ROUGE-1 | 0.2199 |
| ROUGE-2 | 0.1389 |
| ROUGE-L | 0.2127 |

Note: Low BLEU and ROUGE scores are expected in medical report generation as AI uses different but clinically equivalent wording compared to ground truth.

---

## Tech Stack

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

## How to Run Locally

### 1. Clone the repo
git clone https://github.com/MinhajulRana-khan/ai-radiology-report-generator.git
cd ai-radiology-report-generator

### 2. Install dependencies
pip install gradio google-genai Pillow reportlab

### 3. Set your Gemini API key
export GEMINI_API_KEY="your_api_key_here"

### 4. Run the web app
cd huggingface_streamlit
python app.py

### 5. Run the Telegram bot
cd telegram_bot
export BOT_TOKEN="your_bot_token_here"
python bot.py

---

## Disclaimer

This system is developed for research purposes only. It is not intended for clinical use. Always consult a qualified radiologist for medical diagnosis.

---

## Author

Minhajul Islam
Student, Daffodil International University (DIU), Bangladesh
Independent AI Research Project on EMR and PACS Integration

---

## License

MIT License
