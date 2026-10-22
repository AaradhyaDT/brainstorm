# EXP-045: GitHub API skill validation

Date: 2026-10-22. Issue: https://github.com/Aaradhya-Dev-Tamrakar/brainstorm/issues/45

## Delivered artifact

[[gh-api]] lives at `tools/skills/gh-api/SKILL.md`, with shell examples, troubleshooting, and executable read checks. The master skill index links it. It complements [[github-workflow]] and does not replace repository VCS governance.

## EMPIRICALLY_VERIFIED

- GitHub CLI 2.102.0 resolved to the same installation in PowerShell and Git Bash.
- `pwsh -NoProfile -File tools/skills/gh-api/scripts/check-reads.ps1`: passed REST repository identity, paginated labels, GraphQL repository lookup, and template output.
- Git Bash running `tools/skills/gh-api/scripts/check-reads.sh`: passed the corresponding read checks.
- Initial `--paginate --slurp --jq` failed in Git Bash with `the --slurp option is not supported with --jq or --template`. Examples now use per-page projection or standalone slurped JSON. This is the reason for the compatibility note.
- Skill creator `quick_validate.py tools/skills/gh-api`: passed.
- `audit.bat`: structural gate passed; 67 behavioral regression tests passed.
- `sim.bat`: completed successfully.
- Follow-up live mutation validation used disposable issue [#46](https://github.com/Aaradhya-Dev-Tamrakar/brainstorm/issues/46). Both exact REST body-update shell recipes passed post-read comparisons after correcting the PowerShell example. File-based GraphQL `updateIssue` title mutations passed in PowerShell and Git Bash with independent REST verification. Cleanup verified the issue remained closed.
- The first PowerShell comparison incorrectly normalized CRLF into LF when collecting `--jq .body` output. It now decodes the full JSON response and compares `.body` case-sensitively, preserving line endings.
- Git Bash's `python3` command initially resolved to a Windows Store alias. The POSIX recipe was tested with a temporary PATH-local `python3` shim pointing to installed CPython 3.14; no global PATH or alias settings were changed. Python 3 remains an explicit prerequisite for that recipe.
- `graphify update .`: completed, producing 7401 nodes and 8797 edges. It refreshed the code graph; its own output requires an assistant semantic update for documentation. Do not infer complete semantic indexing of the new Markdown from that run.

## Documentation-grounded guidance and limits

The CLI manual, official GraphQL pagination guide, REST issue reference, and REST troubleshooting guide were consulted on this date. Label, milestone, repository-settings, and ProjectsV2 recipes remain documentation-grounded examples; those mutations were not executed. Live mutation coverage is limited to the disposable issue's body/title and closure. Read checks use the public `cli/cli` repository; the selected repository argument applies to REST checks while the GraphQL check deliberately uses that fixed public fixture.

The user-facing skill does not contain machine credentials, private notebook IDs, or personal local configuration. Installation into global skill locations and cross-tool customization synchronization are separate from this repository artifact.
