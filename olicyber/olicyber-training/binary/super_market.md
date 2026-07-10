# Super Market

| | |
|---|---|
| **Section** | Software Security |
| **Category** | binary |
| **Solves** | 1177 |

## Overview

The program implements a simple shop where products are stored in a fixed array:

```c
Product ps[] = {
    {"Penna rossa", 1, pennaRossa},
    {"Pasticciotto alla crema", 3, pasticciotto},
    {"flag", 1000000, flag}
};
```

User input selects an item and quantity, then computes:

```c
cost = ps[choice-1].price * amount;
```

The product index `choice` is validated, but `amount` is not restricted in sign.

## Solve

By selecting the flag product (`choice = 3`) and providing a negative `amount`, the computed cost becomes negative.

This leads to the execution of:

```
ps[choice-1].foo();
```

which triggers `flag()` and prints the flag.