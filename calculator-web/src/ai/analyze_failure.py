import os
from pathlib import Path
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
MODEL = "gpt-4o-mini"

log_path = Path("playwright-output.log")

if not log_path.exists():
    print("No playwright-output.log found. Nothing to analyze.")
    raise SystemExit(0)

log_text = log_path.read_text(encoding="utf-8")

prompt = f"""
You are a senior QA engineer. Analyze the following Playwright test output.

Identify:
- Which test(s) failed
- The root cause (selector issue, timing, popup not visible, wrong assertion, etc.)
- The exact line(s) likely needing change
- A short, clear fix recommendation

PLAYWRIGHT OUTPUT:
{log_text}
"""

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You analyze Playwright failures like a senior SDET."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.1
)

analysis = response.choices[0].message.content.strip()

Path("ai_failure_analysis.txt").write_text(analysis, encoding="utf-8")

print("\n=== AI FAILURE ANALYSIS ===\n")
print(analysis)
print("\n===========================\n")
