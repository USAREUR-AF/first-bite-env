# Dictionaries

One directory per dictionary. Each is a first-bite dictionary transcribed from
an interface document, with the tables it is entered in and the register of
the document's errata beside it. Both here are transcribed from invented
documents in [`documents/`](../documents/).

| Dictionary | Transcribes | Handling | Shows |
|---|---|---|---|
| [`harbour-buoy`](harbour-buoy/README.md) | HB-ICD-001 revision A: a harbour buoy to its shore station | distribution unrestricted; invented | a complete dictionary with no finding allowed |
| [`tide-gauge`](tide-gauge/README.md) | TG-ICD-002 revision B: a tide gauge to its harbour office | distribution unrestricted; invented | a coverage allowance with its reason, and an issues register |

## Layout of one dictionary

```text
dictionaries/<name>/
  README.md              what it transcribes, its marking, its status
  CHANGELOG.md           one entry per dictionary version
  dictionary/            what BITE_DICT_PATH points at
    dictionary.json
    <INTERFACE>/metadata.json
    <INTERFACE>/messages/<Message Name>.json
    vectors/<name>.json
  tables/                the four CSV files the dictionary is entered in
  icd-notes/issues.md    errata and ambiguities, and what was decided
```

## Adding a dictionary

1. Read the document's distribution statement. If it is narrower than this repository's access (the [README's Handling section](../README.md#handling)), the dictionary does not go here.
2. `bite new dictionaries/<name>/dictionary --interface <NAME>`, then follow first-bite's [`docs/icd-to-dictionary/`](https://github.com/USAREUR-AF/first-bite/tree/main/docs/icd-to-dictionary).
3. Add the document's statement, word for word, to the dictionary's README, a row to the table above, and a line to `CODEOWNERS` naming who holds the document.
4. `make check` covers the new dictionary without further change: it runs on every `dictionaries/*/dictionary/dictionary.json`.
