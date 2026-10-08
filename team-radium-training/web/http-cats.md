# HTTP Cats [hard]

| | |
|---|---|
| **Section** | ITSOS CTF 2026 |
| **Category** | web |
| **Solves** | 1 (first blood) |

## Overview

The page always returns the same body: a base64 string that decodes to the list of numbers used by the server.

```
100,101,102,200,201,202,226,300,301,302,303,305,400,401,402,403,404,405,410,411,412,413,414,415,421,422,423,424,505,506,507,508,510,511
```

This list is just HTTP status codes. The attached PHP source shows that the body carries no information about the flag:

```php
if ($_SESSION['cnt'] < strlen($FLAG)) {
    http_response_code($bunchOfNumbers[ord(substr($FLAG, $_SESSION['cnt'], 1)) % count($bunchOfNumbers)]);
    echo base64_encode(implode(',', $bunchOfNumbers));
}
```

Each request increments a counter stored in the PHP session (`PHPSESSID`). The n-th request leaks the n-th character of the flag, encoded as the **HTTP status code** of the response: `codes[ord(c) % 34]`. The only channel is the status code, which is exactly what the Network tab of the dev tools shows. Once the counter passes the length of the flag, the response is a plain `200` with no body.

## Solve

The status code is a lossy encoding: it only reveals `ord(c) % 34`, so each code maps back to up to three printable candidates (`idx`, `idx + 34`, `idx + 68`, `idx + 102`). For lowercase letters (97-122) the 26 values of `ord(c) % 34` are all distinct, so the mapping is unambiguous as long as the content is lowercase. The decoded text also has to be readable, which gives a sanity check on every position.

Two details matter when writing the client:

- The counter lives in the session, so the client must keep the `PHPSESSID` cookie and start from a fresh session. A dropped or repeated request desyncs the counter.
- Informational codes (`100`, `101`, `102`) are special: in a raw socket client, those responses showed up without the usual body. A loop that stops at the first empty body ends too early (it stopped at 15 characters instead of the real length). The real end is the first `200` without a body, so the script treats `1xx` as a character and stops only after 3 consecutive empty responses.

```python
import socket, ssl, re

HOST, PATH = "cali.kt.ci", "/ctf/2026/03/web02/"
codes = [100,101,102,200,201,202,226,300,301,302,303,305,400,401,402,403,404,405,
         410,411,412,413,414,415,421,422,423,424,505,506,507,508,510,511]
ctx = ssl.create_default_context()

def req(cookie=None):
    s = ctx.wrap_socket(socket.create_connection((HOST, 443), timeout=5),
                        server_hostname=HOST)
    h = f"GET {PATH} HTTP/1.1\r\nHost: {HOST}\r\nConnection: close\r\n"
    if cookie:
        h += f"Cookie: {cookie}\r\n"
    s.sendall((h + "\r\n").encode())
    data = b""
    try:
        while chunk := s.recv(4096):
            data += chunk
    except (socket.timeout, ssl.SSLError):
        pass
    s.close()
    return data.decode(errors="ignore")

r = req()
cookie = re.search(r"PHPSESSID=[^;\s]+", r, re.I).group(0)

indices, empty, n = [], 0, 0
while empty < 3 and n < 120:
    if n > 0:
        r = req(cookie)
    lines = re.findall(r"^HTTP/1\.[01] (\d{3})", r, re.M)
    if not lines:
        raise SystemExit(f"timeout at request {n}, restart with a new session")
    status = int(lines[0])
    if "MTAw" in r or status in (100, 101, 102):
        indices.append(codes.index(status))
        empty = 0
    else:
        empty += 1
    n += 1

flag = ""
for idx in indices:
    flag += next(chr(c) for c in range(idx, 127, 34) if chr(c).islower())

print(f"flag{{{flag}}}")
```

Running the script prints the flag.