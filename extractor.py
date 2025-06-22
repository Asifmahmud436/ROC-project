import fitz

doc = fitz.open("roc.pdf")  

with open("output.txt", "w", encoding="utf-8") as output:
    for page_num, page in enumerate(doc, start=1):
        output.write(f"\n--- Page {page_num} ---\n\n")
        
        # Extract plain text
        text = page.get_text("text")
        output.write("📄 Text:\n")
        output.write(text + "\n")

        # Extract links
        links = page.get_links()
        if links:
            output.write("🔗 Links:\n")
            for link in links:
                if "uri" in link:
                    output.write(f"Link: {link['uri']}\n")

print("✅ Extraction complete! Data saved to 'output.txt'")

from groq import Groq
import os
from dotenv import load_dotenv
import json
import re

# Load environment variables
load_dotenv()
MY_KEY = os.getenv("SECRET_KEY")

# Initialize Groq client
client = Groq(api_key=MY_KEY)

# Read content from output.txt
with open('output.txt', "r", encoding="utf-8") as f:
    input_text = f.read()

# Define the system prompt for JSON extraction
system_prompt = """
You are a data extraction assistant.

Your task is to read raw unstructured text from a legal or government form and extract structured information in valid JSON format.

Instructions:
1. Analyze the form text and understand its layout.
2. Identify key fields such as company name, CIN, registered office, auditor details, and appointment type.
3. If any field is missing or not clearly available, leave it as an empty string in the JSON.
4. Return only the JSON object — do not explain anything else.

The final JSON should follow this structure:

{
  "company_name": "",
  "cin": "",
  "registered_office": "",
  "email": "",
  "appointment_date": "",
  "auditor_name": "",
  "auditor_address": "",
  "auditor_pan": "",
  "auditor_frn_or_membership": "",
  "appointment_type": ""
}

Return like this JSON after extracting the values from the following input text. If you think there are more valuable information including this in the text, return those also. We need all important information for the govt files, so you should return all important information. The above is an format only
"""

# sending request to Groq LLaMA model
completion = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=[
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": input_text
        }
    ],
    temperature=1,
    max_completion_tokens=1024,
    top_p=1,
    stream=True,
    stop=None,
)

# Print streamed response as it arrives
response_text = ""
for chunk in completion:
    content = chunk.choices[0].delta.content or ""
    print(content, end="")
    response_text += content

# Clean response_text of markdown-style code blocks
cleaned_json = response_text.strip()

# Remove wrapping ```json or ``` if present
if cleaned_json.startswith("```"):
    cleaned_json = re.sub(r"^```(?:json)?\s*", "", cleaned_json)
    cleaned_json = re.sub(r"\s*```$", "", cleaned_json)

try:
    json_object = json.loads(cleaned_json)
    with open('output.json',"w",encoding='utf-8') as f:
        json.dump(json_object, f, indent=4, ensure_ascii=False)
    print("\n\n Extracted data saved to output.json!")
except json.JSONDecodeError as err:
    print(f"\n\n Failed to decode JSON: {err}")

from pdf2image import convert_from_path
import pytesseract
import glob

pdf_files = glob.glob(r"attachments\*.pdf")

for pdf_path in pdf_files:
    try:
        print(f"\nProcessing: {pdf_path}")
        pages = convert_from_path(pdf_path, dpi=300)
        
        for page_num, img in enumerate(pages, start=1):
            img = img.convert('L')  
            text = pytesseract.image_to_string(img, lang='eng', config='--psm 6')
            
            # Only save if text contains more than just whitespace
            if text.strip():
                output_path = f"{pdf_path[:-4]}_page{page_num}.txt"
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f"✓ Saved: {output_path} (Chars: {len(text)})")
            else:
                print(f"Skipped empty page {page_num}")
                
    except Exception as e:
        print(f"Error processing {pdf_path}: {str(e)}")

print("\nProcessing complete!")

from groq import Groq
import os
from dotenv import load_dotenv
import json
import glob

# Load environment variables
load_dotenv()
MY_KEY = os.getenv("SECRET_KEY")

# Initialize Groq client
client = Groq(api_key=MY_KEY)

with open('output.json','r',encoding='utf-8') as f:
    json_data = json.load(f)

json_string = json.dumps(json_data,indent=1)

txt_contents = []
text_files = glob.glob(r"attachements\*.txt")
for txt in text_files:
    with open(txt, 'r', encoding='utf-8') as f:
            txt_contents.append(f"=== {txt} ===\n{f.read()}\n")

combined_content = (
    "JSON Data:\n" + json_string + "\n\n" +
    "Additional Documents:\n" + "\n".join(txt_contents)
)

completion = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=[
        {
            "role": "system",
            "content": 'summarize the json data for the government in 3-5 lines. Have a professional tone. Example: XYZ Pvt Ltd has appointed M/s Rao & Associates as its statutory auditor for FY 2023–24, effective from 1 July 2023. The appointment has been disclosed via Form ADT-1, with all supporting documents submitted. dont follow this as it is. try to make it better. just return only the summary and nothing else. and for the attachement files, try to provide 2-3 insights and outputs'
        },
        {
            "role": "user",
            "content": combined_content
        }
    ],
    temperature=1,
    max_completion_tokens=1024,
    top_p=1,
    stream=True,
    stop=None,
)

summary_text = ''

for chunk in completion:
    content = chunk.choices[0].delta.content or ""
    summary_text += content

with open('summary.txt','w',encoding='utf-8') as f:
    f.write(summary_text)

print('Summary done')