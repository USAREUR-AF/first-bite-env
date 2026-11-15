## What changed

<!-- Dictionary, messages and fields touched, and the document, revision and section they come from; or the deployment and what it now does. -->

## Checks

- [ ] `make check` passes, with a `bite` of the commit in `first-bite.ref`.
- [ ] `make diff D=<dictionary> OLD=<last release>` output is pasted below, and the version in that dictionary's `dictionary.json` is raised by at least what it asks for.
- [ ] The dictionary's `CHANGELOG.md` has an entry for the new version.
- [ ] A changed deployment still behaves as its README says: `deployments/<site>/check.sh`.

## Transcription

- [ ] Every new or changed field was entered from the document, not from another dictionary or from a capture.
- [ ] Bit positions were entered as the document writes them (`word`, `bits`) and converted by `bite`, not by hand.
- [ ] Every new or changed message has `declared_bits` from the document's stated length.
- [ ] Every new or changed message has a vector whose expected values come from the document, and whose payload was checked without `bite`.
- [ ] Every erratum or ambiguity met is in the dictionary's `icd-notes/issues.md`, and the field carries a `note` naming the entry.
- [ ] Nothing was allowed in `lint.allow` without a reason a reviewer can check.

## Handling

- [ ] This change adds nothing whose handling is narrower than the README's Handling section states for this repository.
- [ ] No capture of real traffic, no payload taken from one, no credential value, no address or host name of a real system.

## Review (second reader)

- [ ] I read each changed field against the document myself: name, word and bits, type, scale and unit, every enumerated value.
- [ ] I recomputed one vector per changed message by hand.

```
<paste the output of make diff here>
```
