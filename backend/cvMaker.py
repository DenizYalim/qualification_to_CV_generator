from docx import Document  # doc manipulator
from docx2pdf import convert  # doc to pdf

TEMPLATES_FOLDER = "../CV_templates"
OUTPUT_FOLDER = "../CVs_generated"


"""sumary_line

Keyword arguments:
data : dict
Return: return_description
"""


def fill_line(line, keyword, text):
    pass


"""def copy_doc(template):
    doc = Document(template)
    doc.save()"""


def fill_cv(template_file_name, values):
    template_file = TEMPLATES_FOLDER + "/" + template_file_name
    doc = Document(template_file_name)  # This is probably destructive

    for paragraph in doc.paragraphs:
        for key, value in values.items():
            if f"{{key}}" in paragraph.text:
                inline = paragraph.runs
                for i in range(len(inline)):
                    if f"{{key}}" in inline[i].text:
                        inline[i].replace(f"{{key}}", value)
        doc.save(OUTPUT_FOLDER)


def convert_to_pdf(doc_path, pdf_path):
    convert(doc_path, pdf_path)

if __name__ == "__main__":
    print("hey")