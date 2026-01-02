#!/usr/bin/env python3
"""
Extract all missing tools from Ch7 stats validation reports
"""
import re
from pathlib import Path
from collections import defaultdict

ch7_dir = Path("/home/etai/projects/REMEMVR/results/ch7")
missing_tools = defaultdict(set)

# Pattern to find tool specifications
tool_patterns = [
    r'tools\.[a-z_]+\.[a-z_]+',  # tools.module.function format
    r'Missing.*?tools.*?:.*?\n(.*?)\n',  # Missing tools sections
    r'Tool Name:.*?`(.*?)`',  # Tool name specifications
]

for rq_dir in sorted(ch7_dir.iterdir()):
    if rq_dir.is_dir():
        stats_file = rq_dir / "docs" / "1_stats.md"
        if stats_file.exists():
            try:
                content = stats_file.read_text(encoding='utf-8', errors='ignore')
                
                # Find all tool references
                for pattern in tool_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE)
                    for match in matches:
                        if 'tools.' in str(match):
                            missing_tools[rq_dir.name].add(match)
                
                # Look for specific missing tool descriptions
                if "Missing Tools" in content or "Missing tools" in content:
                    # Extract the section
                    section = re.search(r'Missing [Tt]ools.*?\n\n', content, re.DOTALL)
                    if section:
                        # Extract tool names from the section
                        tools_in_section = re.findall(r'`(tools\.[^`]+)`', section.group())
                        for tool in tools_in_section:
                            missing_tools[rq_dir.name].add(tool)
                            
            except Exception as e:
                print(f"Error reading {rq_dir.name}: {e}")

# Aggregate all unique tools
all_tools = set()
for rq, tools in missing_tools.items():
    all_tools.update(tools)

# Categorize by module
modules = defaultdict(list)
for tool in sorted(all_tools):
    if 'tools.' in tool:
        parts = tool.split('.')
        if len(parts) >= 3:
            module = f"{parts[0]}.{parts[1]}"
            function = '.'.join(parts[2:])
            modules[module].append(function)

print("Missing Tools for Ch7 by Module:")
print("=" * 60)
for module in sorted(modules.keys()):
    print(f"\n{module}:")
    for func in sorted(modules[module]):
        print(f"  - {func}")

print("\n" + "=" * 60)
print(f"Total unique missing tools: {len(all_tools)}")
print(f"Affected RQs: {len(missing_tools)}")

# Also look for tool availability percentages to understand scope
print("\n" + "=" * 60)
print("Tool Reuse Rates by RQ (from stats reports):")
for rq_dir in sorted(ch7_dir.iterdir()):
    if rq_dir.is_dir():
        stats_file = rq_dir / "docs" / "1_stats.md"
        if stats_file.exists():
            try:
                content = stats_file.read_text(encoding='utf-8', errors='ignore')
                # Look for tool reuse rate
                rate_match = re.search(r'Tool [Rr]euse [Rr]ate.*?(\d+)%', content)
                if rate_match:
                    rate = rate_match.group(1)
                    status = "❌" if int(rate) < 50 else "⚠️" if int(rate) < 80 else "✅"
                    print(f"  {rq_dir.name}: {rate}% {status}")
            except:
                pass