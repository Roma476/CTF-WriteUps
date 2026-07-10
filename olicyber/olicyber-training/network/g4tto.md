# G4tto

| | |
|---|---|
| **Section** | Network Security |
| **Category** | network |
| **Solves** | 2000 |

## Overview

The challenge provides a network capture:

```
G4tt0.pcapng
```

## Solve

Opening the capture in Wireshark and filtering for HTTP traffic reveals a request for an image:

```
GET /HttpEcho/Gatto.jpeg
```

The JPEG file can be extracted directly from the HTTP stream.

Inspecting the recovered image reveals a picture of a cat containing the flag.