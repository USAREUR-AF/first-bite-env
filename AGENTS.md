# AGENTS.md

Instructions for AI coding agents, and a short version for anyone working here. [CONTRIBUTING.md](CONTRIBUTING.md) is the full process.

## What this repository is

first-bite-env is the example first-bite overlay, written down: two dictionaries transcribed from invented interface documents and the configuration of one invented site, over [first-bite](https://github.com/USAREUR-AF/first-bite) at the commit in `first-bite.ref`. It is a template: a private overlay is made from it. Copy its shape; never put a real document, dictionary or deployment's values here.

## Layout

| Path | What |
|---|---|
| `first-bite.ref` | the first-bite commit; move it in its own pull request, with the release in `.github/workflows/check.yml` |
| `dictionaries/<name>/` | `dictionary/`, `tables/`, `icd-notes/issues.md`, `README.md`, `CHANGELOG.md` |
| `deployments/<site>/` | `subscribers.yml`, `first-bite.env`, the systemd drop-in, `check.sh` |
| `documents/`, `examples/` | the invented documents and a capture built from vectors |

## Rules CI enforces

1. **Nothing real.** No interface, message or field of a real document; no hostname, domain, address, account, key or person of a real deployment. Use documentation addresses (RFC 5737), names under `.example`, and `example.org` mail. The leak gate checks every pull request against a private list of names. It never prints what matched, so a red leak gate means: rename the identifier.
2. **Commits.** Conventional Commits subject of 100 characters or fewer, with a scope. Every commit is signed off (`git commit -s`) and signed. One logical change per pull request.
3. **READMEs move with the change**, with the status words built, measured, designed and not built exactly.

## Before you push

```bash
make check
deployments/example-harbour/check.sh
make leak-check
actionlint && yamllint --strict . && git ls-files -z '*.sh' | xargs -0 shellcheck
```
