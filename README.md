<h1 align="center">first-bite-env</h1>

<p align="center">
  An example first-bite overlay, kept separate from the software it runs. A template repository.
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg" alt="License: Apache 2.0"></a>
</p>

This is what a first-bite overlay looks like when it is written down: a repository that uses [`first-bite`](https://github.com/USAREUR-AF/first-bite) by pinned commit and holds what a deployment owns: its dictionaries and its configuration. A real deployment is first-bite at a pinned commit plus a private overlay with that deployment's dictionaries and configuration; this repository has the same shape, and every document, dictionary, address and name in it is invented.

| Example | Where | What it is |
|---|---|---|
| `harbour-buoy` | [`dictionaries/harbour-buoy/`](dictionaries/harbour-buoy/) | a complete dictionary of an invented buoy's interface, with no finding allowed |
| `tide-gauge` | [`dictionaries/tide-gauge/`](dictionaries/tide-gauge/) | a dictionary with a message allowed as defined elsewhere, and an issues register |
| `example-harbour` | [`deployments/example-harbour/`](deployments/example-harbour/) | one site's capture host: a `security:` block at level `tls`, Cursor-on-Target to a TAK server, records to an archive over HTTPS |

Make your own from it: [Make your own](#make-your-own).

## Where things are

| You want | It is in | Visibility |
|---|---|---|
| The decoder (`bite`), the capture and publish process (`mind`), the dictionary format, the method from an interface document to a dictionary, releases | [`USAREUR-AF/first-bite`](https://github.com/USAREUR-AF/first-bite) | public |
| The example overlay: synthetic dictionaries, one deployment, the gates, the template to make a private overlay from | [`USAREUR-AF/first-bite-env`](https://github.com/USAREUR-AF/first-bite-env), this repository | public |
| A worked first-bite example to follow step by step: decode a capture, tap a link, write a dictionary, publish to a goat fabric, make Cursor-on-Target | [`USAREUR-AF/hello-galaxy-first-bite`](https://github.com/USAREUR-AF/hello-galaxy-first-bite) | public |
| Worked examples of consuming first-bite's records | [`USAREUR-AF/hello-galaxy-record-consumers`](https://github.com/USAREUR-AF/hello-galaxy-record-consumers) | public |
| The parallel for goat: the software, and its example environment kept as an overlay the same way | [`USAREUR-AF/goatcore`](https://github.com/USAREUR-AF/goatcore) and [`USAREUR-AF/goatenv`](https://github.com/USAREUR-AF/goatenv) | public |

## What an overlay owns

| Path | Holds |
|---|---|
| `first-bite.ref` | the full commit of `USAREUR-AF/first-bite` whose `bite` checks these dictionaries and whose `mind` runs these deployments: `d65b0389013ca36e14d27b5e802d16e9390f7f5f`, release `v1.1.0` |
| `dictionaries/<name>/` | one dictionary: `dictionary/` (what `BITE_DICT_PATH` points at), `tables/` (the four CSV files it is entered in), `icd-notes/issues.md` (the document's errata and what was decided), `README.md` (the document's distribution statement first, then status), `CHANGELOG.md` |
| `deployments/<site>/` | one site: the subscriber file with its `security:` block, the environment file template, the systemd drop-in, and `check.sh`, which runs them with a `mind` |
| `briefs/`, `records/` | optional: papers about the deployment, design decisions, the leak check's name list. Empty here |
| `documents/` | here only: the two invented interface documents. A private overlay holds no document |
| `examples/` | here only: a capture built from the harbour-buoy vectors |
| `Makefile` | `make check`, the gates every pull request passes, over every dictionary |
| `.github/workflows/` | `first-bite-ref`, `check`, `lint`, `leak-gate`, `contributor-trust` |
| `.github/pull_request_template.md` | the review checklist: transcription, handling, second reader |
| `CODEOWNERS` | who must review: in a private overlay, one line per dictionary naming the people who hold its document |

The software is not here. `bite` and `mind` come from first-bite at the pinned commit, built by `make bite` or installed from that commit's release archive.

## Using it

```bash
make bite                               # build bite from first-bite at first-bite.ref, into .first-bite/ (needs cargo)
make check                              # fmt --check, check --strict, lint, coverage --strict on every dictionary
make tables D=tide-gauge                # dictionary -> tables, to edit in a spreadsheet
make import D=tide-gauge                # tables -> dictionary
make diff D=tide-gauge OLD=<released copy>   # what changed, and whether the version covers it
deployments/example-harbour/check.sh    # the deployment, run with the mind on PATH
make leak-check                         # first-bite's tools/check-public-tree.sh over this tree
```

`make check` uses `.first-bite/target/release/bite` when `make bite` has built it and `bite` on `PATH` otherwise; `BITE=<path>` names another. Instead of building, install the release archive of the pinned commit: download `first-bite-1.1.0-<platform>.tar.gz` and `SHA256SUMS` from [release v1.1.0](https://github.com/USAREUR-AF/first-bite/releases/tag/v1.1.0), check it with `sha256sum --check SHA256SUMS --ignore-missing`, and put the directory holding `bite` and `mind` on `PATH` (`deployment/` in the Linux archives, `bin/` in the macOS ones). The checks read a directory and send nothing anywhere.

To use a dictionary, point the decoder at it; nothing is copied into first-bite:

```bash
BITE_DICT_PATH=/path/to/first-bite-env/dictionaries/harbour-buoy/dictionary
```

## Make your own

### Create the private repository

On GitHub, **Use this template** → **Create a new repository**, with visibility **Private**, in the organisation whose members may hold your documents. Then, in the new repository:

1. Delete `documents/` and `examples/`, `dictionaries/harbour-buoy/`, `dictionaries/tide-gauge/` and `deployments/example-harbour/`, or keep them until your own are in and delete them then.
2. Rewrite this README's first section to say what the repository holds, and its [Handling](#handling) section to carry the distribution statement of each document, word for word.
3. Set `CODEOWNERS`: one line per dictionary naming the people who hold its document and can check a transcription against it.
4. Add a dictionary as [`dictionaries/README.md`](dictionaries/README.md) says, and a site as [`deployments/README.md`](deployments/README.md) says.

### Who may read it

Handling follows the source documents. A dictionary transcribes its document and inherits that document's distribution: so do its tables, its issues register, its vectors and the output of every check, because each restates the document. The repository's access list is the list of people who may hold the document.

- GitHub grants read access per repository, not per branch. Whoever can read the repository can read every branch, so the repository is handled under the narrowest statement of any document on any branch.
- An organisation's base permission gives every member that access to every repository. If the base permission is read, the organisation's membership is the access list; otherwise access is what the teams and outside collaborators added to the repository give.
- Add no one who is not entitled to every document transcribed in the repository. A dictionary whose document is narrower than the access list goes in a repository of its own.
- Nothing from the repository is copied to a repository, a chat, an issue tracker or an online service with wider access: not a table, not an issues entry, not the output of a check. Transcription runs on your machine; first-bite's [`docs/icd-to-dictionary/02-conventions.md`](https://github.com/USAREUR-AF/first-bite/blob/main/docs/icd-to-dictionary/02-conventions.md#handling) has the rules.

### What never goes in a public repository

| Never public | Where it is kept instead |
|---|---|
| a restricted interface document, or anything transcribed from it: the dictionary, the tables, the issues register, the vectors, the output of the checks | the private overlay, handled as the document is |
| the names of a restricted message set: interfaces, messages, fields, enumerated values | the same |
| a capture of real traffic, or a payload taken from one | where the system it was taken from is handled; not in any repository |
| the addresses, host names, accounts and people of a real deployment | the private overlay's `deployments/` |
| a credential value | the host's environment file or credential files; the repository holds only `${NAME}` and `*_file` references |
| the leak check's name list | the private overlay's `records/leak-needles.txt`, and the public repositories' `LEAK_NEEDLES` secret |

### Moving the pin

Public code arrives only by moving the pin. A change to `bite` or `mind` is a pull request on `USAREUR-AF/first-bite`; once merged there:

1. In a pull request of its own, write the full 40-character sha of a commit on first-bite `main` into `first-bite.ref`. The `first-bite-ref` workflow refuses any other commit.
2. In `.github/workflows/check.yml`, set `FIRST_BITE_VERSION` to the release of that commit and `FIRST_BITE_SHA256` to the `x86_64-linux-gnu` archive's line in that release's `SHA256SUMS`. The workflow's first step refuses a release that is not of the pinned commit.
3. Run `make check` and each `deployments/<site>/check.sh` with the new `bite` and `mind`. A newer `bite` can report findings an older one did not; fix or allow them in the same pull request.

A commit with no release can be pinned too. `check.yml` then refuses it at its first step; replace its install step with `make bite`, which needs a Rust toolchain on the runner.

### CI

| Workflow | Runs | In your private copy |
|---|---|---|
| `first-bite-ref` | on every pull request: `first-bite.ref` is a full sha on first-bite `main` | keep; make it a required check |
| `check` | on every pull request: installs the pinned release after checking its SHA-256 and that it is of the pinned commit, then `make check` and `deployments/example-harbour/check.sh` | keep; change the last step to run each of your sites' `check.sh`; make it a required check |
| `lint` | `actionlint`, `yamllint --strict .`, `shellcheck` on every `*.sh` | keep |
| `leak-gate` | first-bite's `tools/check-public-tree.sh` at the pinned commit over the pull request, with the `LEAK_NEEDLES` secret | delete: the private tree holds the very names the check refuses |
| `contributor-trust` | goatcore's check of who opened the pull request and whether it touches `.github/contributor-trust/sensitive-paths.txt`; needs the variable `CONTRIBUTOR_ROSTER_REPO` and the secret `CONTRIBUTOR_ROSTER_TOKEN` | keep if your organisation uses goatcore's contributor roster; otherwise delete |

Actions are pinned by commit sha, and every downloaded tool by version and SHA-256. Branch protection on `main`: a pull request, one approving review from a code owner, signed commits, and the required checks above.

### The leak check

[first-bite's `tools/check-public-tree.sh`](https://github.com/USAREUR-AF/first-bite/blob/main/tools/check-public-tree.sh) refuses, in a public tree: credential shapes, capture files outside `examples/`, private addresses and other identifiers by shape, and every name on a list. A hit prints the file, the line and a 12-character id of the name, never the name. The list is what keeps a restricted dictionary or a real deployment from entering a public repository by mistake, so it lives with what it protects:

1. Keep it in the private overlay as `records/leak-needles.txt`: the names of your restricted message sets and your deployments' hosts, places and accounts, one per line. A plain line matches case-insensitively as a substring; a line starting `re:` is an extended regular expression.
2. Before pushing to a public repository, run the check in its checkout with the list, on your own machine only:

   ```bash
   LEAK_NEEDLES="$(cat ../<your-overlay>/records/leak-needles.txt)" make leak-check            # in this repository
   LEAK_NEEDLES="$(cat ../<your-overlay>/records/leak-needles.txt)" tools/check-public-tree.sh # in first-bite
   ```

   Or copy the list to `.leak-needles` at the top of the public checkout (`.gitignore` refuses that name here) and delete it after.
3. In CI, set the list as the public repository's encrypted secret `LEAK_NEEDLES`; `leak-gate.yml` reads it. Without the secret the name check is skipped and the log says so; the other checks still run.

The list never goes in a public repository, and never on a machine shared with people who may not hold it, such as a common build host.

## Handling

Every document in this repository is invented, and each states its distribution: **Distribution unrestricted.** The dictionaries, tables, issues registers and the output of the checks are public for that reason.

In a private copy this section is where the handling of the whole repository is stated: the narrowest statement among its documents first, in bold, then each document's statement word for word under the name of its dictionary, then who can read the repository and why that matches.

## How it relates to first-bite's dictionary template

first-bite's [`tools/dictionary-repo-template`](https://github.com/USAREUR-AF/first-bite/tree/main/tools/dictionary-repo-template), made by `bite new <dir> --repo`, is one dictionary in one repository. This overlay builds on it:

| | Dictionary template | This overlay |
|---|---|---|
| Dictionaries | one, at `dictionary/` | any number, at `dictionaries/<name>/dictionary/` |
| Per dictionary | `tables/`, `icd-notes/issues.md`, `CHANGELOG.md`, `README.md` with the handling statement | the same, under `dictionaries/<name>/` |
| `make check` | the four gates on `dictionary/` | the same four gates on every dictionary |
| Which first-bite | `bite` on `PATH`; `check.yml` has placeholders for the release | `first-bite.ref` pins a commit, `make bite` builds it, `first-bite-ref.yml` refuses a commit not on `main`, `check.yml` installs its release and checks it is of that commit |
| Deployments | none | `deployments/<site>/` with a `check.sh` |
| Pull-request checklist | transcription and second reader | the same, plus handling and the deployment check |

## Status

| Part | Status |
|---|---|
| `make check` over both dictionaries, `bite` 0.2.0 of release 1.1.0 | measured: 0 failing on each; results in each dictionary's README |
| `deployments/example-harbour/check.sh` | measured with `mind` 1.1.0: every expectation passed, on x86-64 Ubuntu and on macOS |
| leak check | measured: first-bite's `tools/check-public-tree.sh` at the pinned commit passes over this tree, with the full name list, 68 files; the `make leak-check` target is built and not run |
| `actionlint`, `yamllint --strict .`, `shellcheck` | measured: clean |
| `first-bite-ref`, `check`, `lint`, `leak-gate`, `contributor-trust` workflows | built; they run once the repository is on GitHub |

## Licence

`first-bite-env` was written by U.S. Federal government employees. In the U.S. it is not subject to copyright and is in the public domain; in countries where copyright is recognized, it is released under the [Apache License 2.0](LICENSE). See [INTENT.md](INTENT.md). [CONTRIBUTING.md](CONTRIBUTING.md) · [SECURITY.md](SECURITY.md).
