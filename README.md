
# Filesure - Form ADT-1 Extractor

This project extracts structured data from a real-world Form ADT-1 PDF filing using Python. It demonstrates how regulatory documents can be transformed into clean, machine-readable formats and plain-English summaries — a core goal at Filesure.


## 🔧 Features

- Parses Form ADT-1 PDF using PyMuPDF (or relevant libraries).

- Extracts key fields: company details, auditor info, appointment data.

- Outputs a well-structured output.json.

- Generates an AI-style summary (summary.txt) from the extracted JSON.

- Bonus: Extracts and summarizes embedded attachments (if present).


## 📁 Files Included

- extractor.py – Main Python script to extract and process data.

- output.json – Structured data extracted from the form.

- summary.txt – AI-generated plain-language summary.

- README.md – This file.

- demo.mp4 – Screen recording walkthrough.


## ▶️ How to Run

First of all fork it and clone it to your pc. Then open terminal and install all necessary packages:

```bash
  pip install requirements.txt
```
You have to manually install pytesseract and poppler in your Pc and also add it to the system variable path incase there is a pdf which contains image of text!

After doing the above steps you can run the project by:
```bash
  py extractor.py
```