# Click Me

| | |
|---|---|
| **Section** | Web Security |
| **Category** | web |
| **Solves** | 3362 |

## Overview

The application is a clicker game where the goal is to reach 10,000,000 cookies by clicking a button.

## Solve

Inspecting the cookies reveals a value used to store the current number of clicks. This value can be modified directly in the browser.

By setting the cookie to a value >= 10,000,000 and refreshing the page, the server accepts the state and returns the flag.