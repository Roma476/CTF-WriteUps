# ITASECshop - 1mln$ Flag

| | |
|---|---|
| **Section** | HighSchools CTF Workshop - 2023 Bari |
| **Category** | web |
| **Solves** | 611 |

## Overview

The challenge gives us the website of the ITASEC gadget shop (`http://itasecshop.challs.olicyber.it/`). Among the items for sale there is the flag itself, priced at 1 million dollars, and the goal is to find a way to buy it.

After creating an account and logging in, the shop shows the list of items. One of them is called `1.000.000$ FLAG` and costs exactly 1 million dollars, while our account balance is only 23 dollars, so a regular purchase is impossible. The page also has a button to donate money, which is the only other feature that interacts with the balance.

## Solve

The donation feature does not validate the amount it receives, and accepts negative values. Since a donation is normally subtracted from the balance, donating `-1000000` dollars flips the sign: instead of decreasing, the balance increases by 1 million dollars.

With the balance now high enough, it is enough to click the buy button on the `1.000.000$ FLAG` item, and the flag is shown on the page.