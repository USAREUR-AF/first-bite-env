# Changelog

One entry per version of the dictionary, newest first. Each entry names the
document revision it transcribes and lists what `bite diff` reported against
the version before it, most severe first.

## 0.1.0

Transcribed from TG-ICD-002 revision B.

- Started: Water Level and Gauge Status, three vectors from appendix A.
- Calibration Record is named and not defined: it is defined in TG-CAL-003,
  which is not transcribed. `lint.allow` carries the `C004` finding with that
  reason.
- Water Level uses an LSB of 0.001 m, not the 0.01 m of Table 5-2
  (`icd-notes/issues.md` ISSUE-001).
