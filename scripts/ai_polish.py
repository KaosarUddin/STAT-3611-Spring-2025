import sys, glob, os, openai
import sys, glob
print("Args:", sys.argv[1:])
print("Found files:", [f for pat in sys.argv[1:] for f in glob.glob(pat)])
openai.api_key = os.getenv("OPENAI_API_KEY")

# Accept multiple glob patterns from the CLI
patterns = sys.argv[1:]

# Collect all matching .tex files
files = []
for pat in patterns:
    files.extend(glob.glob(pat, recursive=True))

for filepath in sorted(set(files)):
    print(f"Polishing {filepath}…")
    with open(filepath, "r", encoding="utf-8") as f:
        original = f.read()

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert academic editor. Preserve all LaTeX math and structure."},
            {"role": "user", "content": "Please rewrite this LaTeX section to improve clarity, flow, and academic tone:\n\n" + original}
        ],
        temperature=0.2,
    )

    polished = response.choices[0].message.content

    # Overwrite only if changed
    if polished.strip() and polished != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(polished)
        print(f" → Updated {filepath}")
    else:
        print(f" → No change for {filepath}")

