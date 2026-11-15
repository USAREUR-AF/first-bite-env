# example-harbour

The configuration of one first-bite capture host at an invented site,
`example-harbour`: it decodes the buoys' link with the
[`harbour-buoy`](../../dictionaries/harbour-buoy/) dictionary and sends
records off the host two ways, both over TLS. Every address, name and value
is an example.

| Output | Sink | Destination | Carries |
|---|---|---|---|
| `PositionsToTak` | `tcp` with a `tls` block and a `cot:` mapping | the TAK server's TLS streaming input, `203.0.113.40:8089` | one Cursor-on-Target event per `BUOY/Position` record |
| `RecordsToArchive` | `objectstorage` / `awsobject` over `https://` | an S3-compatible archive, `https://archive.harbour.example`, bucket `harbour-records` | every `BUOY` record as JSON |

Who reads the records is something the owner of the host grants. The ZeroMQ
socket stays on loopback, and these two sinks are the only paths off the host.

## Files

| File | Installed as | Holds |
|---|---|---|
| [`subscribers.yml`](subscribers.yml) | `/etc/first-bite/config/subscribers.yml` | the `security:` block and the two sinks |
| [`first-bite.env`](first-bite.env) | `/etc/first-bite/first-bite.env`, `0640 root:firstbite` | the template of the service's environment: interface, dictionary, the archive's access key id |
| [`first-bite.service.d/example-harbour.conf`](first-bite.service.d/example-harbour.conf) | `/etc/systemd/system/first-bite.service.d/example-harbour.conf` | a drop-in for first-bite's unit: `LoadCredential=` for the archive's secret key |
| [`check.sh`](check.sh) | not installed | runs this configuration with a `mind` on the current host, as below |

The unit itself, the `firstbite` user and the directories come from
first-bite's `deployment/install.sh`; [first-bite's
`docs/deployment.md`](https://github.com/USAREUR-AF/first-bite/blob/main/docs/deployment.md)
is the procedure.

## The security block

```yaml
security:
  transport: tls
  min_tls: "1.3"
  client_cert: /etc/first-bite/tls/client.pem
  client_key: /etc/first-bite/tls/client.key
  ca_bundle: /etc/first-bite/tls/ca.pem
```

`transport: tls`: every sink that leaves the host speaks TLS 1.3 to a server
whose certificate chains to a trusted authority and matches its name; an
`http://` endpoint or a plaintext `tcp` stream to another host is refused at
startup. The client certificate is named by path and presented to a server
that asks for one. The TAK stream uses the certificate and truststore the TAK
server's administrator issued, under `/etc/first-bite/tak/`. first-bite's
[`docs/security/transport.md`](https://github.com/USAREUR-AF/first-bite/blob/main/docs/security/transport.md)
explains the levels.

## Credentials

No credential value is in this directory.

| Credential | Written in `subscribers.yml` as | The value is in |
|---|---|---|
| archive access key id | `aws_access_key_id: "${HARBOUR_ARCHIVE_ACCESS_KEY_ID}"` | `/etc/first-bite/first-bite.env` |
| archive secret key | `aws_secret_access_key_file: "archive-secret-access-key"` | `/etc/first-bite/credentials/archive-secret-access-key`, handed to the service by `LoadCredential=` |
| client certificate and key | `client_cert`, `client_key` | `/etc/first-bite/tls/` |
| TAK client certificate and key | `tls.client_cert_file`, `tls.client_key_file` | `/etc/first-bite/tak/` |

## What running it does

`check.sh` runs three things with the `mind` on `PATH` (or `MIND=<path>`),
writing only to a temporary directory it removes. Measured with first-bite
1.1.0 (`mind` of the `x86_64-linux-gnu` release archive) on an x86-64 Ubuntu
host, and with the `aarch64-apple-darwin` archive on macOS: every expectation
passed on both.

**1. The files as written, on a host without `/etc/first-bite/`.**
`mind security check --env-file deployments/example-harbour/first-bite.env`,
with `SUBSCRIBER_CONFIG_PATH` naming `subscribers.yml`, exits 1:

```text
subscriber RecordsToArchive: `aws_secret_access_key_file`: cannot read archive-secret-access-key: No such file or directory (os error 2)
```

With the secret key file in place and the certificates still missing, it
exits 1 again:

```text
subscriber PositionsToTak: `tls.ca_file`: cannot read /etc/first-bite/tak/truststore.pem: I/O error: No such file or directory (os error 2)
subscriber RecordsToArchive: `security.ca_bundle`: cannot read /etc/first-bite/tls/ca.pem: I/O error: No such file or directory (os error 2)
```

**2. With throwaway certificates.** The script writes a throwaway authority
and client certificates, and a placeholder secret key, into its temporary
directory, and a copy of `subscribers.yml` with `/etc/first-bite/` pointing
there. `mind security check` exits 0:

```text
security check passed: level tls (/tmp/example-harbour.XXXXXX/subscribers.yml), 3 path(s)
```

and `mind security show` reports, for the two sinks:

```text
PositionsToTak  [tcp]
  endpoint         203.0.113.40:8089
  leaves the host  yes
  transport        mutual TLS
  minimum TLS      1.3
  client auth      certificate …/etc/first-bite/tak/first-bite.pem (presented when the server asks)
  server trust     bundle …/etc/first-bite/tak/truststore.pem

RecordsToArchive  [objectstorage/awsobject]
  endpoint         https://archive.harbour.example/
  leaves the host  yes
  transport        mutual TLS
  minimum TLS      1.3
  client auth      certificate …/etc/first-bite/tls/client.pem (presented when the server asks)
  server trust     bundle …/etc/first-bite/tls/ca.pem
```

**3. The example capture.**
`mind --pcap-file examples/harbour-buoy.pcap --dictionary dictionaries/harbour-buoy/dictionary --drain-seconds 5`
with that configuration decodes every frame. Nothing answers at the two
destinations, which are a documentation address and a reserved name, so no
record is delivered and `mind` exits 3:

```text
done: 9 frames, 9 records, 9 decoded, 0 not UDP or TCP, 0 malformed
sink PositionsToTak: 0 delivered, 0 failed, 3 abandoned
sink RecordsToArchive: 0 delivered, 0 failed, 9 abandoned (still inside a delivery when the time to drain ran out)
```

The archive's line depends on how the host's resolver answers for
`archive.harbour.example`: the Ubuntu host printed the line above; macOS
answered at once that the name does not exist, and printed
`0 delivered, 9 failed, 0 abandoned`. `check.sh` requires `0 delivered` on
both sinks and exit status 3.

## Status

| Part | Status |
|---|---|
| `subscribers.yml`, `first-bite.env`, the drop-in | built |
| `mind security check` and `security show` against them, `mind --pcap-file` with them | measured, as above |
| delivery to a TAK server and to an S3-compatible store | built in first-bite and measured there (`tools/security-selftest.sh`); here the destinations are examples and nothing is delivered |
