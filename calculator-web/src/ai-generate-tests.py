import os
from pathlib import Path
from openai import AzureOpenAI

# ---------------------------------------------------------
# Azure OpenAI Client (same pattern as your API contract script)
# ---------------------------------------------------------
client = AzureOpenAI(
    api_key=os.environ["AOAI_KEY"],
    azure_endpoint=os.environ["AOAI_ENDPOINT"],
    api_version="2024-12-01-preview"
)

deployment = os.environ["AOAI_DEPLOYMENT"]

# ---------------------------------------------------------
# Files to read
# ---------------------------------------------------------
ROOT = Path(__file__).parent
PUBLIC = ROOT / "public"

signin_html = (PUBLIC / "signin.html").read_text()
store_html = (PUBLIC / "store.html").read_text()

# ---------------------------------------------------------
# Prompt
# ---------------------------------------------------------
prompt = f"""
You are an expert Playwright test generator.

Generate Playwright tests for these pages:

SIGNIN.HTML:
{signin_html}

STORE.HTML:
{store_html}

Rules:
- Use Playwright Test syntax
- Use baseURL (no hardcoded URLs)
- Use getByPlaceholder, getByRole, or #id selectors
- Produce a single file named generated.spec.js
- Do NOT include explanations, only valid JavaScript test code
"""

# ---------------------------------------------------------
# Call Azure OpenAI
# ---------------------------------------------------------
response = client.chat.completions.create(
    model=deployment,
    messages=[
        {"role": "system", "content": "You are an expert Playwright test generator."},
        {"role": "user", "content": prompt}
    ],
    max_completion_tokens=2000
)

content = response.choices[0].message.content

# ---------------------------------------------------------
# Write tests
# ---------------------------------------------------------
tests_dir = ROOT / "tests"
tests_dir.mkdir(exist_ok=True)

output_file = tests_dir / "generated.spec.js"
output_file.write_text(content)

print("AI-generated Playwright tests written to:", output_file)
