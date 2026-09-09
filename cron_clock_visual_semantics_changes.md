# Visual-Semantics Change Ledger

This transformation applies only the confirmed color rules and preserves silent interstices. It creates no VEVENT for demon/grace days or non-period minutes.

| UID | Prior color field | Result |
|---|---|---|
| `millenium-vault_time@cron_clock` | `COLOR:` | `COLOR:white` |
| `century-vault_time@cron_clock` | `COLOR:` | `COLOR:white` |
| `decade-vault_time@cron_clock` | `COLOR:` | `COLOR:white` |
| `year-vault_time@cron_clock` | `COLOR:` | `COLOR:white` |
| `q1-vault_time@cron_clock` | `COLOR:` | `<removed: undecided>` |
| `q2-vault_time@cron_clock` | `COLOR:` | `<removed: undecided>` |
| `q3-vault_time@cron_clock` | `COLOR:` | `<removed: undecided>` |
| `q4-vault_time@cron_clock` | `COLOR:` | `<removed: undecided>` |
| `s1-vault_time@cron_clock` | `COLOR:` | `<removed: undecided>` |
| `s2-vault_time@cron_clock` | `COLOR:` | `<removed: undecided>` |
| `s3-vault_time@cron_clock` | `COLOR:` | `<removed: undecided>` |
| `s4-vault_time@cron_clock` | `COLOR:` | `<removed: undecided>` |
| `s5-vault_time@cron_clock` | `COLOR:` | `<removed: undecided>` |
| `s6-vault_time@cron_clock` | `COLOR:` | `<removed: undecided>` |
| `month-vault_time@cron_clock` | `COLOR:` | `<removed: undecided>` |
| `january-vault_time@cron_clock` | `COLOR:` | `<removed: undecided>` |
| `february-vault_time@cron_clock` | `COLOR:` | `<removed: undecided>` |
| `march-vault_time@cron_clock` | `COLOR:` | `<removed: undecided>` |
| `april-vault_time@cron_clock` | `COLOR:` | `<removed: undecided>` |
| `may-vault_time@cron_clock` | `COLOR:` | `<removed: undecided>` |
| `june-vault_time@cron_clock` | `COLOR:` | `<removed: undecided>` |
| `july-vault_time@cron_clock` | `COLOR:` | `<removed: undecided>` |
| `august-vault_time@cron_clock` | `COLOR:` | `<removed: undecided>` |
| `september-vault_time@cron_clock` | `COLOR:` | `<removed: undecided>` |
| `october-vault_time@cron_clock` | `COLOR:` | `<removed: undecided>` |
| `november-vault_time@cron_clock` | `COLOR:` | `<removed: undecided>` |
| `december-vault_time@cron_clock` | `COLOR:` | `<removed: undecided>` |
| `week-vault_time@cron_clock` | `COLOR:` | `<removed: undecided>` |
| `day-vault_time@cron_clock` | `COLOR:` | `<removed: undecided>` |
| `dawn-vault_time@cron_clock` | `COLOR:gold` | `<removed: undecided>` |
| `noon-vault_time@cron_clock` | `COLOR:silver` | `<removed: undecided>` |
| `dusk-vault_time@cron_clock` | `COLOR:black` | `<removed: undecided>` |
| `yan-vault_time@cron_clock` | `COLOR:violet` | `COLOR:red` |
| `tan-vault_time@cron_clock` | `COLOR:indigo` | `COLOR:orange` |
| `tethera-vault_time@cron_clock` | `COLOR:blue` | `COLOR:yellow` |
| `pits-vault_time@cron_clock` | `COLOR:yellow` | `COLOR:blue` |
| `sethera-vault_time@cron_clock` | `COLOR:orange` | `COLOR:indigo` |
| `azer-vault_time@cron_clock` | `COLOR:red` | `COLOR:violet` |
| `hour-vault_time@cron_clock` | `COLOR:` | `<removed: undecided>` |
| `half-vault_time@cron_clock` | `COLOR:` | `<removed: undecided>` |
| `score-vault_time@cron_clock` | `COLOR:` | `<removed: undecided>` |
| `dozen-vault_time@cron_clock` | `COLOR:` | `<removed: undecided>` |
| `minute-vault_time@cron_clock` | `COLOR:` | `<removed: undecided>` |
| `tick-vault_time@cron_clock` | `COLOR:` | `COLOR:black` |

## Preserved Silence

The five internal senary demon/grace days, leap-year additional grace day, and non-period minutes between named 204-minute rhythms remain absent from the output. No placeholder or filler event was created.

## Unchanged Outside Scope

All DTSTART, DURATION, RRULE, UID, RELATED-TO, category, priority, description, and calendar-level values were preserved exactly from the supplied source. The output uses CRLF content-line delimiters.
