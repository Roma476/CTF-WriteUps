# Weird Device
| | |
|---|---|
| **Section** | HighSchools CTF Workshop - 2023 Verona |
| **Category** | web |
| **Solves** | 253 |

## Overview
The application simulates a hotel captive portal login page that redirects to an "Ubiquiti Networks UAP-AC-PRO WLAN Access Point" admin panel, as shown in the page footer. The `Server` response header reveals the backend is running on `gunicorn`, suggesting a custom Python/Flask application behind the login form rather than a real device firmware.

## Solve
The device name displayed on the page is a direct hint toward the vendor's well-known default credentials. Submitting the login form with:

```
username=ubnt
password=ubnt
```

successfully authenticates as the admin, bypassing the "Invalid username or password" check, and the flag is returned.