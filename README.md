
PII / Sensitive Identifier Scrubber (Exercise A)
Overview

The scrubber processes free-text journal entries and removes personally identifiable or linkable information while preserving all clinical and journaling meaning

Problem Statement

Women’s health journals often contain:
symptoms and cycle notes (which must be preserved)
personally identifying or linkable information (which must be removed)


Detection Approach

This solution uses regex-based detection combined with simple heuristics.
Direct Identifiers :
EMAIL – standard email patterns
PHONE – AU / US / IN formats (spaces, hyphens, parentheses tolerated)
NAME – heuristic detection for personal names (patients, clinicians, partners)
ADDRESS – street-style addresses with locality/postcode patterns
DATE_OF_BIRTH (DOB) – common date formats tied to DOB context

Health-System Identifiers

PROVIDER / CLINIC – known clinic-style phrases (e.g., “Fertility”, “IVF”, “Pathology”)
APPOINTMENT / BOOKING / REFERRAL ID – IDs like APPT-, BKG-, INV-
INSURANCE ID – policy-style identifiers
GOVERNMENT HEALTH ID – Medicare-like, SSN-like, Aadhaar-like patterns

What Is Explicitly NOT Scrubbed

To preserve health meaning, the scrubber does NOT remove:
symptoms (e.g., cramps, bloating, anxiety)
cycle information (period timing, day count)
medication names and dosages
vitals (BP, weight)
lifestyle metrics (steps, sleep)
generic numbers that are not identifiers


Overlap Handling

When multiple detections overlap:
the longest and most specific span wins
nested or duplicate replacements are avoided

Confidence Scoring

Each detected span includes a rule-based confidence score:
High confidence (e.g., EMAIL, PHONE): 0.9 – 0.95
Heuristic detections (e.g., NAME): ~0.8
Confidence scores reflect certainty of detection, not correctness of content.

Output Format

For each journal entry, the scrubber outputs:

{
  "entry_id": "j_001",
  "scrubbed_text": "...",
  "detected_spans": [
    {
      "type": "EMAIL",
      "start": 45,
      "end": 67,
      "confidence": 0.95
    }
  ],
  "types_found": ["EMAIL"],
  "scrubber_version": "v1"
}

Known Limitations

Name detection is heuristic-based and may miss uncommon formats
Clinic/provider detection relies on pattern matching rather than a full dictionary
This solution does not use ML or NER models by design


Future Improvements

With more time or tooling:
integrate a lightweight NER model for improved name detection
expand provider/clinic dictionaries
add language-aware heuristics
support configurable scrubbing policies per region



Created by Rishith

