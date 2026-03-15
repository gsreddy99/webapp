import os
from pathlib import Path
from openai import OpenAI

# ---------------------------------------------------------
# GitHub Models Client (no Azure needed)
# ---------------------------------------------------------
client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.environ["GITHUB_TOKEN"]
)

MODEL = "gpt-4o-mini"   # Free, fast, perfect for test generation

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
# Call GitHub Models
# ---------------------------------------------------------
response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You generate high-quality Playwright tests."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.2
)

generated_code = response.choices[0].message.content

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
