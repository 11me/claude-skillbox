#!/usr/bin/env python3
"""
Memory Validator - Validates .serena/memories consistency with codebase.

Detects:
- References to non-existent files/directories
- References to deleted skills
- Stale cross-references between memories

Usage:
    python3 memory_validator.py                    # Validate all memories
    python3 memory_validator.py --json             # JSON output for hooks
    python3 memory_validator.py --quiet            # Only output if issues found

Exit codes:
    0 - All memories valid (or no memories exist)
    1 - Stale references found
    2 - Error during validation
"""

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class StaleReference:
    """A stale reference found in a memory file."""

    memory_file: str
    reference: str
    reference_type: str  # 'path', 'skill', 'memory'
    line_number: int
    context: str = ""


@dataclass
class ValidationResult:
    """Result of memory validation."""

    total_memories: int = 0
    valid_memories: int = 0
    stale_references: list[StaleReference] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return len(self.stale_references) == 0


def get_project_root() -> Path | None:
    """Find project root (directory containing .serena or .git)."""
    current = Path.cwd()

    for parent in [current, *current.parents]:
        if (parent / ".serena").exists() or (parent / ".git").exists():
            return parent

    return None


def discover_skills(project_root: Path) -> set[str]:
    """Discover skills from skillbox plugin structure."""
    skills = set()

    # Pattern: plugins/*/skills/*/SKILL.md
    plugins_dir = project_root / "plugins"
    if not plugins_dir.exists():
        return skills

    for skill_md in plugins_dir.glob("*/skills/*/SKILL.md"):
        # Extract skill name from path like plugins/core/skills/beads-workflow/SKILL.md
        skill_name = skill_md.parent.name
        skills.add(skill_name)

    return skills


def load_memories(project_root: Path) -> list[tuple[Path, str]]:
    """Load all memory files."""
    memories_dir = project_root / ".serena" / "memories"
    if not memories_dir.exists():
        return []

    memories = []
    for md_file in memories_dir.glob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8")
            memories.append((md_file, content))
        except Exception:
            continue

    return memories


def extract_references(content: str) -> list[tuple[str, str, int]]:
    """
    Extract references from memory content.

    Returns: List of (reference, type, line_number)
    """
    refs = []
    lines = content.split("\n")

    # Patterns to skip (not filesystem paths)
    skip_patterns = [
        r"^https?://",  # URLs
        r"^\$",  # Variables
        r"^/\w+$",  # Slash commands like /task, /commit
        r"^\w+\.\w+\.\w+/",  # Go modules: github.com/..., go.uber.org/...
        r"^[a-z]+-[a-z]+/[a-z]",  # Go packages: go-resty/resty
        r"^[a-z]+/[a-z]+$",  # Simple package paths: log/slog, net/http
        r"^google/",  # Google packages
        r"^uber-go/",  # Uber packages
        r"^errors\.",  # errors.Is/As
        r"YYYY",  # Date templates (checkpoint-YYYY-MM-DD.md)
        r"^\d+\.\d+",  # Version numbers
        r"^~",  # Home directory paths (external)
        r"^\.claude/",  # User's .claude directory (not in project)
        r"^mcp__",  # MCP tool names
    ]

    def should_skip(ref: str) -> bool:
        for pattern in skip_patterns:
            if pattern.startswith("^") or pattern.startswith(r"\d"):
                if re.match(pattern, ref, re.IGNORECASE):
                    return True
            else:
                if re.search(pattern, ref, re.IGNORECASE):
                    return True
        return False

    in_code_block = False

    for line_num, line in enumerate(lines, 1):
        # Track code blocks
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue

        # Skip content inside code blocks
        if in_code_block:
            continue

        # Path references: `path/to/file.md`, `./skill-name/`
        path_matches = re.findall(r"`(\.?\.?/?[a-zA-Z_][a-zA-Z0-9_-]*(?:/[a-zA-Z0-9_.-]+)+)`", line)
        for match in path_matches:
            if should_skip(match):
                continue
            # Only validate paths that look like project structure
            if any(
                marker in match
                for marker in [
                    ".md",
                    ".py",
                    ".json",
                    ".sh",
                    ".yaml",
                    ".yml",
                    "SKILL",
                    "AGENT",
                    ".claude",
                    ".serena",
                    "plugins/",
                    "scripts/",
                    "hooks/",
                ]
            ):
                refs.append((match, "path", line_num))

        # Skill references in markdown links: [skill-name](./skill-name)
        skill_link_matches = re.findall(r"\[([a-z][a-z0-9-]*)\]\(\./([a-z][a-z0-9-]*)\)", line)
        for name, path in skill_link_matches:
            refs.append((path, "skill", line_num))

        # Direct skill mentions: `skill-name/SKILL.md`
        skill_matches = re.findall(r"`([a-z][a-z0-9-]+)/SKILL\.md`", line)
        for match in skill_matches:
            refs.append((match, "skill", line_num))

        # Memory references: read_memory('name.md')
        memory_matches = re.findall(r"read_memory\(['\"]([^'\"]+)['\"]\)", line)
        for match in memory_matches:
            if not should_skip(match):
                refs.append((match, "memory", line_num))

    return refs


