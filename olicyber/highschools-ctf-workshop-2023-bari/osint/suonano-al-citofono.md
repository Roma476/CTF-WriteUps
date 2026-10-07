# Suonano al citofono...

| | |
|---|---|
| **Section** | HighSchools CTF Workshop - 2023 Bari |
| **Category** | osint |
| **Solves** | 455 |

## Overview

The challenge provides a photo sent by the "shady individual", who claims to have registered for an event organized by a friend of his. The goal is to recover the domain of the website he used to register and then find the name of its admin, which has to be submitted in the format `ITASEC{Nome_Cognome}`.

The photo shows a monitor with a website open on it, and the page clearly reads "ITASEC 2023". That is the only clue available, so the first step is to identify the website from its name.

## Solve

Searching for "ITASEC 2023" on Google leads straight to the event's official website: `https://2023.itasec.it/`.

Once the domain is known, the admin can be found through its registration data. I ran a WHOIS lookup on the domain, which returned the following contact information:

```
Registrant Contact
  Organization:  CINI
  Address:       via ARIOSTO, 25, ROMA, 00198, RM, IT

Admin Contact
  Name:          Paolo Ernesto Prinetto
  Organization:  CINI
  Address:       C.so Italia, 86, GASSINO TORINESE, 00198, TO, IT

Tech Contact
  Name:          Paolo Ernesto Prinetto
  Organization:  CINI
  Address:       C.so Italia, 86, GASSINO TORINESE, 00198, TO, IT
```

The registrant is only an organization (CINI), while both the Admin Contact and the Tech Contact are the same person: Paolo Ernesto Prinetto. Putting his full name in the required format gives the flag.