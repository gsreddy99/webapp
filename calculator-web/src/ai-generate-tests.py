import os
import json
from pathlib import Path
import requests

# ---------------------------------------------------------
# GitHub Models API endpoint
# ---------------------------------------------------------
API_URL = "https://models.inference.ai.azure.com/chat/completions"
MODEL = "gpt-4o-mini"

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]

# ---------------------------------------------------------
# Read HTML files
# ---------------------------------------------------------
def read_file(path):
    try:
        return Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""

signin_html = read_file("public/signin.html")
store_html = read_file("public/store.html")

# ---------------------------------------------------------
# Prompt for generating Playwright tests
# ---------------------------------------------------------
prompt = f"""
You are an expert QA engineer. Generate Playwright functional tests
for the following HTML pages. Use stable selectors and cover:

- Page load
- Required fields
- Valid and invalid inputs
- Button clicks
- Navigation
- Error messages
- Success flows

Return ONLY valid JavaScript code for Playwright.

--- signin.html ---
{signin_html}

--- store.html ---
{store_html}
"""

# ---------------------------------------------------------
# Call GitHub Models using raw HTTP
# ---------------------------------------------------------
headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json"
}

payload = {
    "model": MODEL,
    "messages": [
        {"role": "system", "content": "You generate high-quality Playwright tests."},
        {"role": "user", "content": prompt}
    ],
    "temperature": 0.2
}

response = requests.post(API_URL, headers=headers, json=payload)

if response.status_code != 200:
    print("ERROR calling GitHub Models:")
    print(response.text)
    raise SystemExit(1)

generated_code = response.json()["choices"][0]["message"]["content"]

# ---------------------------------------------------------
# Ensure output folder exists
# ---------------------------------------------------------
Path("tests").mkdir(exist_ok=True)

# ---------------------------------------------------------
# Write generated Playwright tests
# ---------------------------------------------------------
output_path = Path("tests/generated.spec.js")
output_path.write_text(generated_code, encoding="utf-8")

print(f"AI-generated Playwright tests written to: {output_path}")
