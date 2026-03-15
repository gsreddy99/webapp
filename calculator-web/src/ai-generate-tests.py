import os
import json
from openai import OpenAI

# ------------------------------------------------------------
# Load Azure OpenAI configuration from environment variables
# ------------------------------------------------------------
AOAI_ENDPOINT = os.getenv("AOAI_ENDPOINT")
AOAI_KEY = os.getenv("AOAI_KEY")
AOAI_DEPLOYMENT = os.getenv("AOAI_DEPLOYMENT")

if not AOAI_ENDPOINT or not AOAI_ENDPOINT.startswith("https://"):
    raise ValueError("AOAI_ENDPOINT must start with https:// and end with /")

# ------------------------------------------------------------
# Initialize Azure OpenAI client
# ------------------------------------------------------------
client = OpenAI(
    api_key=AOAI_KEY,
    base_url=AOAI_ENDPOINT
)

# ------------------------------------------------------------
# Read HTML files to give the model context
# ------------------------------------------------------------
def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""

signin_html = read_file("public/signin.html")
store_html = read_file("public/store.html")

# ------------------------------------------------------------
# Prompt for generating Playwright tests
# ------------------------------------------------------------
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

# ------------------------------------------------------------
# Call Azure OpenAI
# ------------------------------------------------------------
response = client.chat.completions.create(
    model=AOAI_DEPLOYMENT,
    messages=[
        {"role": "system", "content": "You generate high-quality Playwright tests."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.2
)

generated_code = response.choices[0].message.content

# ------------------------------------------------------------
# Ensure output folder exists
# ------------------------------------------------------------
os.makedirs("tests", exist_ok=True)

# ------------------------------------------------------------
# Write generated Playwright tests
# ------------------------------------------------------------
output_path = "tests/generated.spec.js"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(generated_code)

print(f"AI-generated Playwright tests written to: {output_path}")
