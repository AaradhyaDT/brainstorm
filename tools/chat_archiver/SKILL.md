---
name: chat-archiver
description: >-
  Universal AI chat archiver and transcript reader for reading, summarizing, and archiving
  conversations from Antigravity Brain (~/.gemini/antigravity/brain) and external AI share links
  (ChatGPT, Google Gemini) directly into the active repository, workspace, or research archives (e.g. brainstorm/research/transcripts).
---

# Chat Archiver & Reader Skill (`save-chat` & `read-chat`)

CRITICAL RULE: Whenever the user asks to inspect, read, summarize, or archive:
1. An **Antigravity conversation session** (by UUID, prefix like `2417d518`, or latest in brain)
2. An **external shared conversation link** (ChatGPT, Google Gemini)

**DO NOT** write scratch Python scripts, scrape raw files manually, or stream tokens parsing JSONL/HTML.
You **MUST** immediately run the globally installed CLI tools:
- **`read-chat`** to inspect, summarize (bird's-eye view), filter turns, or export Antigravity brain sessions.
- **`save-chat`** to download and archive external share links (or directly archive brain sessions).

## Antigravity Brain Sessions (`read-chat`)

The `read-chat` CLI directly reads and parses transcripts from `~/.gemini/antigravity/brain/<id>/.system_generated/logs/transcript.jsonl` (with automatic fallback to `transcript_full.jsonl` for truncated fields).

### 1. Bird's-Eye View / Session Summary (RECOMMENDED)
To see high-level progress, timeline of milestones, tool statistics, and final deliverable:
```bash
read-chat <CONVERSATION_ID> --summary
# or short flag:
read-chat <CONVERSATION_ID> -s
```
*(Accepts full UUIDs like `2417d518-af98-4175-b36e-80576c01a7b8` or short 8-char prefixes like `2417d518`)*

### 2. User Prompts Audit
To view all progressive user requests across the session:
```bash
read-chat <CONVERSATION_ID> --user-only
# or short flag:
read-chat <CONVERSATION_ID> -u
```

### 3. Inspect Specific Turns
```bash
# View last N turns
read-chat <CONVERSATION_ID> --last 3

# View specific turn range
read-chat <CONVERSATION_ID> --turns 1-5

# Include detailed tool execution arguments and results
read-chat <CONVERSATION_ID> --last 2 --tools
```

### 4. List Recent Brain Conversations
```bash
read-chat --list
# or short flag:
read-chat -l
```

### 5. Search Across Brain Transcripts
```bash
read-chat --search "query"
# or short flag:
read-chat -q "query"
```

### 6. Export Antigravity Session to Clean Markdown
```bash
# Export to default research/transcripts or docs/chat_history
read-chat <CONVERSATION_ID> --export

# Export to custom path
read-chat <CONVERSATION_ID> -o "path/to/session.md"
```

---

## External Share Links & Direct Archiving (`save-chat`)

### 1. Save External Share Link (ChatGPT / Gemini)
```bash
save-chat "<URL>"
save-chat "<URL>" --dir "f:/Aaradhya-Dev-Tamrakar/brainstorm/research/transcripts"
```

### 2. Save Antigravity Brain Session via `save-chat`
```bash
save-chat <CONVERSATION_ID>
save-chat <CONVERSATION_ID> --dir "docs/chat_history"
```

### 3. Append Mode (Continuation of Last / Specified Transcript)
```bash
save-chat "<URL_OR_ID>" --append
# or short form:
save-chat "<URL_OR_ID>" -a
```
