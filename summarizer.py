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

with open('info.json','r',encoding='utf-8') as f:
    json_data = json.load(f)

json_string = json.dumps(json_data,indent=1)

completion = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=[
        {
            "role": "system",
            "content": 'summarize the json data for the government in 3-5 lines. Have a professional tone. Example: XYZ Pvt Ltd has appointed M/s Rao & Associates as its statutory auditor for FY 2023–24, effective from 1 July 2023. The appointment has been disclosed via Form ADT-1, with all supporting documents submitted. dont follow this as it is. try to make it better. just return only the summary and nothing else'
        },
        {
            "role": "user",
            "content": json_string
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