#!/usr/bin/env python3
"""
Search past Claude Code conversations for previously solved problems.

Usage:
    search_history.py <query> [--project <path>] [--limit <n>] [--format json|text]
    search_history.py --digest [today|yesterday|YYYY-MM-DD] [--project <path>]

Examples:
    search_history.py "EMFILE error"
    search_history.py "vitest browser mode" --limit 5
    search_history.py "nuxt content" --project ~/Projects/nuxt/secondBrain
    search_history.py --today "newsletter"
    search_history.py --days 3 "fix bug"
    search_history.py --digest today --project ~/Projects/nuxt/secondBrain
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional


@dataclass
class Message:
    """Represents a single message in a conversation."""
    uuid: str
    parent_uuid: Optional[str]
    role: str  # 'user', 'assistant'
    content: str
    timestamp: str
    tool_uses: list
    tool_results: list


@dataclass
class Conversation:
    """Represents a full conversation session."""
    session_id: str
    file_path: str
    summary: Optional[str]
    messages: list
    project_path: str
    git_branch: Optional[str]
    timestamp: str


@dataclass
class SearchResult:
    """A search result with relevance score."""
    conversation: Conversation
    score: float
    matched_messages: list
    problem_excerpt: str
    solution_excerpt: str
    commands_run: list


def get_claude_projects_dir() -> Path:
    """Get the Claude projects directory."""
    return Path.home() / '.claude' / 'projects'


def decode_project_path(encoded: str) -> str:
    """Decode encoded project path."""
    if encoded.startswith('-'):
        return '/' + encoded[1:].replace('-', '/')
    return encoded.replace('-', '/')


def encode_project_path(path: str) -> str:
    """Encode project path for directory name."""
    if path.startswith('/'):
        path = path[1:]
    return '-' + path.replace('/', '-')


def get_project_dirs(specific_project: Optional[str] = None) -> list:
    """Get all project directories or a specific one."""
    projects_dir = get_claude_projects_dir()

    if not projects_dir.exists():
        return []

    if specific_project:
        # Normalize path
        specific_project = str(Path(specific_project).expanduser().resolve())
        encoded = encode_project_path(specific_project)
        project_dir = projects_dir / encoded
        if project_dir.exists():
            return [project_dir]
        # Try partial match
        for d in projects_dir.iterdir():
            if d.is_dir() and encoded in d.name:
                return [d]
        return []

    return [d for d in projects_dir.iterdir() if d.is_dir()]


def extract_text_content(content) -> str:
    """Extract plain text from message content."""
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        texts = []
        for block in content:
            if isinstance(block, dict):
                if block.get('type') == 'text':
                    texts.append(block.get('text', ''))
                elif block.get('type') == 'thinking':
                    texts.append(block.get('thinking', ''))
        return '\n'.join(texts)

    return ''


def extract_tool_uses(content) -> list:
    """Extract tool_use blocks from message content."""
    if not isinstance(content, list):
        return []

    return [
        {'name': block.get('name'), 'input': block.get('input', {})}
        for block in content
        if isinstance(block, dict) and block.get('type') == 'tool_use'
    ]


def extract_tool_results(content) -> list:
    """Extract tool_result blocks from message content."""
    if not isinstance(content, list):
        return []

    results = []
    for block in content:
        if isinstance(block, dict) and block.get('type') == 'tool_result':
            result_content = block.get('content', '')
            if isinstance(result_content, str):
                results.append({'content': result_content})
            elif isinstance(result_content, list):
                # Extract text from content blocks
                text_parts = []
                for item in result_content:
                    if isinstance(item, dict) and item.get('type') == 'text':
                        text_parts.append(item.get('text', ''))
                results.append({'content': '\n'.join(text_parts)})
    return results


def parse_timestamp(timestamp: str) -> Optional[datetime]:
    """Parse ISO timestamp string to datetime."""
    if not timestamp:
        return None
    try:
        # Handle various ISO formats
        if 'T' in timestamp:
            # Remove timezone info for simplicity
            timestamp = timestamp.split('+')[0].split('Z')[0]
            if '.' in timestamp:
                return datetime.strptime(timestamp[:26], '%Y-%m-%dT%H:%M:%S.%f')
            return datetime.strptime(timestamp[:19], '%Y-%m-%dT%H:%M:%S')
        return datetime.strptime(timestamp[:10], '%Y-%m-%d')
    except (ValueError, IndexError):
        return None


def get_date_filter(args) -> Optional[tuple]:
    """
    Get date filter range based on args.
    Returns (start_date, end_date) or None if no filter.
    """
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    if args.today:
        return (today, today + timedelta(days=1))

    if args.yesterday:
        yesterday = today - timedelta(days=1)
        return (yesterday, today)

    if args.days:
        start = today - timedelta(days=args.days - 1)
        return (start, today + timedelta(days=1))

    if args.since:
        try:
            start = datetime.strptime(args.since, '%Y-%m-%d')
            return (start, today + timedelta(days=1))
        except ValueError:
            print(f"Invalid date format: {args.since}. Use YYYY-MM-DD", file=sys.stderr)
            sys.exit(1)

    return None


def conversation_in_date_range(conversation: Conversation, date_range: tuple) -> bool:
    """Check if conversation falls within date range."""
    if not date_range:
        return True

    start, end = date_range
    conv_date = parse_timestamp(conversation.timestamp)

    if conv_date is None:
        return False

    return start <= conv_date < end


def parse_conversation_file(file_path: Path) -> Optional[Conversation]:
    """Parse a JSONL conversation file into a Conversation object."""
    messages = []
    summary = None
    session_id = file_path.stem
    project_path = decode_project_path(file_path.parent.name)
    git_branch = None
    first_timestamp = None

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue

                entry_type = entry.get('type')

                if entry_type == 'summary':
                    summary = entry.get('summary')
                    continue

                if entry_type not in ('user', 'assistant'):
                    continue

                if git_branch is None:
                    git_branch = entry.get('gitBranch')

                timestamp = entry.get('timestamp', '')
                if first_timestamp is None:
                    first_timestamp = timestamp

                msg_data = entry.get('message', {})
                content = msg_data.get('content', '')

                message = Message(
                    uuid=entry.get('uuid', ''),
                    parent_uuid=entry.get('parentUuid'),
                    role=entry_type,
                    content=extract_text_content(content),
                    timestamp=timestamp,
                    tool_uses=extract_tool_uses(content),
                    tool_results=extract_tool_results(content)
                )
                messages.append(message)

    except Exception as e:
        print(f"Error parsing {file_path.name}: {e}", file=sys.stderr)
        return None

    if not messages:
        return None

    return Conversation(
        session_id=session_id,
        file_path=str(file_path),
        summary=summary,
        messages=messages,
        project_path=project_path,
        git_branch=git_branch,
        timestamp=first_timestamp or ''
    )


def tokenize(text: str) -> set:
    """Tokenize text into lowercase words."""
    return set(re.findall(r'\b\w+\b', text.lower()))


def calculate_relevance_score(query: str, conversation: Conversation) -> tuple:
    """Calculate relevance score for a conversation."""
    query_tokens = tokenize(query)
    if not query_tokens:
        return 0.0, []

    total_score = 0.0
    matched_messages = []

    # Check summary (high weight)
    if conversation.summary:
        summary_tokens = tokenize(conversation.summary)
        summary_overlap = len(query_tokens & summary_tokens) / len(query_tokens)
        total_score += summary_overlap * 3.0

    # Check messages
    for msg in conversation.messages:
        msg_tokens = tokenize(msg.content)
        overlap = len(query_tokens & msg_tokens)

        if overlap > 0:
            msg_score = overlap / len(query_tokens)

            # Boost user messages (problem descriptions)
            if msg.role == 'user':
                msg_score *= 1.5

            # Boost messages with tool uses (solutions)
            if msg.tool_uses:
                msg_score *= 1.3

            total_score += msg_score
            matched_messages.append(msg)

    return total_score, matched_messages


def extract_bash_commands(conversation: Conversation) -> list:
    """Extract Bash commands run during the conversation."""
    commands = []
    for msg in conversation.messages:
        for tool in msg.tool_uses:
            if tool.get('name') == 'Bash':
                cmd = tool.get('input', {}).get('command', '')
                if cmd:
                    commands.append(cmd)
    return commands


def extract_files_touched(conversation: Conversation) -> list:
    """Extract files that were read, written, or edited."""
    files = set()
    for msg in conversation.messages:
        for tool in msg.tool_uses:
            name = tool.get('name', '')
            inp = tool.get('input', {})

            if name in ('Read', 'Write', 'Edit'):
                path = inp.get('file_path', '')
                if path:
                    # Shorten path for display
                    files.add(Path(path).name)
            elif name == 'Glob':
                pattern = inp.get('pattern', '')
                if pattern:
                    files.add(f"glob:{pattern}")

    return sorted(files)[:10]  # Limit to 10 files


def extract_problem_excerpt(conversation: Conversation) -> str:
    """Extract a brief problem description from the conversation."""
    if conversation.summary:
        return conversation.summary

    for msg in conversation.messages:
        if msg.role == 'user' and msg.content:
            content = msg.content.strip()
            # Skip tool results
            if content.startswith('[') or content.startswith('{'):
                continue
            if len(content) > 200:
                return content[:200] + '...'
            return content

    return 'No problem description found'


def extract_solution_excerpt(matched_messages: list) -> str:
    """Extract a brief solution description from matched messages."""
    for msg in reversed(matched_messages):
        if msg.role == 'assistant' and msg.content:
            content = msg.content.strip()
            if len(content) > 300:
                return content[:300] + '...'
            return content
    return 'No solution found'


def extract_topics(conversation: Conversation) -> list:
    """Extract key topics from conversation."""
    topics = set()

    # Look for common patterns in first user message
    for msg in conversation.messages[:3]:
        if msg.role == 'user':
            content = msg.content.lower()

            # Extract quoted terms
            quoted = re.findall(r'"([^"]+)"', content)
            topics.update(quoted[:3])

            # Extract key action words
            if 'add' in content:
                topics.add('adding')
            if 'fix' in content:
                topics.add('fixing')
            if 'implement' in content:
                topics.add('implementing')
            if 'refactor' in content:
                topics.add('refactoring')
            if 'test' in content:
                topics.add('testing')
            if 'debug' in content:
                topics.add('debugging')

            break

    return list(topics)[:5]


def search_conversations(
    query: str,
    project_path: Optional[str] = None,
    limit: int = 10,
    date_filter: Optional[tuple] = None
) -> list:
    """Search conversations for the given query."""
    results = []
    project_dirs = get_project_dirs(project_path)

    for project_dir in project_dirs:
        for jsonl_file in project_dir.glob('*.jsonl'):
            # Skip agent files
            if jsonl_file.name.startswith('agent-'):
                continue

            conversation = parse_conversation_file(jsonl_file)
            if conversation is None:
                continue

            # Apply date filter
            if not conversation_in_date_range(conversation, date_filter):
                continue

            score, matched = calculate_relevance_score(query, conversation)
            if score > 0:
                results.append(SearchResult(
                    conversation=conversation,
                    score=score,
                    matched_messages=matched,
                    problem_excerpt=extract_problem_excerpt(conversation),
                    solution_excerpt=extract_solution_excerpt(matched),
                    commands_run=extract_bash_commands(conversation)
                ))

    results.sort(key=lambda r: r.score, reverse=True)
    return results[:limit]


def get_conversations_for_date(
    target_date: datetime,
    project_path: Optional[str] = None
) -> list:
    """Get all conversations for a specific date."""
    conversations = []
    project_dirs = get_project_dirs(project_path)

    start = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)

    for project_dir in project_dirs:
        for jsonl_file in project_dir.glob('*.jsonl'):
            if jsonl_file.name.startswith('agent-'):
                continue

            conversation = parse_conversation_file(jsonl_file)
            if conversation is None:
                continue

            if conversation_in_date_range(conversation, (start, end)):
                conversations.append(conversation)

    # Sort by timestamp
    conversations.sort(key=lambda c: c.timestamp)
    return conversations


def format_digest(conversations: list, target_date: datetime, project_filter: Optional[str]) -> str:
    """Format a daily digest of conversations."""
    date_str = target_date.strftime('%B %d, %Y')

    if not conversations:
        return f"## {date_str} - No sessions found\n"

    lines = [
        f"## {date_str} - {len(conversations)} session{'s' if len(conversations) != 1 else ''}",
        ""
    ]

    for i, conv in enumerate(conversations, 1):
        problem = extract_problem_excerpt(conv)
        commands = extract_bash_commands(conv)
        files = extract_files_touched(conv)

        # Create a title from the problem excerpt
        title = problem[:60].replace('\n', ' ')
        if len(problem) > 60:
            title += '...'

        lines.append(f"### {i}. {title}")
        lines.append(f"   Session: `{conv.session_id[:8]}`")

        if conv.git_branch:
            lines.append(f"   Branch: `{conv.git_branch}`")

        if files:
            lines.append(f"   Files: {', '.join(files[:5])}")

        if commands:
            lines.append(f"   Commands: {len(commands)} executed")

        lines.append("")

    return '\n'.join(lines)


def parse_digest_date(date_arg: str) -> datetime:
    """Parse digest date argument."""
    today = datetime.now()

    if date_arg == 'today':
        return today
    elif date_arg == 'yesterday':
        return today - timedelta(days=1)
    else:
        try:
            return datetime.strptime(date_arg, '%Y-%m-%d')
        except ValueError:
            print(f"Invalid date: {date_arg}. Use 'today', 'yesterday', or YYYY-MM-DD", file=sys.stderr)
            sys.exit(1)


def format_result_text(result: SearchResult, index: int) -> str:
    """Format a search result for text output."""
    lines = [
        f"\n{'='*60}",
        f"Result #{index + 1} (Score: {result.score:.2f})",
        f"{'='*60}",
        f"Project: {result.conversation.project_path}",
        f"Session: {result.conversation.session_id[:8]}...",
        f"Branch: {result.conversation.git_branch or 'N/A'}",
        f"Date: {result.conversation.timestamp[:10] if result.conversation.timestamp else 'N/A'}",
        "",
        "PROBLEM:",
        result.problem_excerpt,
        "",
        "SOLUTION:",
        result.solution_excerpt,
    ]

    if result.commands_run:
        lines.extend([
            "",
            f"COMMANDS RUN ({len(result.commands_run)} total):",
            *[f"  $ {cmd[:80]}{'...' if len(cmd) > 80 else ''}"
              for cmd in result.commands_run[:5]]
        ])
        if len(result.commands_run) > 5:
            lines.append(f"  ... and {len(result.commands_run) - 5} more")

    return '\n'.join(lines)


def format_result_json(result: SearchResult) -> dict:
    """Format a search result for JSON output."""
    return {
        'score': result.score,
        'session_id': result.conversation.session_id,
        'project': result.conversation.project_path,
        'git_branch': result.conversation.git_branch,
        'timestamp': result.conversation.timestamp,
        'summary': result.conversation.summary,
        'problem': result.problem_excerpt,
        'solution': result.solution_excerpt,
        'commands': result.commands_run[:10],
        'file_path': result.conversation.file_path
    }


def main():
    parser = argparse.ArgumentParser(
        description='Search past Claude Code conversations',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Basic search
    search_history.py "EMFILE error"
    search_history.py "vitest browser mode" --limit 5

    # Search with date filters
    search_history.py --today "newsletter"
    search_history.py --yesterday "bug fix"
    search_history.py --days 7 "refactor"
    search_history.py --since 2026-01-01 "feature"

    # Daily digest (what did we do today?)
    search_history.py --digest today
    search_history.py --digest yesterday --project ~/Projects/myapp
    search_history.py --digest 2026-01-04
        """
    )

    parser.add_argument('query', nargs='?', help='Search query (optional with --digest)')
    parser.add_argument('--project', '-p', help='Specific project path to search')
    parser.add_argument('--limit', '-l', type=int, default=5, help='Max results (default: 5)')
    parser.add_argument('--format', '-f', choices=['text', 'json'], default='text',
                       help='Output format (default: text)')

    # Temporal filters
    parser.add_argument('--today', action='store_true', help='Only sessions from today')
    parser.add_argument('--yesterday', action='store_true', help='Only sessions from yesterday')
    parser.add_argument('--days', type=int, metavar='N', help='Sessions from last N days')
    parser.add_argument('--since', metavar='YYYY-MM-DD', help='Sessions since date')

    # Digest mode
    parser.add_argument('--digest', nargs='?', const='today', metavar='DATE',
                       help='Show daily digest (today, yesterday, or YYYY-MM-DD)')

    args = parser.parse_args()

    # Handle digest mode
    if args.digest is not None:
        target_date = parse_digest_date(args.digest)
        conversations = get_conversations_for_date(target_date, args.project)

        if args.format == 'json':
            output = {
                'date': target_date.strftime('%Y-%m-%d'),
                'session_count': len(conversations),
                'sessions': [
                    {
                        'session_id': c.session_id,
                        'project': c.project_path,
                        'branch': c.git_branch,
                        'timestamp': c.timestamp,
                        'problem': extract_problem_excerpt(c),
                        'commands_count': len(extract_bash_commands(c)),
                        'files': extract_files_touched(c)
                    }
                    for c in conversations
                ]
            }
            print(json.dumps(output, indent=2))
        else:
            print(format_digest(conversations, target_date, args.project))

        sys.exit(0)

    # Regular search mode - require query
    if not args.query:
        parser.error("query is required (unless using --digest)")

    # Get date filter
    date_filter = get_date_filter(args)

    results = search_conversations(
        query=args.query,
        project_path=args.project,
        limit=args.limit,
        date_filter=date_filter
    )

    if not results:
        date_desc = ""
        if args.today:
            date_desc = " from today"
        elif args.yesterday:
            date_desc = " from yesterday"
        elif args.days:
            date_desc = f" from the last {args.days} days"
        elif args.since:
            date_desc = f" since {args.since}"

        print(f"No conversations found{date_desc} matching: {args.query}", file=sys.stderr)
        sys.exit(1)

    if args.format == 'json':
        output = {
            'query': args.query,
            'total_results': len(results),
            'results': [format_result_json(r) for r in results]
        }
        print(json.dumps(output, indent=2))
    else:
        date_desc = ""
        if args.today:
            date_desc = " (today only)"
        elif args.yesterday:
            date_desc = " (yesterday only)"
        elif args.days:
            date_desc = f" (last {args.days} days)"
        elif args.since:
            date_desc = f" (since {args.since})"

        print(f"\nFound {len(results)} relevant conversations for: '{args.query}'{date_desc}\n")
        for i, result in enumerate(results):
            print(format_result_text(result, i))

    sys.exit(0)


if __name__ == '__main__':
    main()
