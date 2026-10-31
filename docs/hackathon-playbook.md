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
