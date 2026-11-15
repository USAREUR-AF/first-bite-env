# Security policy

first-bite-env is the public example of a first-bite overlay: synthetic dictionaries and the configuration of one invented deployment. Security reports are prioritised over feature work.

## Reporting a vulnerability

**Do not open a public issue or pull request to report a vulnerability.**

**[Report a vulnerability privately](https://github.com/USAREUR-AF/first-bite-env/security/advisories/new)**

You can also open the reporting form from this repository's *Security* tab by selecting *Report a vulnerability*.

Reports are private and accessible to repository administrators, organization owners, security managers, the reporter, and collaborators explicitly added to the advisory. Being listed in `CODEOWNERS` does not itself grant access. Reports remain private until an authorized maintainer publishes the advisory. See [GitHub's advisory permissions](https://docs.github.com/en/code-security/reference/permissions/repository-security-advisory) for details.

Include: a description of the issue and its impact; reproduction steps or a proof of concept; the affected commits or files; whether you have shared it elsewhere.

## What to expect

| Step | Target |
|---|---|
| Acknowledgement | 3 working days |
| Triage and severity | 7 working days |
| Fix or mitigation for a confirmed high or critical issue | 30 days, with a coordinated disclosure date agreed with you |
| Public advisory | when the fix is merged, crediting you unless you prefer otherwise |

## Scope

In scope: the files in this repository, in particular the deployment example under `deployments/`, the workflows under `.github/` and the `Makefile`. Out of scope: first-bite itself (report to [USAREUR-AF/first-bite](https://github.com/USAREUR-AF/first-bite/security/advisories/new)); upstream projects; any deployment you do not own.

Do not attach a dictionary, an interface document or a capture that you are not permitted to share.

## Supported versions

The head of `main` is supported. Fixes land on `main`.
