# tide-gauge dictionary

The first-bite dictionary for the TIDE interface of an invented tide gauge:
the document [`TG-ICD-002-B.md`](../../documents/TG-ICD-002-B.md) transcribed
into JSON that the `bite` decoder loads. It shows two things the harbour-buoy
dictionary does not: a message the document names and defines elsewhere,
allowed with a reason, and an issues register with one decided and one open
entry.

## Handling

The statement on the document, word for word:

> Revision B. Distribution unrestricted.

The document is invented, so this dictionary is public. In a private overlay
this section carries the distribution statement printed on the real document.

## What is here

| Interface | Source document | Messages the document names | Messages defined here | Fields |
|---|---|---|---|---|
| `TIDE` tide gauge to harbour office | TG-ICD-002 revision B | 3 | 2 | 13 |

`Calibration Record` (identifier 3) is named in Table 5-1 and defined in
TG-CAL-003, which is not transcribed. A record of it carries its message type
and no fields. The coverage gate would fail on it (`C004`, every message named
in `message_type` has a definition); `dictionary.json` allows that one finding
under `lint.allow`, with the reason.

## Status

| Part | Status |
|---|---|
| Water Level, Gauge Status | built: every field, unit, scale, description, source and declared length |
| Calibration Record | not built: defined in TG-CAL-003; allowed as `C004` |
| Water Level LSB | built as 0.001 m, against Table 5-2: [`icd-notes/issues.md`](icd-notes/issues.md) ISSUE-001, decided |
| Datum Check Due, overdue case | open: ISSUE-002; decoding does not depend on it |
| Test vectors | built: 3, from the document's appendix A; Water Level has one above and one below chart datum |
| `make check` | measured with `bite` 0.2.0 (first-bite 1.1.0): `fmt --check` 7 files canonical; `check --strict` 0 errors, 0 warnings, 1 allowed, 3 of 3 vectors passed; `lint` 0 findings; `coverage --strict` 0 failing, 1 allowed |
| Tables (`tables/*.csv`) | built by `bite export-csv`; `bite import-csv` rebuilds the same dictionary from them |

## Layout

| Path | Holds |
|---|---|
| `dictionary/` | the dictionary: `dictionary.json` (with `lint.allow`), `TIDE/`, `vectors/` |
| `tables/` | the spreadsheet form the dictionary is entered in: four CSV files |
| `icd-notes/issues.md` | ISSUE-001 and ISSUE-002 |
| `CHANGELOG.md` | one entry per dictionary version |

## Using it with first-bite

```bash
BITE_DICT_PATH=/path/to/first-bite-env/dictionaries/tide-gauge/dictionary
bite decode --interface TIDE /path/to/first-bite-env/dictionaries/tide-gauge/dictionary 0104032a04d24000
```

A Calibration Record decodes to its message type and no fields:

```bash
bite decode --port 47300 dictionaries/tide-gauge/dictionary 0303032d
```

```json
{
  "fields": {},
  "interface": "TIDE",
  "message_type": "Calibration Record"
}
```
