# Records

An optional place for what the overlay's maintainers keep beside the
dictionaries and are handled as the overlay is.

| Path, in a private overlay | Holds |
|---|---|
| `records/decisions.md` | design decisions, each with the alternative |
| `records/leak-needles.txt` | the names public repositories must never contain: one per line, a plain line matched case-insensitively as a substring, a line starting `re:` an extended regular expression. [README: the leak check](../README.md#the-leak-check) says how it is used |
| `records/notes/` | working notes |

This example holds none of them: a needle list names what is private, so it
exists only in a private overlay.
