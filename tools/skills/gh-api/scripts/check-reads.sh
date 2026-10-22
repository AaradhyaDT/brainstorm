#!/bin/sh
set -eu
repo=${1:-cli/cli}
test "$(gh api "repos/$repo" --jq .full_name)" = "$repo"
gh api -X GET "repos/$repo/labels" -F per_page=100 --paginate --jq '.[].name'
test "$(gh api graphql -f 'query=query { repository(owner:"cli", name:"cli") { nameWithOwner } }' --jq .data.repository.nameWithOwner)" = cli/cli
gh api "repos/$repo/milestones" --template '{{range .}}{{.number}}{{"\n"}}{{end}}'
printf '%s\n' 'PASS: REST identity, pagination, GraphQL, template (read-only)'
