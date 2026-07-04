# Bautiful Content
| | |
|---|---|
| **Section** | HighSchools CTF Workshop - 2023 Perugia |
| **Category** | network |
| **Solves** | 213 |

## Overview
The provided PCAP contains two relevant TCP/HTTP conversations against an Apache/PHP server:
- a `POST /index.php` with a `multipart/form-data` body uploading a file named `dear_ted.jpeg` (field `fileToUpload`)
- a subsequent `GET /uploads/dear_ted.jpeg`, whose response contains the actual JPEG image data

No other protocols in the capture carry relevant data (only DHCP/mDNS noise).

## Solve
In Wireshark, using **File > Export Objects > HTTP** lists both HTTP objects, including `dear_ted.jpeg`. Selecting it and clicking **Preview** reconstructs the image directly from the TCP stream, revealing the flag overlaid as text on the picture.