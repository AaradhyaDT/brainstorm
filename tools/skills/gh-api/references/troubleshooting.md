# Errors, limits, and sources

Capture the CLI exit status immediately (`$LASTEXITCODE` in PowerShell, `$?` in POSIX). Avoid pipelines that hide a failed request. In scripts, stop before parsing or mutating when a preceding request fails. GraphQL can contain `errors` and partial `data` even when the transport succeeds; inspect both.

| Symptom | Check / response |
| --- | --- |
| 401 | Active host/account and environment credential precedence; never print tokens |
| 403 | Endpoint permissions, SSO, organization policy, and rate headers; more scopes do not fix every 403 |
| 404 for a known resource | Exact host/path/ID and private-resource access; absence is not proven by an unauthorized 404 |
| 409 / 412 | Conflicting state or failed precondition; re-read before deciding on a new write |
| 422 | Validation response, required fields, types, duplicate names, and accepted enum values |
| Unexpected POST | Fields changed the default method; add `--method GET` for query parameters |
| Body fields ignored | `--input` plus fields places fields in the query string |
| Missing results | Link pagination, GraphQL cursors, search caps, permission visibility, nested connections |
| GraphQL schema error | Current host schema, variable types, node IDs, nullable fields, and selection sets |
| 204 / empty body | Valid for some mutations; verify documented resulting state separately |
| Timeout / 5xx | Bounded read retries with backoff; inspect state before retrying writes |

Use `--include` to inspect status and `x-ratelimit-*`, `retry-after`, and `link` headers. `--verbose` can expose private request/response bodies; use locally only when necessary and redact before sharing. Never enable token-printing or copy credential-bearing traces. Avoid `--cache` when diagnosing current state.

For rate limits, honor `retry-after`; if remaining is zero, wait until the reset UTC epoch. For secondary limits without those signals, wait at least a minute and use bounded exponential backoff. Reduce request volume/concurrency and stop after the chosen retry budget (for example three attempts). Do not blindly retry validation or permission errors. GraphQL has its own cost/node limits; inspect `rateLimit { cost remaining resetAt }` where appropriate.

Official sources checked 2026-10-22; recheck when behavior or schema matters:

- [gh api flags and semantics](https://cli.github.com/manual/gh_api)
- [CLI formatting](https://cli.github.com/manual/gh_help_formatting)
- [REST troubleshooting](https://docs.github.com/en/rest/using-the-rest-api/troubleshooting-the-rest-api)
- [REST API versions](https://docs.github.com/en/rest/about-the-rest-api/api-versions)
- [GraphQL pagination](https://docs.github.com/en/graphql/guides/using-pagination-in-the-graphql-api)
- [Projects API](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-api-to-manage-projects)
