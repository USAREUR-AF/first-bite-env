# Tables

The dictionary as four CSV files, for entry and review in a spreadsheet.
`make import` builds `dictionary/` from them; `make tables` writes them from
`dictionary/`. Both directions give the same bytes, so either may be edited:
commit both in the same change.

| File | One row per |
|---|---|
| `interfaces.csv` | interface |
| `messages.csv` | message, defined or only named |
| `fields.csv` | field |
| `values.csv` | enumerated value of a field |

Save as UTF-8 CSV. Do not let the spreadsheet reformat cells: enter `word`,
`bits`, `value` and `type_id` as text.
