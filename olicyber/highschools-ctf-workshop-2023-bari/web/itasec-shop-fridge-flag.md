# ITASECshop - Fridge Flag

| | |
|---|---|
| **Section** | HighSchools CTF Workshop - 2023 Bari |
| **Category** | web |
| **Solves** | 400 |

## Overview

This is the second challenge on the ITASEC gadget shop (`http://itasecshop.challs.olicyber.it/`). This time the description says that one of the flags has to be stored at -10°C, so before the purchase the shop automatically checks that the buyer owns a "Samsung Smart Fridge". The goal is to trick the site into believing we have one.

The article to look at is `-10°C FLAG 🚩`. Clicking the buy button returns an error message: `Solo i Samsung Smart Fridge possono acquistare questo articolo` ("Only Samsung Smart Fridges can buy this item"). Since the site cannot know what device we own other than through the request itself, the check is most likely based on a header sent by the client, and the `User-Agent` is the obvious candidate.

## Solve

I intercepted the buy request with Burp Suite and modified its `User-Agent` header. First I tried a realistic User-Agent string of a Samsung fridge:

```
Mozilla/5.0 (Linux; Tizen 6.0; SAMSUNG Family Hub 9.0) AppleWebKit/537.36 (KHTML, Like Gecko) SamsungBrowser/1.0 Chrome/108.0.5359.1 Mobile Safari/537.36
```

This did not work, the shop still refused the purchase. The check was probably looking for something simpler, so I tried using exactly the name given by the site as the User-Agent:

```
User-Agent: Samsung Smart Fridge
```

With this value the request is accepted and the flag is shown.