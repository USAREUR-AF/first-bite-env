# Document issues

Every place the source document is wrong, contradicts itself or can be read
two ways, and what this dictionary does about it. An entry is added the moment
the issue is found, before anything is decided. The field or message it
concerns carries a `note` that names the entry.

| Status | Means |
|---|---|
| open | no decision; the dictionary follows the document as written |
| decided | the dictionary follows the decision recorded here |
| confirmed | the document's owner agreed, in the reference given |
| fixed in <revision> | a later revision of the document corrects it |

## ISSUE-001: Table 5-2 gives the Water Level LSB as 0.01 m; the document elsewhere says millimetres

| | |
|---|---|
| Status | decided |
| Where | TG-ICD-002 revision B, section 5.2, Table 5-2, word 3 |
| Affects | `TIDE/Water Level/water_level` |
| The document says | Table 5-2: "Water Level", LSB "0.01", unit "m". Section 3.2: "Water levels are carried in millimetres." |
| The problem | The two cannot both hold. 0.01 m is a centimetre. |
| Evidence | Appendix A.1 gives a water level of 1.234 m in the bytes `04d2`, which is 1234: an LSB of 0.001 m. Appendix A.2 gives -0.250 m in `ff06`, which is -250: the same. With 0.01 m the examples would read 12.34 m and -2.50 m. |
| Decision | The dictionary uses 0.001 m, which section 3.2 and both examples agree on. Decided by the transcriber and the second reader. |
| Reported to | the document's owner, the Harbour Office engineering desk, query HO-Q-0001 (invented) |

## ISSUE-002: "Datum Check Due" does not say whether an overdue check also sets the bit

| | |
|---|---|
| Status | open |
| Where | TG-ICD-002 revision B, section 5.3, Table 5-3, word 3 bit 14 |
| Affects | `TIDE/Gauge Status/datum_check_due` |
| The document says | "1 when the datum check is due." |
| The problem | A consumer cannot tell whether the bit stays set once the check is overdue, or clears. Decoding is not affected: the field is one bit either way. |
| Evidence | none; no example shows an overdue check |
| Decision | none; the dictionary follows the document as written, and the description is the document's |
| Reported to | the document's owner, query HO-Q-0002 (invented) |
