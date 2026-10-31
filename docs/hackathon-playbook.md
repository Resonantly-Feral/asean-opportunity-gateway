# Hackathon speedrun playbook

Lessons from Hacktoberfest Hack Day KL 2026 (Top 5 finalist of 48).
Check each event's rules: most require the project to be built during the
event, so prepare **skills, templates and checklists**, not the project itself.

## Before the day

- [ ] Accounts ready: GitHub, event platform, AI provider (API key tested), hosting (Streamlit Cloud)
- [ ] Know how to: create a public repo with MIT licence, deploy a Streamlit app, add a secret
- [ ] Screen recorder tested **with microphone** (Windows: Win + Shift + R or Win + Alt + R)
- [ ] YouTube account able to upload public videos
- [ ] Read the problem statements and prize categories; jot 2–3 ideas per statement
- [ ] Bring charger, multi-plug, phone hotspot as Wi-Fi backup

## Timeline for a 4-hour sprint (adjust to the event)

| Time into sprint | Goal |
|---|---|
| 0:00–0:20 | Pick problem statement + prize category. One sentence pitch. Split roles. |
| 0:20 | Create repo (licence, README skeleton, .gitignore, .env.example). Everyone clones. |
| 0:20–1:30 | **One working journey end to end**, ugly is fine. Deploy early. |
| 1:30–2:30 | Make it real: real data with sources, safety checks, demo cases. |
| 2:30–3:00 | Plain-language UI pass ("would a C-suite get it in 10 seconds?"). **Feature freeze.** |
| 3:00–3:30 | Record video (one take), upload, submit. **Submit 15 min early.** |

## The winning formula: looks great + scores well

Winners at this event combined **visual appeal** with a **strong match to the rubric**
(a gamified project won). Plan both from minute one, not at the end.

### 1. Rubric map (first 20 minutes)

Before coding, list every judging criterion and the prize category's wording.
For each one, write the **exact demo moment** that proves it:

| Criterion (from rubric / category) | Demo moment that proves it | Owner |
|---|---|---|
| e.g. "Multimodal experience" | Upload pitch slide → 8/9 becomes 9/9 | |
| e.g. "Working prototype" | Live link, real AI call | |
| e.g. "Clear understanding of the problem" | First 20s of video: the problem in one sentence | |
| e.g. "Unique / impactful" | Trick text caught live | |

If a criterion has no demo moment, it scores nothing. Ask organisers for the
full rubric at the briefing.

### 2. Visual polish (budget 30–45 minutes, not the last 5)

- **First screen sells it:** one-line promise, 3-step strip, one big call to action.
- **One colour theme** and consistent icons; coloured badges for statuses.
- **Show, don't list:** progress bars, cards, a simple chart or before/after.
- **Demo data that looks real** (names, places, numbers) so screenshots look good.
- **Make it fun:** quests, badges, streaks, a satisfying "level up" moment, but only
  earned by real actions (keep it honest).
- **Readable on a projector:** large text, high contrast, zoom 125% when demoing.
- Check every screen on a phone too.

### 3. Keep what worked here

- One working journey first, polish second.
- AI proposes, rules decide, every result shows its proof.
- Wow moment in the first 60 seconds of the demo.
- Real data with sources, honest labels, nothing faked.

## What judges responded to

- A **live link** that works, plus a clear README
- **Honesty**: no fake percentages, evidence shown for every result
- A **wow moment** ("ignore your rules" caught live): **put it first in the demo**
- Real data from official sources, with links
- Two-sided story (founders and investors)
- Engagement: a gamified project won a prize, so make the demo feel fun

## Demo and video

- Put the strongest moment in the first 60 seconds.
- Video must be under the limit (ours ran 3:01 the first time; trim dead seconds).
- Warm up the AI before recording; cut waiting time.
- Upload as **Public**; check in incognito.

## Submission checklist

- [ ] Public repo, licence in root, README with setup and run steps
- [ ] Live demo link checked in incognito (app not asleep)
- [ ] Video link (public)
- [ ] Description: problem statement, problem, solution, how it works, tech, users, uniqueness
- [ ] Prize categories ticked (all that genuinely apply)
- [ ] Teammates added to the submission before submitting
- [ ] AI tools and models disclosed honestly

## Gotchas we hit

- Streamlit kept old code in memory after a deploy → reboot the app; reload modules on each run.
- Live site was deployed from a different branch than expected → check the branch in Streamlit.
- Default AI "thinking" made calls take 1–2 minutes → use minimal thinking for demos.
- API keys pasted into chat or code → use a throwaway key and delete it after.
