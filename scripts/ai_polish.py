import sys, glob, os, openai

# Debug prints
print("→ AI-Polish args:", sys.argv[1:])
print("→ Matching files:", [f for pat in sys.argv[1:] for f in glob.glob(pat, recursive=True)])

openai.api_key = os.getenv("OPENAI_API_KEY")

patterns = sys.argv[1:]
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
            {"role": "user",   "content": "Please rewrite this LaTeX section to improve clarity, flow, and academic tone:\n\n" + original}
        ],
        temperature=0.2,
    )

    polished = response.choices[0].message.content

    if polished.strip() and polished != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(polished)
        print(f" → Updated {filepath}")
    else:
        print(f" → No change for {filepath}")
