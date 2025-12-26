import re
import json
import argparse

SCRUBBER_VERSION = "v1"

PATTERNS = {
    "EMAIL": re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"),
    "PHONE": re.compile(r"\b(?:\+?\d{1,3}[\s-]?)?(?:\(?\d{2,4}\)?[\s-]?)?\d{3,4}[\s-]?\d{3,4}\b"),
    "DOB": re.compile(r"\b(?:DOB[:\s]*)?\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b"),
    "APPT_ID": re.compile(r"\b(?:APPT|BKG|INV)[-_]?\d+\b"),
    "INSURANCE_ID": re.compile(r"\b[A-Z]{2,}-[A-Z]{2}-\d+\b"),
    "GOV_ID": re.compile(r"\b(?:\d{3}-\d{2}-\d{4}|\d{4}\s\d{4}\s\d{4}|\d{4}\s\d{5}\s\d)\b"),
    "URL": re.compile(r"https?://\S+"),
}

NAME_RE = re.compile(r"\b(Dr\.?\s)?[A-Z][a-z]+(?:\s[A-Z][a-z]+)+\b")
ADDRESS_RE = re.compile(
    r"\b\d{1,4}\s[\w\s]+(?:Street|St|Road|Rd|Lane|Ln|Avenue|Ave|Blvd),?\s[\w\s]+\d{4,6}\b",
    re.IGNORECASE
)
PROVIDER_RE = re.compile(
    r"\b(?:Clinic|Hospital|Pathology|Fertility|IVF|Labs|Health)\b.*?(?:Clinic|Labs|IVF|Hospital)?",
    re.IGNORECASE
)

def confidence(t):
    return {
        "EMAIL": 0.95, "PHONE": 0.95, "GOV_ID": 0.95,
        "DOB": 0.9, "APPT_ID": 0.9, "INSURANCE_ID": 0.9
    }.get(t, 0.8)

def detect(text):
    spans = []

    def add(m, t):
        spans.append({
            "type": t,
            "start": m.start(),
            "end": m.end(),
            "confidence": confidence(t)
        })

    for t, r in PATTERNS.items():
        for m in r.finditer(text):
            add(m, t)

    for m in NAME_RE.finditer(text):
        add(m, "NAME")
    for m in ADDRESS_RE.finditer(text):
        add(m, "ADDRESS")
    for m in PROVIDER_RE.finditer(text):
        add(m, "PROVIDER")

    return resolve(spans)

def resolve(spans):
    spans.sort(key=lambda s: (s["start"], -(s["end"] - s["start"])))
    out = []
    for s in spans:
        if not out or s["start"] >= out[-1]["end"]:
            out.append(s)
        elif (s["end"] - s["start"]) > (out[-1]["end"] - out[-1]["start"]):
            out[-1] = s
    return out

def scrub(text, spans):
    out, i = [], 0
    for s in spans:
        out.append(text[i:s["start"]])
        out.append(f"[{s['type']}]")
        i = s["end"]
    out.append(text[i:])
    return "".join(out)

def process(entry):
    spans = detect(entry["text"])
    return {
        "entry_id": entry["entry_id"],
        "scrubbed_text": scrub(entry["text"], spans),
        "detected_spans": spans,
        "types_found": sorted({s["type"] for s in spans}),
        "scrubber_version": SCRUBBER_VERSION
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--in", dest="inp", required=True)
    p.add_argument("--out", dest="out", required=True)
    args = p.parse_args()

    with open(args.inp) as fin, open(args.out, "w") as fout:
        for line in fin:
            fout.write(json.dumps(process(json.loads(line))) + "\n")

if __name__ == "__main__":
    main()
