import gradio as gr
from google import genai
from PIL import Image
import os
import tempfile
import urllib.request
import unicodedata
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

# Download fonts once at startup
font_path = "/tmp/NotoSans.ttf"
font_path_bengali = "/tmp/NotoSansBengali.ttf"

if not os.path.exists(font_path):
    urllib.request.urlretrieve(
        "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSans/NotoSans-Regular.ttf",
        font_path
    )

if not os.path.exists(font_path_bengali):
    urllib.request.urlretrieve(
        "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSansBengali/NotoSansBengali-Regular.ttf",
        font_path_bengali
    )

pdfmetrics.registerFont(TTFont("NotoSans", font_path))
pdfmetrics.registerFont(TTFont("NotoSansBengali", font_path_bengali))


def generate_report(image, patient_name, patient_id, patient_age, patient_gender, language):
    try:
        img = image.resize((512, 512), Image.LANCZOS)

        if language == "English":
            lang_instruction = "Write the report in English only."
        elif language == "Bengali":
            lang_instruction = "Write the entire report in Bengali language only."
        else:
            lang_instruction = "Write the report in both English and Bengali. First write the full report in English, then write the full report in Bengali below it."

        prompt = f"""You are an expert radiologist. Analyze this chest X-ray image and generate a structured radiology report.
{lang_instruction}
Return ONLY this format:
FINDINGS:
[Describe lung fields, heart size, mediastinum, bones, any abnormalities]
IMPRESSION:
[1-3 sentence clinical summary and conclusion]
RECOMMENDATION:
[Follow-up suggestion or 'No further imaging required.']
⚠️ AI-generated report for research purposes only. Not for clinical use."""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt, img]
        )
        return response.text

    except Exception as e:
        return f"Error: {str(e)}"


def export_pdf(report_text, patient_name, patient_id, patient_age, patient_gender):
    if not report_text or report_text.strip() == "":
        return None
    try:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        doc = SimpleDocTemplate(tmp.name, pagesize=A4,
                                rightMargin=20*mm, leftMargin=20*mm,
                                topMargin=20*mm, bottomMargin=20*mm)

        title_style = ParagraphStyle(
            'Title', fontName='NotoSans', fontSize=18,
            spaceAfter=10, alignment=1
        )
        heading_style = ParagraphStyle(
            'Heading', fontName='NotoSans', fontSize=13,
            spaceAfter=6, spaceBefore=10
        )
        normal_style = ParagraphStyle(
            'Normal', fontName='NotoSans', fontSize=10,
            spaceAfter=4, leading=16
        )
        bengali_style = ParagraphStyle(
            'Bengali', fontName='NotoSansBengali', fontSize=11,
            spaceAfter=4, leading=20
        )

        story = []

        # Title
        story.append(Paragraph("AI Radiology Report", title_style))
        story.append(Spacer(1, 5*mm))

        # Patient info
        story.append(Paragraph("Patient Information", heading_style))
        story.append(Paragraph(f"Name   : {patient_name or 'N/A'}", normal_style))
        story.append(Paragraph(f"ID     : {patient_id or 'N/A'}", normal_style))
        story.append(Paragraph(f"Age    : {patient_age or 'N/A'}", normal_style))
        story.append(Paragraph(f"Gender : {patient_gender or 'N/A'}", normal_style))
        story.append(Spacer(1, 5*mm))

        # Report
        story.append(Paragraph("Radiology Report", heading_style))

        for line in report_text.split('\n'):
            if not line.strip():
                story.append(Spacer(1, 3*mm))
                continue
            has_bengali = any('\u0980' <= ch <= '\u09FF' for ch in line)
            if has_bengali:
                line = unicodedata.normalize('NFC', line)
                story.append(Paragraph(line, bengali_style))
            else:
                story.append(Paragraph(line, normal_style))

        story.append(Spacer(1, 5*mm))
        story.append(Paragraph(
            "AI-generated report for research purposes only. Not for clinical use.",
            normal_style
        ))

        doc.build(story)
        return tmp.name

    except Exception as e:
        return f"Error generating PDF: {str(e)}"


# UI
with gr.Blocks(title="AI Radiology Report Generator") as demo:
    gr.Markdown("# 🩺 AI Radiology Report Generator")
    gr.Markdown("Upload a chest X-ray and get an AI-generated structured radiology report.\n\n⚠️ *For research purposes only. Not for clinical use.*")

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 👤 Patient Information")
            patient_name = gr.Textbox(label="Patient Name", placeholder="e.g. John Doe")
            patient_id = gr.Textbox(label="Patient ID", placeholder="e.g. P-12345")
            patient_age = gr.Textbox(label="Age", placeholder="e.g. 45")
            patient_gender = gr.Dropdown(["Male", "Female", "Other"], label="Gender")
            language = gr.Dropdown(
                ["English", "Bengali", "Both (English + Bengali)"],
                label="Report Language",
                value="English"
            )
            image_input = gr.Image(type="pil", label="📷 Upload Chest X-Ray")
            generate_btn = gr.Button("🔍 Generate Report", variant="primary")

        with gr.Column(scale=1):
            gr.Markdown("### 📋 Generated Report")
            report_output = gr.Textbox(label="AI Radiology Report", lines=20)
            export_btn = gr.Button("📄 Export as PDF", variant="secondary")
            pdf_output = gr.File(label="⬇️ Download PDF")

    generate_btn.click(
        fn=generate_report,
        inputs=[image_input, patient_name, patient_id, patient_age, patient_gender, language],
        outputs=report_output
    )

    export_btn.click(
        fn=export_pdf,
        inputs=[report_output, patient_name, patient_id, patient_age, patient_gender],
        outputs=pdf_output
    )

if __name__ == "__main__":
    demo.launch()
