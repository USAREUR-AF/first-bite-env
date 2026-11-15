# Documents

The interface documents the dictionaries of this repository transcribe. Both
are invented, with distribution unrestricted, and written as Markdown.

| Document | Revision | Dictionary |
|---|---|---|
| [`HB-ICD-001-A.md`](HB-ICD-001-A.md): Harbour Buoy to Shore Station | A | [`harbour-buoy`](../dictionaries/harbour-buoy/) |
| [`TG-ICD-002-B.md`](TG-ICD-002-B.md): Tide Gauge to Harbour Office | B | [`tide-gauge`](../dictionaries/tide-gauge/) |

`HB-ICD-001-A.md` is copied from `icd/` of
[USAREUR-AF/hello-galaxy-first-bite](https://github.com/USAREUR-AF/hello-galaxy-first-bite).
`TG-ICD-002-B.md` was written for this repository, with one deliberate
erratum (its ISSUE-001).

A private overlay has no `documents/` directory. The source document stays
where its owner keeps it, and `.gitignore` refuses the formats documents come
in (`*.pdf`, `*.docx`, `*.doc`). What the overlay holds is the transcription,
handled as the document is.
