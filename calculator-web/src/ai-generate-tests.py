import os
from pathlib import Path
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
MODEL = "gpt-4o-mini"

# Prompt for generating Playwright tests
prompt = """
You are an expert QA engineer. Generate Playwright functional tests for the following pages.
Use ONLY selectors that exist in the HTML/JS described below.

SIGNIN PAGE STRUCTURE:
- Two input fields have class "dynamic-field"
- The login button has id "login-btn"
- There is NO validation; clicking login always redirects to store.html

STORE PAGE STRUCTURE:
- Items are inside #items-container > div
- Each item has:
  - an input for price (IMPORTANT: it is just <input>, no type attribute)
  - a button that opens a popup
- Popup has id="popup"
- Confirm button id="confirm-btn"
- Cancel button id="cancel-btn"

TESTS TO GENERATE:
1. Sign-in page loads
2. User can type into both dynamic-field inputs
3. Clicking login redirects to store.html
4. Store page loads items
5. Clicking Update opens popup
6. Clicking Cancel closes popup
7. Clicking Confirm logs price update and closes popup

REQUIREMENTS:
- Return ONLY valid JavaScript for Playwright.
- MUST begin with: const { test, expect } = require('@playwright/test');
- No markdown fences.
- Use test.describe and test blocks.
- Use page.goto('/signin.html') and page.goto('/store.html').
- Use stable selectors based on the structure above.
- For item count, ALWAYS use: await expect(items).toHaveCount(2);
- NEVER use toHaveCountGreaterThan or any matcher that does not exist in Playwright.
- For the price input, ALWAYS use: locator('input')
- NEVER use input[type="text"] or any attribute selector.
"""

# Call OpenAI to generate the test file
response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You generate high-quality Playwright tests."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.2
)

generated_code = response.choices[0].message.content

# Strip markdown fences if present
for fence in ["```javascript", "```js", "```"]:
    generated_code = generated_code.replace(fence, "")

generated_code = generated_code.strip()

# Ensure import line exists
IMPORT_LINE = "const { test, expect } = require('@playwright/test');"
if not generated_code.startswith("const { test"):
    generated_code = IMPORT_LINE + "\n\n" + generated_code

# Ensure tests directory exists
Path("tests").mkdir(exist_ok=True)

# Write the generated test file
output_path = Path("tests/generated.spec.js")
output_path.write_text(generated_code, encoding="utf-8")

print("AI-generated Playwright tests written to tests/generated.spec.js")
