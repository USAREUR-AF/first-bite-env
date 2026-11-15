# Deployments

The configuration of first-bite deployments: one directory per site, holding
what is installed on its capture hosts under `/etc/first-bite/`.

| Site | Holds |
|---|---|
| [`example-harbour`](example-harbour/README.md) | an invented site: a `security:` block at level `tls`, Cursor-on-Target to a TAK server, every record to an S3-compatible archive over HTTPS |

A file here carries no secret value: a credential is named by where it is
kept (`${NAME}` from the service's environment file, or a `*_file` key that
reads a file systemd hands the service), never written out. Certificates and
keys are named by path.

## Adding a site

1. Copy `example-harbour/` to `deployments/<site>/` and change every value.
2. Keep `check.sh` working for the site: it is how a reviewer sees what the
   configuration does without the site's hosts.
3. Add a row to the table above and a line to `CODEOWNERS` naming who may
   approve a change to the site.
