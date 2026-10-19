#!/usr/bin/env python3
"""
read_chat.py
------------
Antigravity Brain Conversation Reader & Archiver CLI.

Reads, inspects, summarizes, and exports Google Antigravity agent conversation transcripts
from the local brain directory (~/.gemini/antigravity/brain/<conversation-id>).

Features:
- List recent conversations (--list / -l)
- Keyword search across transcripts (--search / -q)
- Bird's-eye session summary & milestone timeline (--summary / -s)
- User-only prompt audit (--user-only / -u)
- Turn filtering (--turns, --last)
- Publication-grade Markdown export (--export / -o / --dir)
- Transparent handling of truncated_fields via transcript_full.jsonl fallback
"""

from __future__ import annotations

import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass



def get_default_brain_dir() -> Path:
    """Locates Antigravity brain storage directory."""
    user_home = Path(os.path.expanduser("~"))
    brain_dir = user_home / ".gemini" / "antigravity" / "brain"
    return brain_dir


def clean_prompt_text(text: str) -> str:
    """Strips system XML tags (<USER_REQUEST>, <ADDITIONAL_METADATA>, etc.) for readability."""
    if not text:
        return ""
    # Extract inner user request if wrapped in <USER_REQUEST>
    m = re.search(r"<USER_REQUEST>(.*?)</USER_REQUEST>", text, re.DOTALL | re.IGNORECASE)
    if m:
        text = m.group(1)
    else:
        # Strip other known metadata tags
        text = re.sub(r"<ADDITIONAL_METADATA>.*?</ADDITIONAL_METADATA>", "", text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<USER_SETTINGS_CHANGE>.*?</USER_SETTINGS_CHANGE>", "", text, flags=re.DOTALL | re.IGNORECASE)
    return text.strip()


def resolve_conversation_path(target: str, brain_dir: Optional[Path] = None) -> Path:
    """
    Resolves a conversation target to its brain folder path.
    Accepts:
    - Full path to brain directory or transcript.jsonl
    - Full UUID (e.g. 2417d518-af98-4175-b36e-80576c01a7b8)
    - Partial UUID prefix (e.g. 2417d518)
    """
    if brain_dir is None:
        brain_dir = get_default_brain_dir()

    target_path = Path(target)
    if target_path.exists():
        if target_path.is_file():
            # If transcript.jsonl was passed, return parent conversation root
            if target_path.name in ("transcript.jsonl", "transcript_full.jsonl"):
                return target_path.parent.parent.parent
            return target_path.parent
        return target_path

    # Try matching within brain directory
    if brain_dir.exists():
        exact = brain_dir / target
        if exact.exists():
            return exact

        # Search for prefix match
        matches = [d for d in brain_dir.iterdir() if d.is_dir() and d.name.lower().startswith(target.lower())]
        if len(matches) == 1:
            return matches[0]
        elif len(matches) > 1:
            matching_ids = "\n  - ".join(m.name for m in matches[:5])
            raise ValueError(f"Ambiguous conversation prefix '{target}'. Matches:\n  - {matching_ids}")

    raise FileNotFoundError(f"Conversation '{target}' not found in {brain_dir}")


def find_latest_conversation(brain_dir: Optional[Path] = None, exclude_id: Optional[str] = None) -> Path:
    """Finds the most recently modified conversation in the brain directory."""
    if brain_dir is None:
        brain_dir = get_default_brain_dir()

    if not brain_dir.exists():
        raise FileNotFoundError(f"Brain directory not found: {brain_dir}")

    convs = [
        d for d in brain_dir.iterdir()
        if d.is_dir() and (d / ".system_generated" / "logs" / "transcript.jsonl").exists()
    ]
    if exclude_id:
        convs = [d for d in convs if d.name.lower() != exclude_id.lower()]

    if not convs:
        raise FileNotFoundError(f"No valid conversations found in {brain_dir}")

    convs.sort(key=lambda d: d.stat().st_mtime, reverse=True)
    return convs[0]


class ConversationTranscript:
    """Loads and encapsulates an Antigravity conversation transcript."""

    def __init__(self, conv_dir: Path):
        self.conv_dir = conv_dir
        self.conv_id = conv_dir.name
        self.transcript_compact_path = conv_dir / ".system_generated" / "logs" / "transcript.jsonl"
        self.transcript_full_path = conv_dir / ".system_generated" / "logs" / "transcript_full.jsonl"
        self.steps: List[Dict[str, Any]] = []
        self.artifacts: List[Path] = []
        self._load()

    def _load(self):
        if not self.transcript_compact_path.exists():
            raise FileNotFoundError(f"Transcript file not found: {self.transcript_compact_path}")

        # Scan for markdown artifacts in conversation directory
        self.artifacts = [
            f for f in self.conv_dir.iterdir()
            if f.is_file() and f.suffix == ".md" and not f.name.endswith(".metadata.json")
        ]

        # Load steps
        compact_lines: List[Dict[str, Any]] = []
        with open(self.transcript_compact_path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        compact_lines.append(json.loads(line))
                    except Exception:
                        pass

        # Check if full transcript exists for truncated lookups
        full_lines: Dict[int, Dict[str, Any]] = {}
        if self.transcript_full_path.exists():
            with open(self.transcript_full_path, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            item = json.loads(line)
                            idx = item.get("step_index")
                            if idx is not None:
                                full_lines[idx] = item
                        except Exception:
                            pass

        # Resolve full contents when truncated_fields are present
        for step in compact_lines:
            truncated = step.get("truncated_fields") or []
            step_idx = step.get("step_index")
            if truncated and step_idx in full_lines:
                full_item = full_lines[step_idx]
                for field in truncated:
                    if field in full_item:
                        step[field] = full_item[field]
            self.steps.append(step)

    @property
    def start_time(self) -> Optional[str]:
        for s in self.steps:
            if s.get("created_at"):
                return s["created_at"]
        return None

    @property
    def end_time(self) -> Optional[str]:
        for s in reversed(self.steps):
            if s.get("created_at"):
                return s["created_at"]
        return None

    def get_turns(self) -> List[Dict[str, Any]]:
        """
        Groups steps into logical dialogue turns.
        Each turn begins with a USER_INPUT step.
        """
        turns: List[Dict[str, Any]] = []
        current_turn: Optional[Dict[str, Any]] = None

        for step in self.steps:
            stype = step.get("type")
            source = step.get("source")
            content = step.get("content", "")
            tool_calls = step.get("tool_calls") or []

            if stype == "USER_INPUT":
                if current_turn:
                    turns.append(current_turn)
                clean_user = clean_prompt_text(content)
                current_turn = {
                    "turn_index": len(turns) + 1,
                    "step_index": step.get("step_index"),
                    "created_at": step.get("created_at", ""),
                    "user_text": clean_user,
                    "assistant_text": "",
                    "tool_calls": [],
                    "tool_results": [],
                }
            elif current_turn is not None:
                if stype == "PLANNER_RESPONSE":
                    if content and not current_turn["assistant_text"]:
                        current_turn["assistant_text"] = content.strip()
                    elif content:
                        current_turn["assistant_text"] += "\n\n" + content.strip()
                    if tool_calls:
                        for tc in tool_calls:
                            current_turn["tool_calls"].append(tc)
                elif stype == "GENERIC" and source == "MODEL":
                    if content:
                        current_turn["tool_results"].append(content.strip())

        if current_turn:
            turns.append(current_turn)

        return turns

    def get_tool_statistics(self) -> Dict[str, int]:
        """Calculates frequency of tool calls."""
        stats: Dict[str, int] = {}
        for step in self.steps:
            for tc in step.get("tool_calls") or []:
                name = tc.get("name", "unknown")
                stats[name] = stats.get(name, 0) + 1
        return dict(sorted(stats.items(), key=lambda kv: kv[1], reverse=True))

    def get_summary(self) -> Dict[str, Any]:
        """Generates a bird's-eye executive summary of the conversation."""
        turns = self.get_turns()
        first_prompt = turns[0]["user_text"] if turns else "No prompt recorded"
        # First 120 chars for title
        title = first_prompt.split("\n")[0][:120].strip() or f"Conversation {self.conv_id[:8]}"

        last_assistant_resp = ""
        for t in reversed(turns):
            if t.get("assistant_text"):
                last_assistant_resp = t["assistant_text"]
                break

        return {
            "conversation_id": self.conv_id,
            "title": title,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "total_steps": len(self.steps),
            "total_turns": len(turns),
            "tool_stats": self.get_tool_statistics(),
            "artifacts": [a.name for a in self.artifacts],
            "first_prompt": first_prompt,
            "final_response": last_assistant_resp,
            "milestone_prompts": [
                {"turn": t["turn_index"], "created_at": t["created_at"], "prompt": t["user_text"][:160]}
                for t in turns
            ],
        }


def print_summary(transcript: ConversationTranscript):
    """Outputs high-level bird's-eye summary to stdout."""
    summary = transcript.get_summary()
    print("=" * 80)
    print(f"  🦅 BIRD'S-EYE VIEW: Antigravity Session {summary['conversation_id']}")
    print("=" * 80)
    print(f"- Title:        {summary['title']}")
    print(f"- Started:      {summary['start_time']}")
    print(f"- Ended:        {summary['end_time']}")
    print(f"- Total Turns:  {summary['total_turns']} user interactions ({summary['total_steps']} total execution steps)")

    stats = summary["tool_stats"]
    total_tools = sum(stats.values())
    print(f"- Tools Run:    {total_tools} calls across {len(stats)} distinct tool types")
    if stats:
        tool_str = ", ".join(f"{k}: {v}" for k, v in list(stats.items())[:6])
        print(f"  ↳ ({tool_str})")

    if summary["artifacts"]:
        art_str = ", ".join(summary["artifacts"])
        print(f"- Artifacts:    {art_str}")

    print("\n--- 🧭 PROGRESSIVE USER MILESTONES ---")
    for m in summary["milestone_prompts"]:
        ts = m["created_at"][:19].replace("T", " ") if m["created_at"] else ""
        print(f"[{m['turn']:2d}] ({ts}) {m['prompt']}")

    print("\n--- 🏁 FINAL DELIVERABLE PREVIEW ---")
    final_text = summary["final_response"]
    if final_text:
        preview_lines = final_text.splitlines()[:15]
        print("\n".join(preview_lines))
        if len(final_text.splitlines()) > 15:
            print("  ... [truncated, run `read-chat --last 1` to view full final response] ...")
    else:
        print("No final assistant response recorded.")
    print("=" * 80)


def print_user_prompts(transcript: ConversationTranscript):
    """Prints only the user prompts across all turns."""
    turns = transcript.get_turns()
    print(f"User Prompt Log for Session [{transcript.conv_id}] ({len(turns)} turns):")
    print("-" * 80)
    for t in turns:
        ts = t["created_at"][:19].replace("T", " ") if t["created_at"] else ""
        print(f"\n[Turn {t['turn_index']}] {ts}")
        print(t["user_text"])
    print("-" * 80)


def print_turns(
    transcript: ConversationTranscript,
    turns_filter: Optional[List[int]] = None,
    show_tools: bool = False,
):
    """Prints formatted turn-by-turn conversation transcript to stdout."""
    turns = transcript.get_turns()
    if turns_filter:
        turns = [t for t in turns if t["turn_index"] in turns_filter]

    print(f"\nConversation: {transcript.conv_id} ({len(turns)} turns displayed)")
    print("=" * 80)

    for t in turns:
        ts = t["created_at"][:19].replace("T", " ") if t["created_at"] else ""
        print(f"\n## Turn {t['turn_index']}  [{ts}]")
        print("-" * 80)
        print("👤 USER:")
        print(t["user_text"])
        print()

        if t["tool_calls"]:
            if show_tools:
                print("🛠️ TOOLS EXECUTED:")
                for tc in t["tool_calls"]:
                    name = tc.get("name")
                    args = tc.get("args") or {}
                    args_summary = json.dumps(args, ensure_ascii=False)
                    if len(args_summary) > 160:
                        args_summary = args_summary[:160] + "..."
                    print(f"  - {name}: {args_summary}")
                print()
            else:
                tool_names = [tc.get("name", "") for tc in t["tool_calls"]]
                counts = {}
                for tn in tool_names:
                    counts[tn] = counts.get(tn, 0) + 1
                t_summary = ", ".join(f"{k} (x{v})" for k, v in counts.items())
                print(f"🛠️ Tools: {t_summary}\n")

        print("🤖 ASSISTANT:")
        print(t["assistant_text"] or "(No text response emitted)")
        print("-" * 80)


def format_markdown(transcript: ConversationTranscript) -> str:
    """Renders the full conversation as a clean GitHub Flavored Markdown document."""
    summary = transcript.get_summary()
    date_str = datetime.now().strftime("%Y-%m-%d")

    md = [
        f"# Conversation: {summary['title']}\n",
        f"- **Session ID:** `{transcript.conv_id}`",
        f"- **Started:** {summary['start_time']}",
        f"- **Ended:** {summary['end_time']}",
        f"- **Archived Date:** {date_str}",
        f"- **Total Interaction Turns:** {summary['total_turns']}",
        f"- **Total Execution Steps:** {summary['total_steps']}\n",
    ]

    stats = summary["tool_stats"]
    if stats:
        md.append("### Tool Call Summary\n")
        md.append("| Tool Name | Invocation Count |")
        md.append("| :--- | :--- |")
        for k, v in stats.items():
            md.append(f"| `{k}` | {v} |")
        md.append("")

    if transcript.artifacts:
        md.append("### Generated Session Artifacts\n")
        for art in transcript.artifacts:
            md.append(f"- [{art.name}](file:///{art.as_posix()})")
        md.append("")

    md.append("---\n")

    turns = transcript.get_turns()
    for t in turns:
        ts = t["created_at"][:19].replace("T", " ") if t["created_at"] else ""
        md.append(f"## Turn {t['turn_index']} ({ts})\n")
        md.append("### 👤 User\n")
        md.append(f"{t['user_text']}\n")

        if t["tool_calls"]:
            md.append("<details><summary>🛠️ Tool Calls Executed (" + str(len(t['tool_calls'])) + ")</summary>\n")
            md.append("```json")
            md.append(json.dumps(t["tool_calls"], indent=2, ensure_ascii=False))
            md.append("```\n</details>\n")

        md.append("### 🤖 Assistant\n")
        md.append(f"{t['assistant_text']}\n")
        md.append("---\n")

    return "\n".join(md)


def list_conversations(brain_dir: Optional[Path] = None, limit: int = 15):
    """Lists recent conversations stored in the Antigravity brain."""
    if brain_dir is None:
        brain_dir = get_default_brain_dir()

    if not brain_dir.exists():
        print(f"No brain directory found at: {brain_dir}")
        return

    convs = [
        d for d in brain_dir.iterdir()
        if d.is_dir() and (d / ".system_generated" / "logs" / "transcript.jsonl").exists()
    ]
    convs.sort(key=lambda d: d.stat().st_mtime, reverse=True)

    print("=" * 110)
    print(f"  🧠 ANTIGRAVITY BRAIN CONVERSATIONS (Total: {len(convs)} | Showing top {min(limit, len(convs))})")
    print("=" * 110)
    print(f"{'CONVERSATION ID':<38} {'MODIFIED':<19} {'TURNS':<6} {'FIRST PROMPT PREVIEW'}")
    print("-" * 110)

    for d in convs[:limit]:
        mtime = datetime.fromtimestamp(d.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        prompt = ""
        turns_count = 0
        try:
            transcript_file = d / ".system_generated" / "logs" / "transcript.jsonl"
            with open(transcript_file, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    if '"type":"USER_INPUT"' in line:
                        turns_count += 1
                        if not prompt:
                            data = json.loads(line)
                            prompt = clean_prompt_text(data.get("content", "")).splitlines()[0]
        except Exception:
            prompt = "(Could not parse prompt)"

        if len(prompt) > 42:
            prompt = prompt[:39] + "..."
        print(f"{d.name:<38} {mtime:<19} {turns_count:<6} {prompt}")
    print("=" * 110)


def search_conversations(query: str, brain_dir: Optional[Path] = None, limit: int = 10):
    """Searches for keyword or regex matches across all transcripts in the brain."""
    if brain_dir is None:
        brain_dir = get_default_brain_dir()

    if not brain_dir.exists():
        print(f"No brain directory found at: {brain_dir}")
        return

    convs = [
        d for d in brain_dir.iterdir()
        if d.is_dir() and (d / ".system_generated" / "logs" / "transcript.jsonl").exists()
    ]
    convs.sort(key=lambda d: d.stat().st_mtime, reverse=True)

    print(f"\n🔍 Searching {len(convs)} conversations for: '{query}'...")
    print("=" * 100)

    matches_found = 0
    pattern = re.compile(query, re.IGNORECASE)

    for d in convs:
        tfile = d / ".system_generated" / "logs" / "transcript.jsonl"
        try:
            with open(tfile, "r", encoding="utf-8", errors="replace") as f:
                for line_idx, line in enumerate(f, start=1):
                    if pattern.search(line):
                        data = json.loads(line)
                        stype = data.get("type", "")
                        cnt = clean_prompt_text(data.get("content", "")).replace("\n", " ")
                        if len(cnt) > 90:
                            cnt = cnt[:87] + "..."
                        print(f"[{d.name[:8]}] ({stype}): {cnt}")
                        matches_found += 1
                        break
        except Exception:
            pass

        if matches_found >= limit:
            break

    if matches_found == 0:
        print(f"No conversations matching '{query}' found.")
    print("=" * 100)


def resolve_export_directory(specified_dir: str) -> Path:
    """Determines the target directory for saving markdown archives."""
    if specified_dir:
        p = Path(specified_dir)
        p.mkdir(parents=True, exist_ok=True)
        return p

    cwd = Path.cwd()
    if (cwd / "research" / "transcripts").exists():
        return cwd / "research" / "transcripts"
    if (cwd / "docs").exists():
        target = cwd / "docs" / "chat_history"
        target.mkdir(parents=True, exist_ok=True)
        return target

    target = cwd / "chat_history"
    target.mkdir(parents=True, exist_ok=True)
    return target


def main():
    parser = argparse.ArgumentParser(
        description="Antigravity Brain Conversation Reader & Archiver (read-chat)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "conversation",
        nargs="?",
        default=None,
        help="Conversation UUID, prefix (e.g. 2417d518), or path. Use --latest for most recent.",
    )
    parser.add_argument(
        "-l", "--list",
        action="store_true",
        help="List recent conversations stored in ~/.gemini/antigravity/brain",
    )
    parser.add_argument(
        "-q", "--search",
        type=str,
        help="Search across all transcripts for a keyword or pattern",
    )
    parser.add_argument(
        "-s", "--summary",
        action="store_true",
        help="Display bird's-eye session summary, timeline of milestones, and final deliverable",
    )
    parser.add_argument(
        "-u", "--user-only",
        action="store_true",
        help="Display only the user prompts across all interaction turns",
    )
    parser.add_argument(
        "-t", "--turns",
        type=str,
        help="Specific turn or turn range to display (e.g. '1', '1-5', '3,5,7')",
    )
    parser.add_argument(
        "--last",
        type=int,
        help="Display only the last N turns of the conversation",
    )
    parser.add_argument(
        "--tools",
        action="store_true",
        help="Include full tool call arguments and outputs in transcript display",
    )
    parser.add_argument(
        "-e", "--export",
        action="store_true",
        help="Export full conversation to a clean GitHub Flavored Markdown document",
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Custom output file path for markdown export",
    )
    parser.add_argument(
        "--dir",
        type=str,
        default="",
        help="Directory to save exported markdown file",
    )

    args = parser.parse_args()

    if args.list:
        list_conversations()
        return

    if args.search:
        search_conversations(args.search)
        return

    # Resolve target conversation
    if not args.conversation:
        # Default to latest conversation
        conv_dir = find_latest_conversation()
    else:
        conv_dir = resolve_conversation_path(args.conversation)

    transcript = ConversationTranscript(conv_dir)

    # Export mode
    if args.export or args.output:
        md_text = format_markdown(transcript)
        if args.output:
            out_file = Path(args.output)
            out_file.parent.mkdir(parents=True, exist_ok=True)
        else:
            export_dir = resolve_export_directory(args.dir)
            date_prefix = datetime.now().strftime("%Y-%m-%d")
            slug = re.sub(r"[^\w\s-]", "", transcript.conv_id[:8]).strip().lower()
            out_file = export_dir / f"{date_prefix}_AGY_{slug.upper()}_TRANSCRIPT.md"

        out_file.write_text(md_text, encoding="utf-8")
        print(f"Successfully archived Antigravity conversation to: {out_file.resolve()}")
        return

    # Summary mode
    if args.summary:
        print_summary(transcript)
        return

    # User-only mode
    if args.user_only:
        print_user_prompts(transcript)
        return

    # Filter turns
    turns_filter: Optional[List[int]] = None
    all_turns = transcript.get_turns()
    total_turns = len(all_turns)

    if args.last:
        start_idx = max(1, total_turns - args.last + 1)
        turns_filter = list(range(start_idx, total_turns + 1))
    elif args.turns:
        turns_filter = []
        for part in args.turns.split(","):
            part = part.strip()
            if "-" in part:
                p_start, p_end = part.split("-", 1)
                turns_filter.extend(range(int(p_start), int(p_end) + 1))
            else:
                turns_filter.append(int(part))

    # Default: if no specific flags, output bird's-eye summary first if large (>5 turns) or full turns if short
    if not args.turns and not args.last and total_turns > 10:
        # For long conversations, show the summary and instruct on turns
        print_summary(transcript)
        print(f"\n💡 Tip: Run `read-chat {transcript.conv_id[:8]} --turns 1-5` or `read-chat {transcript.conv_id[:8]} --last 3` to view specific turns.")
        print(f"💡 Tip: Run `read-chat {transcript.conv_id[:8]} --export` to save full markdown to disk.")
    else:
        print_turns(transcript, turns_filter=turns_filter, show_tools=args.tools)


if __name__ == "__main__":
    main()
