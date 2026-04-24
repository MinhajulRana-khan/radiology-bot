import gradio as gr
from google import genai
from PIL import Image
import os
import threading
import subprocess

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

def generate_report(image):
    try:
        img = image.resize((512, 512), Image.LANCZOS)
        prompt = """You are an expert radiologist. Analyze this chest X-ray image and generate a structured radiology report.

Return ONLY this format:

FINDINGS:
[Describe lung fields, heart size, mediastinum, bones, any abnormalities]

IMPRESSION:
[1-3 sentence clinical summary and conclusion]

RECOMMENDATION:
[Follow-up suggestion or "No further imaging required."]

⚠️ AI-generated report for research purposes only. Not for clinical use."""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt, img]
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Start Telegram bot in background thread
def run_bot():
    subprocess.Popen(["python", "bot.py"])

threading.Thread(target=run_bot, daemon=True).start()

demo = gr.Interface(
    fn=generate_report,
    inputs=gr.Image(type="pil", label="Upload Chest X-Ray"),
    outputs=gr.Textbox(label="AI Radiology Report", lines=15),
    title="🩺 AI Radiology Report Generator",
    description="Upload a chest X-ray image and get an AI-generated radiology report instantly.\n\n⚠️ For research purposes only. Not for clinical use.",
    examples=[],
)

if __name__ == "__main__":
    demo.launch(show_error=True)
