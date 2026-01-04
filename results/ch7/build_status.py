#!/usr/bin/env python3
"""Build comprehensive Ch7 RQ status table."""

import os
import re
import csv
from pathlib import Path

def extract_question(concept_file):
    """Extract research question from concept file."""
    if not os.path.exists(concept_file):
        return "NO_CONCEPT_FILE"
    
    with open(concept_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        
    # Look for the primary question after "Primary Question:" marker
    in_question = False
    for i, line in enumerate(lines):
        if "Primary Question:" in line:
            in_question = True
            continue
        if in_question and line.strip():
            return line.strip()
    
    return "QUESTION_NOT_FOUND"

def extract_score(validation_file):
    """Extract score from validation file (1_scholar.md or 1_stats.md)."""
    if not os.path.exists(validation_file):
        return "N/A"
    
    with open(validation_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Look for score patterns like "9.5/10" or "Score: 9.5/10"
    patterns = [
        r'Score:\s*(\d+(?:\.\d+)?)/10',
        r'Final Score:\s*(\d+(?:\.\d+)?)/10',
        r'(\d+(?:\.\d+)?)/10\s*(?:APPROVED|CONDITIONAL|REJECTED)',
        r'(?:APPROVED|CONDITIONAL|REJECTED).*?(\d+(?:\.\d+)?)/10'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            return float(match.group(1))
    
    return "N/A"

def check_file_exists(file_path):
    """Check if a file exists."""
    return "Y" if os.path.exists(file_path) else "N"

def get_tools_status(rq_dir):
    """Get rq_tools status."""
    tools_file = os.path.join(rq_dir, "docs", "3_tools.yaml")
    if os.path.exists(tools_file):
        return "pass"
    
    # Check if it failed (we ran it but no file created)
    if rq_dir.name in ["7.1.2", "7.1.3"]:
        if rq_dir.name == "7.1.2":
            return "fail-missing-tools"
        else:
            return "fail-no-plan"
    
    return "TBD"

def get_analysis_status(rq_dir):
    """Get rq_analysis status."""
    analysis_file = os.path.join(rq_dir, "docs", "4_analysis.yaml")
    return "Y" if os.path.exists(analysis_file) else "N"

# Updated validation scores from the archives
KNOWN_SCORES = {
    # From ch7_rq_stats_reassessment_campaign.md (post-reassessment)
    "7.1.1": {"scholar": 9.6, "stats": 8.2},  # Unchanged
    "7.1.2": {"scholar": 9.2, "stats": 9.0},
    "7.1.3": {"scholar": 9.0, "stats": 9.2},
    "7.1.4": {"scholar": 9.1, "stats": 9.4},  # Improved from 8.1
    "7.2.1": {"scholar": 9.5, "stats": 9.1},
    "7.2.2": {"scholar": 9.3, "stats": 9.2},
    "7.2.3": {"scholar": 9.0, "stats": 8.5},  # Unchanged
    "7.2.4": {"scholar": 9.4, "stats": 9.3},
    "7.3.1": {"scholar": 9.8, "stats": 9.4},  # From state.md - fixed
    "7.3.2": {"scholar": 9.2, "stats": 9.4},  # From state.md - fixed from 8.7
    "7.3.3": {"scholar": 9.5, "stats": 9.0},
    "7.3.4": {"scholar": 9.1, "stats": 9.2},
    "7.3.5": {"scholar": 9.0, "stats": 9.3},
    "7.4.1": {"scholar": 9.6, "stats": 9.4},
    "7.4.2": {"scholar": 9.2, "stats": 9.3},  # Improved from 8.0
    "7.4.3": {"scholar": 9.0, "stats": 9.1},  # From state.md - fixed from 8.3
    "7.5.1": {"scholar": 9.3, "stats": 9.4},  # Improved from 8.6
    "7.5.2": {"scholar": 9.5, "stats": 9.2},
    "7.5.3": {"scholar": 9.1, "stats": 9.0},
    "7.5.4": {"scholar": 9.4, "stats": 9.3},
    "7.6.1": {"scholar": 9.2, "stats": 9.1},
    "7.6.2": {"scholar": 9.0, "stats": 8.8},  # Unchanged
    "7.6.3": {"scholar": 9.6, "stats": 9.4},
    "7.6.4": {"scholar": 9.3, "stats": 9.2},
    "7.7.1": {"scholar": "N/A", "stats": "N/A"},  # Not assessed yet
    "7.7.2": {"scholar": 9.1, "stats": 8.2},  # Unchanged
    "7.7.3": {"scholar": 9.4, "stats": 9.3},
    "7.7.4": {"scholar": 9.5, "stats": 9.2},
    "7.8.1": {"scholar": 9.3, "stats": 9.0},
    "7.8.2": {"scholar": 9.0, "stats": 9.1},  # From state.md - fixed from 8.9
    "7.8.3": {"scholar": 9.2, "stats": 9.4},
    "7.8.4": {"scholar": 9.4, "stats": 9.3},  # Improved from 7.9
}

def main():
    ch7_dir = Path("/home/etai/projects/REMEMVR/results/ch7")
    
    # Get all RQ directories
    rq_dirs = sorted([d for d in ch7_dir.iterdir() if d.is_dir() and d.name.startswith("7.")])
    
    rows = []
    
    for rq_dir in rq_dirs:
        rq = rq_dir.name
        
        # Get research question text
        concept_file = rq_dir / "docs" / "1_concept.md"
        question = extract_question(concept_file)
        
        # Get scores (use known values or extract from files)
        if rq in KNOWN_SCORES:
            scholar_score = KNOWN_SCORES[rq]["scholar"]
            stats_score = KNOWN_SCORES[rq]["stats"]
        else:
            scholar_file = rq_dir / "docs" / "1_scholar.md"
            stats_file = rq_dir / "docs" / "1_stats.md"
            scholar_score = extract_score(scholar_file)
            stats_score = extract_score(stats_file)
        
        # Check for 2_plan.md (could be in root or docs/)
        plan_exists = "N"
        if (rq_dir / "2_plan.md").exists():
            plan_exists = "Y"
        elif (rq_dir / "docs" / "2_plan.md").exists():
            plan_exists = "Y"
        
        # Get tools and analysis status
        tools_status = get_tools_status(rq_dir)
        analysis_status = get_analysis_status(rq_dir)
        
        rows.append({
            "rq": rq,
            "question": question,
            "rq_scholar": scholar_score,
            "rq_stats": stats_score,
            "rq_plan": plan_exists,
            "rq_tools": tools_status,
            "rq_analysis": analysis_status
        })
    
    # Write TSV file
    output_file = ch7_dir / "rq_status.tsv"
    with open(output_file, 'w', newline='') as f:
        fieldnames = ["rq", "question", "rq_scholar", "rq_stats", "rq_plan", "rq_tools", "rq_analysis"]
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"Status file created: {output_file}")
    
    # Print summary statistics
    total = len(rows)
    scholar_approved = sum(1 for r in rows if isinstance(r["rq_scholar"], (int, float)) and r["rq_scholar"] >= 9.0)
    stats_approved = sum(1 for r in rows if isinstance(r["rq_stats"], (int, float)) and r["rq_stats"] >= 9.0)
    plans_exist = sum(1 for r in rows if r["rq_plan"] == "Y")
    tools_pass = sum(1 for r in rows if r["rq_tools"] == "pass")
    analysis_done = sum(1 for r in rows if r["rq_analysis"] == "Y")
    
    print(f"\nSummary:")
    print(f"Total RQs: {total}")
    print(f"Scholar approved (≥9.0): {scholar_approved}/{total} ({100*scholar_approved/total:.1f}%)")
    print(f"Stats approved (≥9.0): {stats_approved}/{total} ({100*stats_approved/total:.1f}%)")
    print(f"Plans exist: {plans_exist}/{total} ({100*plans_exist/total:.1f}%)")
    print(f"Tools passed: {tools_pass}/{total} ({100*tools_pass/total:.1f}%)")
    print(f"Analysis done: {analysis_done}/{total} ({100*analysis_done/total:.1f}%)")

if __name__ == "__main__":
    main()