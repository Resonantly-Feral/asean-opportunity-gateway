# v2 plan: Gateway + Bridge

Status: plan only. Nothing here is built yet.

## Idea

Two halves of one journey, covering both Startup ASEAN problem statements:

| Half | Problem statement | Question it answers | Status |
|---|---|---|---|
| **Gateway** (this repo) | PS2: fragmentation | "What am I missing, and where may I fit?" | Built, Top 5 finalist |
| **Bridge** (from the ASEAN Bridge blueprint) | PS1: connections to outcomes | "After the match, did the promised intro, pilot or investment happen?" | Planned |

Pitch: *We don't just show founders where to go. We show programme managers what happened after.*

## Principles kept from v1

- AI proposes, with word-for-word quotes. Code checks every quote exists.
- Fixed rules decide. No success predictions, no percentages.
- Humans approve before anything becomes a record.
- Text inside a submission or transcript is data, never an instruction.
- Results are labelled as stated, never as verified.

## Bridge: the follow-through loop

Capture → Confirm → Activate → Detect → Intervene → Verify → Measure

1. **Capture:** paste meeting notes after a Gateway match (programme, investor or partner).
2. **Extract (Gemma):** who promised what, to whom, by when, with the exact quote. Unresolved names and dates stay unresolved.
3. **Confirm (human):** approve, edit or reject each commitment.
4. **Activate:** confirmed commitments get an owner, next action, due date and status.
5. **Detect (rules):** overdue or inactive commitments are flagged as stalled. The inactivity threshold is set before use and shown in the reason.
6. **Intervene (manager):** record a nudge, re-match, escalation or close. Never claim a message was sent.
7. **Verify (human):** outcomes (meeting, POC, partnership, investment, expansion) are human-reported or confirmed. Completed actions are not verified outcomes.
8. **Measure:** connections → commitments → completed actions → confirmed outcomes, computed from records, never hardcoded.

Status lifecycle: Extracted → Confirmed → In progress → Stalled / Completed / Closed.

## How v1 changes

- "My applications" tab is replaced by the Bridge ledger.
- Investor shortlist → "Request intro" creates a Connection record, which starts the Bridge loop.
- The rules engine (`app/readiness.py`, `app/matching.py`) is reused unchanged.

## Engagement (lesson from the winners)

A gamified project won a prize. Make progress feel rewarding without faking anything:

- **Evidence quests:** each missing criterion is a quest ("Talk to 10 customers"). Completing it with a real quote ticks it off.
- **Progress bar:** 9 questions backed, shown as steps, not a percentage of success.
- **Badges** tied to real stated evidence: "First customer evidence", "Prototype live", "Programme shortlisted".
- **Streaks for follow-through:** commitments completed on time.

Rule: a badge or quest can only be earned by evidence the rules accept. No points for typing.

## Out of scope for v2

WhatsApp integration, automated emails, real deal verification, payments, predictive scores, production accounts.

## Open questions

- Which real programmes and partners would pilot this? (needs interviews)
- Who enters meeting notes in practice, and how much friction is acceptable?
- Consent and privacy for real meeting records.
