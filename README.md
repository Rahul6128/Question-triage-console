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
