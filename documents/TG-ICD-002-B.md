# TG-ICD-002: Tide Gauge to Harbour Office Interface Control Document

Revision B. Distribution unrestricted.

This document is invented for the first-bite-env example. The tide gauge, the
harbour office and every value in it are synthetic. It has one deliberate
error, in Table 5-2, so that the dictionary transcribed from it shows how an
erratum is recorded.

## 1. Scope

This document defines the messages a tide gauge sends to the harbour office.
The harbour office sends nothing to the gauge on this interface.

## 2. Transport

Each message is one UDP datagram sent by the gauge to port 47300 of the
harbour office. The interface is named TIDE.

## 3. Conventions

### 3.1 Words and bits

A message is a whole number of 16-bit words. Words are numbered from 1 and are
sent most significant byte first. The bits of a word are numbered 15 to 0, and
bit 15 is the most significant.

### 3.2 Numbers

Fields are unsigned integers unless a table says "two's complement". A field
with an LSB weight carries the physical value divided by that weight. Water
levels are carried in millimetres. Spare bits are sent as zero.

## 4. Common header

Every message starts with the two words of Table 4-1.

Table 4-1: Common header

| Word | Bits | Field | Unit | Description |
|---|---|---|---|---|
| 1 | 15-8 | Message ID | | Identifies the message. See Table 5-1. |
| 1 | 7-0 | Message Length | words | Length of the message in 16-bit words. |
| 2 | 15-8 | Gauge Number | | Gauge that sent the message, 1 to 200. |
| 2 | 7-0 | Sequence Number | | Incremented by the gauge for each message; wraps from 255 to 0. |

## 5. Messages

Table 5-1: Messages of the TIDE interface

| Message ID | Message | Length (words) | Sent |
|---|---|---|---|
| 1 | Water Level | 4 | every six minutes |
| 2 | Gauge Status | 3 | every hour, and at once when a fault is raised |
| 3 | Calibration Record | 12 | after each calibration; defined in TG-CAL-003 |

### 5.2 Water Level

Sent every six minutes with the mean water level of the last three minutes.

Table 5-2: Water Level

| Word | Bits | Field | LSB | Unit | Description |
|---|---|---|---|---|---|
| 1-2 | | Common header | | | Table 4-1. |
| 3 | 15-0 | Water Level | 0.01 | m | Two's complement. Height of the water above chart datum. |
| 4 | 15-14 | Quality | | | How far the measurement can be trusted. See Table 5-2a. |
| 4 | 13-0 | Spare | | | |

Table 5-2a: Quality

| Value | Meaning |
|---|---|
| 0 | Good |
| 1 | Suspect |
| 2 | Failed |
| 3 | reserved |

### 5.3 Gauge Status

Sent every hour, and at once when a fault is raised.

Table 5-3: Gauge Status

| Word | Bits | Field | LSB | Unit | Description |
|---|---|---|---|---|---|
| 1-2 | | Common header | | | Table 4-1. |
| 3 | 15 | Pump Fault | | | 1 when the stilling-well pump has failed. |
| 3 | 14 | Datum Check Due | | | 1 when the datum check is due. |
| 3 | 13-8 | Spare | | | |
| 3 | 7-0 | Supply Voltage | 0.1 | V | Voltage of the gauge's supply. |

### 5.4 Calibration Record

Defined in TG-CAL-003, the gauge's calibration procedure.

## Appendix A. Example messages

Each example gives the values and the bytes of one message, most significant
byte of word 1 first.

### A.1 Water Level

Gauge 3, sequence number 42. Water level 1.234 m above chart datum, quality
Suspect.

```text
0104 032a 04d2 4000
```

### A.2 Water Level, below datum

Gauge 3, sequence number 43. Water level 0.250 m below chart datum, quality
Good.

```text
0104 032b ff06 0000
```

### A.3 Gauge Status

Gauge 3, sequence number 44. No pump fault, datum check due, supply 12.6 V.

```text
0203 032c 407e
```
