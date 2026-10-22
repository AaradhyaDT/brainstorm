# Shell examples and workflow recipes

Run from an authenticated shell with `gh` on PATH. All reads below use public `cli/cli`; change the explicit repository intentionally. Check every exit status before using output. PowerShell examples target PowerShell 7; use `Set-Content -Encoding utf8` to write payloads without legacy encoding surprises. Complex PowerShell automation belongs in a `.ps1` file.

## REST reads (both shells)

```sh
gh api --method GET repos/cli/cli -H 'Accept: application/vnd.github+json' -H 'X-GitHub-Api-Version: 2022-11-28' --jq '{full_name,default_branch}'
gh api --method GET repos/cli/cli/issues -f state=open -F per_page=2 --jq '.[] | select(has("pull_request") | not) | {number,title}'
gh api --method GET repos/cli/cli/labels -F per_page=100 --paginate --jq '.[].name'
gh api --method GET search/issues -f 'q=repo:cli/cli is:issue is:open' -F per_page=2 --jq '.items[] | {number,title}'
gh api repos/cli/cli/milestones --template '{{range .}}{{.number}}: {{.title}}{{"\n"}}{{end}}'
gh api repos/cli/cli/pulls -X GET -F per_page=2 --jq '.[] | {number,title,head:.head.ref,base:.base.ref}'
```

The issues endpoint includes pull requests; filter them when the task requests only issues. Path IDs must come from discovery, not fabricated examples. For one PR use `repos/OWNER/REPO/pulls/NUMBER`; for changed files append `/files` and paginate. Inspect repository metadata with `repos/OWNER/REPO`; labels and milestones have their own collection endpoints.

## GraphQL query file and pagination

Save as `issues.graphql` (literal UTF-8 text):

```graphql
query($owner: String!, $name: String!, $endCursor: String) {
  repository(owner: $owner, name: $name) {
    issues(first: 100, after: $endCursor, states: OPEN) {
      nodes { id number title }
      pageInfo { hasNextPage endCursor }
    }
  }
}
```

PowerShell and POSIX use the same invocation:

```sh
gh api graphql -F 'query=@issues.graphql' -f owner=cli -f name=cli --paginate --jq '.data.repository.issues.nodes[] | {number,title}'
```

When diagnosing, omit projection and inspect `errors` alongside `data`. Do not paginate a mutation.

## Authorized REST update with literal Markdown

After inspecting the issue and obtaining authorization for the exact body replacement, use a disposable issue or the intended real target. These examples overwrite its body; they do not append. Replace OWNER/REPO and 123 with the verified target.

PowerShell:

