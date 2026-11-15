# Examples

Captures built from a dictionary's vectors, not taken from any network.

| File | Frames | Built from |
|---|---|---|
| `harbour-buoy.pcap` | 9: Position, Sea State, Status, three times | `dictionaries/harbour-buoy/dictionary/vectors/` |

Each frame is Ethernet, IPv4 and UDP from 192.0.2.10:47200 to
192.0.2.20:50000, one second apart, written by first-bite's
`tools/make-example-pcap.py` at the commit in `first-bite.ref`:

```bash
make first-bite
python3 .first-bite/tools/make-example-pcap.py dictionaries/harbour-buoy/dictionary examples/harbour-buoy.pcap --repeat 3
```

first-bite's `tools/check-public-tree.sh` refuses a capture file anywhere but
`examples/`. A private overlay keeps captures of real traffic out of the
repository altogether: a capture is handled as the system it was taken from.