def validate_reference(
    ref: str, ref_type: str, project_root: Path, skills: set[str], memories_dir: Path
) -> bool:
    """Check if a reference is valid."""
    if ref_type == "skill":
        return ref in skills

    if ref_type == "memory":
        return (memories_dir / ref).exists()

    if ref_type == "path":
        # Clean up the path
        clean_ref = ref
        if clean_ref.startswith("./"):
            clean_ref = clean_ref[2:]

        # Check if it's a skill directory reference
        if clean_ref.endswith("/") or "/" not in clean_ref:
            skill_name = clean_ref.rstrip("/")
            if skill_name in skills:
                return True

        # Check filesystem
        full_path = project_root / clean_ref
        return full_path.exists()

    return True


def validate_memories(project_root: Path | None = None) -> ValidationResult:
    """Validate all memories and return results."""
    if project_root is None:
        project_root = get_project_root()

    if project_root is None:
        return ValidationResult()

    result = ValidationResult()
    skills = discover_skills(project_root)
    memories = load_memories(project_root)
    memories_dir = project_root / ".serena" / "memories"

    result.total_memories = len(memories)

    for memory_path, content in memories:
        memory_name = memory_path.name
        has_stale = False

        refs = extract_references(content)
        lines = content.split("\n")

        for ref, ref_type, line_num in refs:
            if not validate_reference(ref, ref_type, project_root, skills, memories_dir):
                has_stale = True
                context = lines[line_num - 1] if line_num <= len(lines) else ""
                result.stale_references.append(
                    StaleReference(
                        memory_file=memory_name,
                        reference=ref,
                        reference_type=ref_type,
                        line_number=line_num,
                        context=context[:100],
                    )
                )

        if not has_stale:
            result.valid_memories += 1

    return result


def format_report(result: ValidationResult) -> str:
    """Format validation result as human-readable report."""
    if result.is_valid:
        if result.total_memories == 0:
            return ""  # No memories, no output
        return f"✓ All {result.total_memories} memories are valid"

    lines = [
        f"## ⚠️ Memory Validation: {len(result.stale_references)} stale reference(s)",
        "",
    ]

    # Group by memory file
    by_file: dict[str, list[StaleReference]] = {}
    for ref in result.stale_references:
        by_file.setdefault(ref.memory_file, []).append(ref)

    for memory_file, refs in by_file.items():
        lines.append(f"**{memory_file}:**")
        for ref in refs:
            lines.append(f"  - Line {ref.line_number}: `{ref.reference}` ({ref.reference_type})")
        lines.append("")

    lines.append("*Run `/checkpoint` after fixing to update memories.*")

    return "\n".join(lines)


def format_json(result: ValidationResult) -> str:
    """Format validation result as JSON."""
    return json.dumps(
        {
            "valid": result.is_valid,
            "total_memories": result.total_memories,
            "valid_memories": result.valid_memories,
            "stale_count": len(result.stale_references),
            "stale_references": [
                {
                    "file": r.memory_file,
                    "reference": r.reference,
                    "type": r.reference_type,
                    "line": r.line_number,
                }
                for r in result.stale_references
            ],
        },
        indent=2,
    )


def main():
    """Main entry point."""
    import argparse

    # Add lib to path for session_output
    sys.path.insert(0, str(Path(__file__).parent))
    from lib.response import session_output

    parser = argparse.ArgumentParser(description="Validate memory consistency")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--quiet", action="store_true", help="Only output if issues found")
    args = parser.parse_args()

    try:
        project_root = get_project_root()
        result = validate_memories(project_root)

        if args.quiet and result.is_valid:
            sys.exit(0)

        if args.json:
            output = format_json(result)
            print(output)
        else:
            output = format_report(result)
            if output:
                # Use session_output for proper hook formatting
                session_output(output)

        sys.exit(0 if result.is_valid else 1)

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
