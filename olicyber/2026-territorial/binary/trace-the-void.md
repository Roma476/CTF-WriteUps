# Trace the void

| | |
|---|---|
| **Section** | OliCyber 2026 Selezione Territoriale |
| **Category** | binary |
| **Solves** | 93 |

## Overview

The binary appears to be simple and non-interactive. When executed normally, it prints only a misleading message:

```
Questo programma non ha segreti... o forse si?
```

## Solve

By running the binary under `strace`, it becomes clear what the program is actually doing at syscall level.

After the initial setup and standard library loading, the program performs a redirection of its standard output:

- It opens `/dev/null`
- It duplicates the file descriptor onto stdout using `dup2`

After this redirection, any normal output is discarded.

However, before exiting, the program still performs a final `write()` syscall that sends data directly to the (now hidden) output stream. This behavior is only visible through syscall tracing, which captures the write call before it is discarded by `/dev/null`.

The flag is therefore obtained by inspecting the `write` syscall output in the `strace` trace.