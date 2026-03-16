import os
import re
from pathlib import Path
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
MODEL = "gpt-4o-mini"

# ---------------------------------------------------------
# STEP 1 — Read Playwright output and detect failing test
# ---------------------------------------------------------

log_path = Path("playwright-output.log")
if not log_path.exists():
    print("No playwright-output.log found. Nothing to fix.")
    raise SystemExit(0)

log_text = log_path.read_text(encoding="utf-8")

# Example failure line:
# [7/7] tests/generated.spec.js:51:3 › Functional Tests › Clicking Confirm logs price update and closes popup
match = re.search(r"› (.+)", log_text)
if not match:
    print("No failing test name found in output.")
    raise SystemExit(0)

failing_test_name = match.group(1).strip()
print(f"\nDetected failing test: {failing_test_name}\n")

# ---------------------------------------------------------
# STEP 2 — Extract existing generated.spec.js
# ---------------------------------------------------------

spec_path = Path("tests/generated.spec.js")
if not spec_path.exists():
    print("generated.spec.js not found.")
    raise SystemExit(0)

spec_text = spec_path.read_text(encoding="utf-8")

# Extract the failing test block
pattern = rf"(test\(['\"]{re.escape(failing_test_name)}['\"].*?}}\);)"
match = re.search(pattern, spec_text, re.DOTALL)

if not match:
    print("Could not locate failing test block in generated.spec.js")
    raise SystemExit(0)

old_test_block = match.group(1)

print("\n=== OLD TEST BLOCK ===\n")
print(old_test_block)
print("\n=======================\n")

# ---------------------------------------------------------
# STEP 3 — Ask AI to regenerate ONLY this test
# ---------------------------------------------------------

prompt = f"""
You are an expert QA engineer. Rewrite ONLY the following Playwright test so that it passes.

RULES:
- Use ONLY selectors that exist in the DOM described earlier.
- The price input is <input> with no type attribute.
- Items are inside #items-container > div.
- Popup has id="popup".
- Confirm button id="confirm-btn".
- Cancel button id="cancel-btn".
- MUST begin with: test('{failing_test_name}', async ({{ page }}) => {{
- MUST NOT include markdown fences.
- MUST NOT modify any other tests.
- MUST NOT change the test name.

Here is the failing test:

{old_test_block}

Rewrite it correctly:
"""

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You fix Playwright tests like a senior SDET."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.2
)

new_test_block = response.choices[0].message.content.strip()

# Remove accidental markdown fences
for fence in ["```javascript", "```js", "```"]:
    new_test_block = new_test_block.replace(fence, "")

print("\n=== NEW TEST BLOCK ===\n")
print(new_test_block)
print("\n=======================\n")

# ---------------------------------------------------------
# STEP 4 — Replace old test block with new one
# ---------------------------------------------------------

updated_spec = spec_text.replace(old_test_block, new_test_block)

spec_path.write_text(updated_spec, encoding="utf-8")

print("Updated generated.spec.js with fixed test.")
