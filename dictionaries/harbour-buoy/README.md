# harbour-buoy dictionary

The first-bite dictionary for the BUOY interface of an invented harbour buoy:
the document [`HB-ICD-001-A.md`](../../documents/HB-ICD-001-A.md) transcribed
into JSON that the `bite` decoder loads.

## Handling

The statement on the document, word for word:

> Revision A. Distribution unrestricted.

The document is invented, so this dictionary is public. In a private overlay
this section carries the distribution statement printed on the real document,
and every file under the dictionary's directory is handled as that document
is: the dictionary, the tables, the issues register and the output of the
checks.

## What is here

| Interface | Source document | Messages the document names | Messages defined here | Fields |
|---|---|---|---|---|
| `BUOY` harbour buoy to shore station | HB-ICD-001 revision A | 3 | 3 | 30 |

## Status

| Part | Status |
|---|---|
| Fields, units, scales, descriptions, sources, declared lengths | built: every field of the document |
| Test vectors | built: 3, one per message, each an example of the document's appendix A |
| `make check` | measured with `bite` 0.2.0 (first-bite 1.1.0): `fmt --check` 8 files canonical; `check --strict` 0 errors, 0 warnings, 3 of 3 vectors passed; `lint` 0 findings; `coverage --strict` 0 failing, 0 allowed |
| Tables (`tables/*.csv`) | built by `bite export-csv`; `bite import-csv` rebuilds the same dictionary from them |
| Example capture | [`examples/harbour-buoy.pcap`](../../examples/harbour-buoy.pcap): the three vectors three times, 9 frames |

## Layout

| Path | Holds |
|---|---|
| `dictionary/` | the dictionary: `dictionary.json`, `BUOY/`, `vectors/` |
| `tables/` | the spreadsheet form the dictionary is entered in: four CSV files |
| `icd-notes/issues.md` | the errata and ambiguities of the document; none found |
| `CHANGELOG.md` | one entry per dictionary version |

## Using it with first-bite

Point the decoder at the dictionary directory; nothing is copied into first-bite.

```bash
BITE_DICT_PATH=/path/to/first-bite-env/dictionaries/harbour-buoy/dictionary
bite list /path/to/first-bite-env/dictionaries/harbour-buoy/dictionary
mind --pcap-file examples/harbour-buoy.pcap --dictionary dictionaries/harbour-buoy/dictionary
```

An interface is selected by UDP port: a packet whose source or destination
port is 47200 is decoded as `BUOY`.
