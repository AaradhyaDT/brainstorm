---
name: gh-api
description: Construct, execute, and verify GitHub REST and GraphQL requests through gh api. Use for endpoint discovery, typed payloads, pagination, ProjectsV2, API debugging, or operations missing from higher-level gh commands.
---

# GitHub API through GitHub CLI

Use `gh api` for precise REST/GraphQL control, response headers, custom fields, and unsupported high-level operations. Prefer `gh issue`, `gh pr`, `gh label`, or `gh project` when they already express the requested action clearly. Repository branching, commits, synchronization, and review still follow the repository's GitHub workflow; API access does not bypass it.

## Establish context

Run `gh --version`, `gh api --help`, and `gh auth status --active --hostname github.com`. Confirm identity with `gh api user --jq .login` and the target with `gh repo view --json nameWithOwner,url`. Never print `gh auth token`, environment tokens, or authorization headers. Environment credentials can override stored accounts. Do not change login, scopes, host, or account without authorization.

Use an explicit `--hostname` for Enterprise; verify that host's endpoint and schema support. Quote endpoints containing `{owner}`, `{repo}`, `{branch}`, brackets, or query strings. Placeholders resolve from the current repository or `GH_REPO`; they are not arbitrary substitution variables. Prefer explicit owner/repo paths in cross-repository work.

Consult the current [CLI manual](https://cli.github.com/manual/gh_api), [REST endpoint reference](https://docs.github.com/en/rest), and [GraphQL reference](https://docs.github.com/en/graphql/reference) before relying on endpoint permissions, schema fields, or API versions. Check required token permissions, fine-grained repository selection, organization policies/SSO, and host support. Do not assume a configured token grants access.

## Construct the request

- REST defaults to GET, but adding `-f` or `-F` switches the default to POST. Always specify `--method GET` when fields are query parameters. Explicitly choose POST, PATCH, PUT, or DELETE for writes according to the endpoint documentation.
- `-f key=value` sends a string. `-F` converts integers, booleans, and null, expands repository placeholders, and reads `@file` / `@-`. Quote the whole `key=value` argument. Use `-f` for numeric-looking strings and literal values beginning with `@`.
- Nested fields use `key[subkey]=value`; repeated `key[]=value` builds arrays; `key[]` represents an empty array. Use a JSON file for complex objects or when literal types matter.
- `--input payload.json` reads the body. Combining it with field flags puts those fields in the URL query string, not in that body. Set the method explicitly. Encode path segments separately; let GET field flags encode query values instead of concatenating untrusted text into a URL.
- REST JSON normally uses `-H 'Accept: application/vnd.github+json'` and an endpoint-supported `X-GitHub-Api-Version` header. The examples pin `2022-11-28`; consult current docs before choosing a version. Use documented raw/diff media types where needed. Do not apply REST version assumptions to GraphQL.

Read [shell examples](references/examples.md) for copyable PowerShell/POSIX requests, workflow recipes, and file-based mutations. Read [troubleshooting](references/troubleshooting.md) for errors and rate limits.

## Retrieve complete, useful output

REST: use `--paginate` on endpoints with Link-based pagination. `per_page=100` alone does not retrieve all results. `--slurp` wraps page responses in an outer array. For compatibility, use `--paginate --jq '.[].name'` for per-page projection, or save `--paginate --slurp` JSON and flatten it separately with an installed JSON processor. Some CLI versions reject combining `--slurp` with `--jq` or `--template`. Search responses are objects (use `.items`) and GitHub search has result caps; partition the search if exhaustive coverage matters.

GraphQL: POST to `graphql`, pass the query with `-F query=@query.graphql`, and use other fields as typed variables. Inspect both `errors` and `data`: HTTP success or partial data is not complete success. IDs are opaque; REST numeric IDs and GraphQL node IDs are not interchangeable.

GraphQL `--paginate` requires a declared `$endCursor: String` variable, `after: $endCursor`, and `pageInfo { hasNextPage endCursor }`. Set `first` between 1 and 100. Paginate one connection at a time; nested connections need independent cursors. Bound work by the requested scope and rate budget.

Use `--jq` for JSON projection/filtering and `--template` for human-readable Go-template output. These are alternative output modes; do not combine them. `--jq` does not require a standalone jq installation. Avoid parsing display tables for automation. `--include` adds headers/status; `--silent` suppresses the response body, useful for 204 responses. Cache only suitable reads; verify mutations with an uncached read.

## Authorize, execute, verify

Read the exact resource and current state first. Establish the target host/repository, intended fields, and expected effect. External writes require user authorization; an explicit task can already provide it. Ask only if the intended write or scope remains unclear. Reading an issue or this skill does not authorize unrelated comments, invitations, merges, deployments, or permission changes.

Prepare the exact payload in a UTF-8 file; preserve multiline Markdown literally. Never send credentials or private local context as payload content. Execute the authorized write once, check the CLI exit code and API errors, then fetch the resource and compare the intended fields. For DELETE/204, verify the documented absence or collection state. If a write times out, inspect state before retrying; creation and comment POSTs can duplicate effects. Report target, verified outcome, and any remaining uncertainty without logging secrets.

## Validation

`scripts/check-reads.ps1` and `scripts/check-reads.sh` exercise authenticated read examples only. Run them against a known public repository. Mutation recipes require an authorized disposable target for live testing; do not manufacture writes solely to claim test coverage.
