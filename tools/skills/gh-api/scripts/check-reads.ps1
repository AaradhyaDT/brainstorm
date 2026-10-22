param([string]$Repository = 'cli/cli')
$ErrorActionPreference = 'Stop'
function Read-Gh([string[]]$Arguments) {
    $result = & gh @Arguments
    if ($LASTEXITCODE -ne 0) { throw 'gh read failed' }
    return ($result -join "`n")
}
$repo = Read-Gh @('api', "repos/$Repository") | ConvertFrom-Json
if ($repo.full_name -ne $Repository) { throw 'Repository mismatch' }
$pages = Read-Gh @('api', '-X', 'GET', "repos/$Repository/labels", '-F', 'per_page=100', '--paginate', '--slurp') | ConvertFrom-Json
if ($pages.Count -lt 1) { throw 'No pagination response' }
$query = 'query { repository(owner:"cli", name:"cli") { nameWithOwner } }'
$response = Read-Gh @('api', 'graphql', '-f', "query=$query") | ConvertFrom-Json
if ($response.errors -or $response.data.repository.nameWithOwner -ne 'cli/cli') { throw 'GraphQL failed' }
$null = Read-Gh @('api', "repos/$Repository/milestones", '--template', '{{range .}}{{.number}}{{"\n"}}{{end}}')
Write-Output 'PASS: REST identity, pagination, GraphQL, template (read-only)'
