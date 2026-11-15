#!/usr/bin/env bash
# Run the example-harbour configuration with this host's mind, the way
# README.md says it behaves:
#
#   deployments/example-harbour/check.sh                 mind from PATH
#   MIND=/path/to/mind deployments/example-harbour/check.sh
#
# 1. `mind security check` on the files as written, on a host without
#    /etc/first-bite/: refused, first for the archive's secret key file, then,
#    with that in place, for the first certificate (skipped on a host that has
#    /etc/first-bite/).
# 2. The same files with /etc/first-bite/ moved to a temporary directory that
#    holds throwaway certificates and a placeholder credential:
#    `mind security check` passes and `mind security show` prints each path.
# 3. `mind --pcap-file examples/harbour-buoy.pcap` with that configuration: 9
#    frames decoded; the TAK server and the archive are documentation
#    addresses nothing answers on, so no record is delivered and mind exits 3.
#
# Nothing is installed and nothing outside the temporary directory is written.
# Needs bash, openssl and a mind of the release first-bite.ref names.
set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
root="$(cd "$here/../.." && pwd)"
mind="${MIND:-mind}"
work="$(mktemp -d "${TMPDIR:-/tmp}/example-harbour.XXXXXX")"
work="$(cd "$work" && pwd -P)"
trap 'rm -rf "$work"' EXIT

fail=0
pass() { printf 'ok    %s\n' "$1"; }
miss() { printf 'FAIL  %s\n' "$1"; fail=1; }
# expect <description> <file> <fixed text>
expect() {
  if grep -qF -- "$3" "$2"; then pass "$1"; else miss "$1: no line with: $3"; sed 's/^/      /' "$2"; fi
}

"$mind" --version

# The placeholder the archive's access key id reference resolves to here.
export HARBOUR_ARCHIVE_ACCESS_KEY_ID=placeholder-access-key-id

echo "== 1. the files as written, on a host without /etc/first-bite/"
# refused <step> <fixed text>: security check exits non-zero, naming <text>.
refused() {
  local status=0
  "$mind" security check --env-file "$here/first-bite.env" >"$work/$1.out" 2>&1 || status=$?
  sed 's/^/      /' "$work/$1.out"
  if [ "$status" -ne 0 ]; then pass "security check refuses (exit $status)"; else miss "security check passed"; fi
  expect "the refusal names $2" "$work/$1.out" "$2"
}
if [ -e /etc/first-bite ]; then
  echo "skip  this host has /etc/first-bite"
else
  export SUBSCRIBER_CONFIG_PATH="$here/subscribers.yml"
  refused 1a "cannot read archive-secret-access-key"
  # The credential in place, the certificates still missing.
  mkdir -p "$work/credentials"
  printf 'placeholder-secret-access-key\n' >"$work/credentials/archive-secret-access-key"
  CREDENTIALS_DIRECTORY="$work/credentials" refused 1b "cannot read /etc/first-bite/tak/truststore.pem"
fi

echo "== 2. with throwaway certificates in place of /etc/first-bite/"
etc="$work/etc/first-bite"
mkdir -p "$etc/tls" "$etc/tak" "$etc/credentials"
certificate() { # certificate <directory> <ca file> <certificate file> <key file>
  openssl req -x509 -newkey ec -pkeyopt ec_paramgen_curve:P-256 -nodes -days 1 \
    -subj "/CN=throwaway authority" -keyout "$1/ca.key" -out "$1/$2" 2>/dev/null
  openssl req -newkey ec -pkeyopt ec_paramgen_curve:P-256 -nodes \
    -subj "/CN=first-bite example-harbour" -keyout "$1/$4" -out "$1/request.csr" 2>/dev/null
  # An extension file makes a version 3 certificate on every OpenSSL; without one,
  # OpenSSL 3.0 (Ubuntu 22.04 and 24.04) makes version 1, which TLS libraries refuse.
  printf 'basicConstraints=CA:FALSE\nkeyUsage=digitalSignature\nextendedKeyUsage=clientAuth\n' >"$1/extensions.cnf"
  openssl x509 -req -days 1 -in "$1/request.csr" -CA "$1/$2" -CAkey "$1/ca.key" \
    -CAcreateserial -extfile "$1/extensions.cnf" -out "$1/$3" 2>/dev/null
}
certificate "$etc/tls" ca.pem client.pem client.key
certificate "$etc/tak" truststore.pem first-bite.pem first-bite.key
printf 'placeholder-secret-access-key\n' >"$etc/credentials/archive-secret-access-key"
sed "s#/etc/first-bite/#$etc/#g" "$here/subscribers.yml" >"$work/subscribers.yml"

export SUBSCRIBER_CONFIG_PATH="$work/subscribers.yml"
export CREDENTIALS_DIRECTORY="$etc/credentials"

"$mind" security check --env-file "$here/first-bite.env" >"$work/2.out" 2>&1 || true
sed 's/^/      /' "$work/2.out"
expect "security check passes" "$work/2.out" "security check passed: level tls"
expect "three paths: the publisher and two sinks" "$work/2.out" "3 path(s)"

"$mind" security show --env-file "$here/first-bite.env" >"$work/show.out" 2>&1 || true
sed 's/^/      /' "$work/show.out"
expect "the TAK stream leaves the host over mutual TLS" "$work/show.out" "transport        mutual TLS"
expect "the archive leaves the host over TLS" "$work/show.out" "https://archive.harbour.example/"
expect "minimum TLS is 1.3" "$work/show.out" "minimum TLS        1.3"

echo "== 3. the example capture"
set +e
(cd "$work" && NO_COLOR=1 RUST_LOG=info "$mind" --env-file "$here/first-bite.env" \
  --dictionary "$root/dictionaries/harbour-buoy/dictionary" \
  --pcap-file "$root/examples/harbour-buoy.pcap" --drain-seconds 5) >"$work/3.out" 2>&1
status=$?
set -e
grep -E 'done: |sink [A-Za-z]+: ' "$work/3.out" | sed 's/^.*--- /      /'
expect "every frame decoded" "$work/3.out" "done: 9 frames, 9 records, 9 decoded, 0 not UDP or TCP, 0 malformed"
expect "the TAK server got nothing" "$work/3.out" "sink PositionsToTak: 0 delivered"
expect "the archive got nothing" "$work/3.out" "sink RecordsToArchive: 0 delivered"
if [ "$status" -eq 3 ]; then
  pass "mind exits 3: records not delivered within --drain-seconds"
else
  miss "mind exited $status, expected 3"
fi

if [ "$fail" -ne 0 ]; then
  echo "example-harbour: FAILED" >&2
  exit 1
fi
echo "example-harbour: ok"
