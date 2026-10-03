---
name: life-memory
description: Maintain a private, compact life-memory store when the user wants to remember, retrieve, review, export, correct, or forget personal experiences. Use for long-term personal memory, not ordinary one-off conversation.
agent_created: true
---

# Life Memory

Help the user keep a durable, user-controlled record without turning normal conversation into diary administration. Store only information with future value; treat raw conversation as cold data.

## Operating rules

- Continue the normal conversation first. Do not announce routine storage unless the user explicitly asks to remember something.
- A direct request to remember, save, add to the diary, forget, delete, inspect memories, or export data takes priority.
- Save an ordinary memory only when it has value 2–3: a sustained preference, goal, decision, important relationship or experience, career/value change, or repeated theme. Value 1 belongs only in a daily log; value 0 is not stored.
- Record user-stated facts as facts. Label model-derived trends as a `pattern`, with cautious language such as “可能” or “值得观察”; never present a pattern as a fact.
- Never diagnose health, personality, or mental conditions from memories.
- Preserve changes over time. A later preference does not erase a prior one unless the user asks to delete it.

## Retrieval and context budget

Use the smallest adequate layer: current conversation → profile → index → memories → daily logs → compressed conversation. Do not load a complete history by default.

- Ordinary history question: at most 300 tokens of memory context.
- Complex history question: at most 800 tokens.
- Explicit deep life review: at most 2,000 tokens.
- Default to five results (absolute maximum ten). Keep each selected memory concise.

Before querying history, use [prompts/memory_gate.md](prompts/memory_gate.md). For selection and answer evidence, use [prompts/retrieval.md](prompts/retrieval.md). Use [references/schema.md](references/schema.md) when changing storage or using the command-line helpers.

## Daily and periodic review

For daily processing, use [prompts/daily_extract.md](prompts/daily_extract.md), then apply candidates through `scripts/daily_job.py`. Daily logs are concise (100–200 tokens) and date-upserted so reprocessing cannot duplicate a day. Generate patterns only during weekly/monthly review or when the user explicitly requests analysis.

For merging and time changes, follow [prompts/memory_update.md](prompts/memory_update.md). Use the scripts only for the private local database and never put API keys or sensitive values into debug logs.

## Storage

The SQLite database defaults to `data/life_memory.db` inside this skill folder. Pass `--db <path>` to any script to keep the store somewhere else (for example a private folder outside the skill directory). Only the standard library is required; there is no cloud service and no vector database. Never log the full database contents or any sensitive value into debug output.

## User control

On “forget” or delete requests, set the relevant memory status to `deleted`; deleted entries must never be retrieved. Explain ambiguity and ask for a target only when it is unsafe to infer which memory is meant. Export includes the complete local database data in a portable JSON file.
