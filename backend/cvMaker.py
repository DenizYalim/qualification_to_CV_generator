from docx import Document # doc manipulator
from docx2pdf import convert # doc to pdf

TEMPLATE_PATH
OUTPUT_PATH

"""sumary_line

Keyword arguments:
data : dict
Return: return_description
"""

def fill_cv(data):
    doc = Document(TEMPLATE_PATH)

    for paragraph in doc.paragraphs:
        for key, value in data:
            if f"{{key}}" in paragraph.text:
                inline = paragraph.runs
                for i in range(len(inline)):
                    if f"{{key}}" in inline[i].text:
                        inline[i].replace(f"{{key}}",value)
        doc.save(OUTPUT_PATH)

def convert_to_pdf(doc_path, pdf_path):
    convert(doc_path, pdf_path)

