# LongMemEval grading rubric (ledger answers)

You grade answers a chat assistant gave about a user's past conversations. For each item you see the question, the date it was asked, its type, the GOLD answer, and the RESPONSE. Grade only the RESPONSE against the GOLD. Do not use outside knowledge, and do not reward style.

Verdicts:
- `correct`: the response states the gold answer or an equivalent. Paraphrase, units and formatting may differ. Extra true detail is fine.
- `partial`: some of a multi-part gold answer is right and some is missing, or the right answer is given but hedged next to a conflicting one.
- `wrong`: anything else, including "I don't know" when the gold has an answer.

Per-type rules:
- **is_abs = true** (the question is unanswerable; the gold explains what is missing): `correct` only if the response says it does not know or that the information is not available, or explicitly corrects the false premise. A response that invents an answer is `wrong`.
- **temporal-reasoning:** do not penalize off-by-one day counts when the gold allows it, or when the gold says "(including the last day)". Orderings must match exactly.
- **knowledge-update:** `correct` if it gives the updated (most recent) value, even if it also mentions the old one as old. It is `wrong` if it gives only the old value, or presents the old value as current.
- **single-session-preference:** the gold describes what a good answer would take into account. `correct` if the response is clearly tailored to the user's stated preferences, gear or situation in the gold. `wrong` if it is generic advice that ignores them. `partial` if it touches them only in passing.
- **multi-session counts and totals:** the number must match. A different number is `wrong`, even with reasonable reasoning.
- If a response says it doesn't know and also gives the right answer, grade the answer it commits to. If it commits to neither, it is `wrong`.

Output: one JSON object per item, `{"question_id": ..., "verdict": "correct"|"partial"|"wrong", "reason": "<= 20 words"}`. Write the whole list as a JSON array to the output path you were given. Grade every item; skip none.
