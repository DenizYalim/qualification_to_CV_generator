from docx import Document
from docx2pdf import convert
from pathlib import Path
import json

TEMPLATES_FOLDER = Path("../CV_templates")
OUTPUT_FOLDER = Path("../CVs_generated")
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

def _replace_in_paragraph(paragraph, mapping):
    if not mapping or "{{" not in paragraph.text:
        return
    for key, val in mapping.items():
        ph = f"{{{{{key}}}}}"  # e.g. {{full_name}}
        if ph in paragraph.text:
            for run in paragraph.runs:
                run.text = run.text.replace(ph, str(val))
                print(f"trying replacement {run.text}, {val}")

def _replace_in_doc(doc: Document, mapping: dict):
    for p in doc.paragraphs:
        _replace_in_paragraph(p, mapping)
    for tbl in doc.tables:
        for row in tbl.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    _replace_in_paragraph(p, mapping)

def fill_cv(template_file_name: str, values: dict) -> Path:
    template_path = TEMPLATES_FOLDER / template_file_name
    doc = Document(template_path)

    _replace_in_doc(doc, values)

    out_docx = OUTPUT_FOLDER / f"filled_{Path(template_file_name).stem}.docx"
    doc.save(out_docx)
    return out_docx

def convert_to_pdf(doc_path: Path) -> Path:
    pdf_path = doc_path.with_suffix(".pdf")
    convert(str(doc_path), str(pdf_path))  # Requires Word on Windows
    return pdf_path

if __name__ == "__main__":
    with open("../example_values.json", "r", encoding="utf-8") as f:
        values = json.load(f)

    out_docx = fill_cv("simpler_template.docx", values)
    # pdf_path = convert_to_pdf(out_docx)