```powershell
$ErrorActionPreference = 'Stop'
$repo = 'OWNER/REPO'
$number = 123
$body = @'
## Status
Literal `code`, $variables, and backslashes \ remain intact.
'@
@{ body = $body } | ConvertTo-Json -Depth 10 | Set-Content -Encoding utf8 payload.json
gh api "repos/$repo/issues/$number" --jq '{number,body}'
if ($LASTEXITCODE -ne 0) { throw 'Inspection failed' }
gh api --method PATCH "repos/$repo/issues/$number" --input payload.json --jq '{number,body}'
if ($LASTEXITCODE -ne 0) { throw 'Update failed; inspect state before retry' }
$actual = gh api "repos/$repo/issues/$number"
if ($LASTEXITCODE -ne 0) { throw 'Verification read failed' }
$verified = ($actual -join "`n") | ConvertFrom-Json
if ($verified.body -cne $body) { throw 'Body verification mismatch' }
```

POSIX (requires Python 3 for JSON escaping and comparison):

```sh
set -eu
repo='OWNER/REPO'
number=123
cat > body.md <<'EOF'
## Status
Literal `code`, $variables, and backslashes \ remain intact.
EOF
python3 -c 'import json,pathlib; pathlib.Path("payload.json").write_text(json.dumps({"body":pathlib.Path("body.md").read_text()}),encoding="utf-8")'
gh api "repos/$repo/issues/$number" --jq '{number,body}'
gh api --method PATCH "repos/$repo/issues/$number" --input payload.json --jq '{number,body}'
gh api "repos/$repo/issues/$number" > actual.json
python3 -c 'import json,pathlib; assert json.loads(pathlib.Path("actual.json").read_text())["body"] == pathlib.Path("body.md").read_text()'
```

Keep scratch payloads out of commits and logs if they contain sensitive content. For issue creation use documented POST `/issues` with `title` and `body`; verify the returned number before further edits. For comments use POST `/issues/NUMBER/comments`, then GET `/issues/comments/COMMENT_ID` to verify. Do not confuse issue numbers with comment IDs.

## Labels, milestones, and repository metadata writes

Use these endpoint/payload combinations only after discovery and authorization. Send JSON via `--input` and verify with a fresh GET.

| Task | Method and endpoint | Payload / verification |
| --- | --- | --- |
| Create label | POST `repos/OWNER/REPO/labels` | `{"name":"triaged","color":"0366d6","description":"Reviewed"}`; GET labels and match name |
| Add issue labels | POST `repos/OWNER/REPO/issues/NUMBER/labels` | `{"labels":["triaged"]}`; GET issue labels |
| Replace issue labels | PUT same endpoint | Replaces the entire set; inspect existing labels first |
| Create milestone | POST `repos/OWNER/REPO/milestones` | `{"title":"Next release"}`; verify returned milestone number |
| Assign milestone | PATCH `repos/OWNER/REPO/issues/NUMBER` | `{"milestone":MILESTONE_NUMBER}`; GET issue `.milestone.number` |
| Update description | PATCH `repos/OWNER/REPO` | `{"description":"Approved description"}`; GET repo `.description` |

Label names in URL paths require percent encoding. Closing/merging PRs changes repository state and needs authorization; prefer `gh pr merge` with repository review/CI governance rather than a raw merge endpoint.

## Authorized GraphQL issue update (both shells)

Discover the target issue with a REST read and use its `node_id`. After authorization, save this as `update.graphql`:

```graphql
mutation($id: ID!, $title: String!) {
  updateIssue(input: {id: $id, title: $title}) {
    issue { id title }
  }
}
```

```sh
gh api graphql -F 'query=@update.graphql' -f id=ISSUE_NODE_ID -f 'title=Approved issue title'
```

Check the exit status and the unfiltered response for `errors`. Independently GET `repos/OWNER/REPO/issues/NUMBER` and compare `.title` with the intended title. This file-based query and typed-variable pattern was exercised in PowerShell and Git Bash against a disposable issue. The REST body's PowerShell verification decodes JSON to preserve CRLF/LF and compares case-sensitively; comparing line-split `--jq .body` output can falsely report a mismatch.

## ProjectsV2 GraphQL mutation

Discover the project under its actual user or organization owner using `projectsV2(first: 100)` with pagination; verify title, URL, access, and project node ID. Resolve the issue/PR's node ID from `repository { issue(number: ...) { id } }` or `pullRequest`. Projects permissions are separate from repository permissions.

Save as `add-item.graphql`:

```graphql
mutation($project: ID!, $content: ID!) {
  addProjectV2ItemById(input: {projectId: $project, contentId: $content}) {
    item { id }
  }
}
```

After authorization, both shells can run (replace IDs):

```sh
gh api graphql -F 'query=@add-item.graphql' -f project=PROJECT_NODE_ID -f content=ISSUE_NODE_ID
```

Inspect `errors` and save the returned item ID. Verify with `node(id: $project) { ... on ProjectV2 { items(first: 100, after: $endCursor) { nodes { id content { ... on Issue { id url } ... on PullRequest { id url } } } pageInfo { hasNextPage endCursor } } } }`, passing the project and cursor variables. For field updates, discover `fields` and the current item values first: single-select options require option IDs; date, text, number, and iteration values have different input shapes. Consult the current `updateProjectV2ItemFieldValue` schema rather than guessing. Do not retry an uncertain add without checking existing items.
