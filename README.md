# Acadza "Report → Fix"

Turns student "Report error" tickets into safe, reviewable fixes. Original brief: `BRIEF.md`.

| Path | What |
|---|---|
| `results.json` | Triage for all 44 reports (scored file) |
| `findings.json` | 8 defects nobody reported (bonus) |
| `web/` | Faculty console: static, no build. Open `web/index.html` |
| `engine/` | Pipeline: group by question, 2 blind solves, triage prompt, `guards.py` decides the route |
| `scripts/build_results.py` | Builds `results.json` through the real guards |
| `tests/test_guards.py` | 9 safety tests |
| `PROMPTS.md`, `PRODUCT.md` | Required write-ups |

**Provenance:** `results.json` was produced by Claude in chat and then validated by `engine/guards.py`; the live `engine/run.py` has not been run against the API (see `PROMPTS.md` section 0). The console serves these precomputed results and makes no LLM calls.

```bash
pip install anthropic
ANTHROPIC_API_KEY=... python -m engine.run results.live.json   # live engine (model: $MODEL)
python scripts/build_results.py                                  # rebuild results.json + findings.json
# python scripts/build_web_data.py                                 # refresh the console data
```
Deploy: Vercel/Netlify, set the publish directory to `web`.

## Before you submit (only you can do these)
- [ ] Push to a **public** GitHub repo and deploy `web/` (must stay up 7 days)
- [ ] Record the 3-minute video: the queue, one auto-applied case (R001-R003), and one tricky case (R034 or R004)
- [ ] Fill in your real prompts in `PROMPTS.md` section 2, and run the live engine if you can
- [ ] Reply to the email with repo, URL, video, and your own answers to the 4 questions (months, start date, why)
- [ ] **Deadline: Wed 11 Nov 2026, 11:59 PM IST**
