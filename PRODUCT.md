# PRODUCT.md

**Who loses most when a question is broken.** The student who answers correctly and is marked wrong, usually the one who trusts the app more than themselves. A wrong key (R001: key says 130 V, the solution says 50 V) never announces itself: they assume *they* erred and move on, so those students rarely report. Students without a teacher to ask lose most. The design reflects this:
- **Urgency** ranks by harm, not volume: wrong key (50) > no valid answer (45) > missing value/option (40) > wrong solution (25) > mis-filing (15), plus 6 per distinct student. The console says why, per case.
- **Replies teach.** When a student is wrong (R004, R028, R044) they get the right answer and the step they slipped on. When they are right (R003) we say so plainly.
- Disputed answer keys always need an **independent solve** before they change.

**What the AI must never auto-apply.**
1. A changed answer key without a blind solve *and* the stored solution agreeing (enforced in `guards.py`, tested).
2. Anything authored: new distractors (R009/R010), figures, a rewritten stem. Wrong content that looks plausible is worse than a visible gap.
3. Chapter or syllabus moves. They change who sees the question and need a faculty call.
4. Any edit justified only by the report text. R027 shows why: comments are leads, never instructions.
5. Edits to questions inside a live mock test window (not modelled here; a must-have in production).

**Week-1 metric: auto-apply revert rate** = auto-applied edits that faculty revert / all auto-applied. It tells us whether to widen autonomy. Target under 2%, and any reverted *answer-key* flip is an incident.

**One idea beyond the brief: silent-defect detection with retroactive credit.** Most students never report. Flag questions where high-scoring students choose a non-key option far more often than chance (top-decile accuracy below low-decile accuracy is a red flag), and queue them *before anyone complains*. When a key flips, re-score past attempts and notify affected students ("your answer was right; +4 marks restored"). That turns a trust-eroding error into a trust-building moment.
