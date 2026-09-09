# Confirmed Visual Semantics

## Color Rules

| Calendar layer or group | Color rule | Repair constraint |
|---|---|---|
| Any seven-item group | **ROYGBIV**, in item order: red, orange, yellow, green, blue, indigo, violet. | Preserve the ordered sequence. Do not flatten, reorder, or substitute a different seven-color palette. |
| Years | **White**. | Preserve `COLOR:white` where a year-level visual marker is represented. |
| Seconds | **Black**. | Preserve `COLOR:black` for the second-level tick. |
| All other layers | **Undecided**. | Do not assign a color and do not replace an absent or empty color with an inferred palette. |

The seven named weekdays and the seven named 204-minute rhythms are the currently evident ROYGBIV groups. Any future seven-item group follows the same order unless Logan explicitly overrides it.

## Combined Repair Constraint

Colors are semantic metadata. The same rule applies to silent interstices: demon/grace days and the non-period minutes between named rhythms are intentional absence, not incomplete coverage. Future mechanical repairs must preserve both the specified color assignments and the intentional silence, without inventing visual or event data.
