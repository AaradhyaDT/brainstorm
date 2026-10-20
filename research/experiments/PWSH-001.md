# Experiment: PWSH-001 — PowerShell Profile Startup Latency

- **Date:** 2026-10-19
- **Target:** Windows 11 PowerShell 7.6.5 interactive ConsoleHost startup
- **Classification:** `EMPIRICALLY_VERIFIED` (single-machine measurements)
- **Objective:** Find the source of slow normal `pwsh` startup and check whether profile location or startup initialization accounted for the delay.

## Method

Measured the resolved `pwsh.exe` in an interactive terminal with the profile enabled and with `-NoProfile`. Compared profile locations in alternating order across five warm runs per location. Also timed initialization commands in a fresh interactive host. A separate non-interactive benchmark showed startup cost without terminal initialization and was not used as the primary comparison.

## Results

| Condition | Warm startup |
|---|---:|
| Before changes, normal profile | 1,547–1,618 ms |
| `-NoProfile` | 220–229 ms initially; 228–233 ms in later runs |
| Profile in Local AppData on C: | 1,559–1,596 ms; median 1,587 ms |
| Profile on ReFS Dev Drive F: | 1,531–1,601 ms; median 1,573 ms |
| After lazy optional-module loading and editor discovery | 943–956 ms warm |

The Dev Drive median was 14 ms lower (about 0.9%), inside observed variation. Profile location was not a material source of startup delay. The profile itself accounted for most of the initial difference from `-NoProfile`.

Fresh-shell component timings varied between launches. In the profiled diagnostic shell, optional module initialization and command discovery were the largest avoidable costs; Oh My Posh and PSReadLine remained enabled. Scheduled network profile updates were not due during measurement and were removed from automatic startup in favor of an explicit manual update command.

## Change and verification

The active profile lives at `%LOCALAPPDATA%\PowerShell\profile.ps1`; the conventional OneDrive Documents profile is a one-line loader. The Dev Drive copy at `F:\PowerShell\profile.ps1` was used for benchmarking and is not active.

Optional listing modules load on first directory listing. Editor lookup runs when the `vim` alias is invoked. Startup was checked in fresh interactive shells; directory listing output matched the native command in a parity comparison, Terminal-Icons loaded on first listing, aliases resolved, and the prompt remained available. Warm startup fell to 943–956 ms, about 40% below the original range.

## Limits

These are machine- and cache-specific observations, not general PowerShell timings. The first measured launch was slower than subsequent warm runs. The benchmark does not isolate OneDrive file latency from profile initialization cost; the near-equal local and Dev Drive results only show that moving the profile between these tested volumes did not materially change warm startup.

## Packaged PowerShell compatibility follow-up

On 2026-10-19, the user's default WindowsApps PowerShell 7.6.7 launch could not see `%LOCALAPPDATA%\PowerShell\profile.ps1`, although the bundled PowerShell 7.6.5 runtime could read the same path and both printed the same `%LOCALAPPDATA%` value. The Store package reported the directory as absent. The standard OneDrive Documents profile path was visible to 7.6.7, so the optimized profile was restored there and the loader removed. `GetProfileDir` now uses the actual profile root, keeping the prompt theme available. In an interactive 7.6.7 smoke check, the profile loaded, the prompt existed, Terminal-Icons was absent before a listing and loaded after it. This demonstrates that profile relocation must be tested against the exact PowerShell executable in use; environment path strings alone do not establish filesystem visibility.
