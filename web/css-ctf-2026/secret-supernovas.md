# Secret Supernovas — Web (GraphQL), 215 pts

## Objective
A "Star City Observatory" login app at `http://34.116.80.78:9982/` (given creds `cadet` / `star`).
The dashboard shows 3 star cards. Hint: *"This is just a list of stars. Nothing else to see here..."*
Find the flag. Flag format: `CSSCTF{...}`

## Concepts
- The page is a **SvelteKit** app whose data comes from a single **GraphQL** endpoint (`POST /graphql`).
- GraphQL exposes **one endpoint, many queries**. The UI only renders what *it* asked for —
  the server will return far more if you ask.
- **Introspection**: a GraphQL server can describe its own schema (`__schema`). Unless disabled,
  this leaks every type, field, and root query — including ones the UI never uses.
- The request body is JSON: `{"query":"<graphql here>"}` — not raw GraphQL.

## Steps
**1. Find the API.** Log in (`cadet`/`star`), open DevTools → **Network**, reload. Among the requests
is `POST graphql` returning JSON. Its body:
```graphql
query Stars { stars { id name spectralClass magnitude classification galaxy { name } } }
```

**2. Introspect the schema.** Right-click the request → **Edit and Resend**, keep the headers/cookie,
replace the body with:
```json
{"query":"{ __schema { queryType { name } types { name kind fields { name type { name kind ofType { name } } } } } }"}
```
The schema reveals more than the UI uses:
- `Query` roots: `stars`, `star`, `galaxies`, `galaxy`, **`user`**
- `Star` fields: id, name, spectralClass, magnitude, classification, galaxy, **`owner` → Person**
- `Person` fields: first_name, last_name, id, date_of_birth, **`description`**

The hidden `Star.owner` (a `Person`) with a free-text `description` is the obvious place to look.

**3. Ask for the hidden field.** Extend the query to pull each star's owner:
```json
{"query":"{ stars { name owner { first_name last_name description } } }"}
```
The response contains **11 stars** (the UI only rendered 3). One owner's `description` is the flag:
```
Black Canary → Laurel Lance → CSSCTF{we_l000ve_grafs}
```

## Flag
```
CSSCTF{we_l000ve_grafs}
```

## Takeaway
When a page's data comes from **GraphQL**, the rendered UI is just *one* query — the schema is the
real attack surface. First move: **run an introspection query**; enumerate every root query and every
field, then request the ones the UI hides. Here the `stars` query already returned everything —
the app filtered to 3 cards client-side, but `owner.description` (and the extra stars) were one query away.
Defence: **disable introspection in prod** and don't rely on the client to hide sensitive fields —
enforce authorization server-side per field.
Tools worth knowing: **GraphiQL / Apollo Sandbox**, **graphql-voyager**, **InQL**, **clairvoyance**
(schema recovery when introspection is off).
