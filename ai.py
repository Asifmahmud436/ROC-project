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
    with open('info.json',"w",encoding='utf-8') as f:
        json.dump(json_object, f, indent=4, ensure_ascii=False)
    print("\n\n Extracted data saved to info.json!")
except json.JSONDecodeError as err:
    print(f"\n\n Failed to decode JSON: {err}")
