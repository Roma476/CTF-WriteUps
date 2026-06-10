# Gabibbo Says

| | |
|---|---|
| **Section** | OliCyber 2023 Training Camp 1 |
| **Category** | web |
| **Solves** | 864 |

## Overview

The page displays an instruction from the Gabibbo asking the user to send a POST request with a specific parameter:

```
gabibbo=angry
```

## Solve

Simply follow the instructions with a curl request:

```bash
curl -X POST -d "gabibbo=angry" http://gabibbo-says.challs.olicyber.it/
```

returns the flag.