# Figures

`make-figures.py` draws the README's figure from this tree. It writes each
figure twice, `<name>-light.svg` and `<name>-dark.svg`, for a `<picture>`
element. The files stand alone: no external CSS, fonts or scripts. The visual
system is first-bite's `docs/img/build.py`: the same palette, fonts and label
measurement against `font-metrics.json`, which is a copy of first-bite's.
Standard library only.

```sh
python3 -I docs/figures/make-figures.py           # write the SVG files
python3 -I docs/figures/make-figures.py --check   # exit 1 if a committed file is out of date
```

| Figure | Shows | Read from |
|---|---|---|
| `overlay` | first-bite at a pinned commit, the overlay's dictionaries and site, the pull-request checks, and a private overlay made from this template | `first-bite.ref`; `FIRST_BITE_VERSION` in `.github/workflows/check.yml`; each `dictionaries/<name>/dictionary/` (name, version, source document, message files); `deployments/<site>/subscribers.yml` (security block); the workflow file names |

Regenerate after any of those change. The script stops if a label does not
fit its box or leaves the canvas. The figure was rendered as an `<img>` at
830 px and 400 px wide, in both themes, and inspected.
