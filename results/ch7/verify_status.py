#!/usr/bin/env python3
"""Verify and update Ch7 RQ status table with actual file existence."""

import os
import csv
from pathlib import Path

def check_files(rq_dir):
    """Check actual file existence for an RQ."""
    status = {}
    
    # Check for 2_plan.md (could be in root or docs/)
    if (rq_dir / "docs" / "2_plan.md").exists():
        status['plan'] = "Y"
    elif (rq_dir / "2_plan.md").exists():
        status['plan'] = "Y"
    else:
        status['plan'] = "N"
    
    # Check for 3_tools.yaml
    if (rq_dir / "docs" / "3_tools.yaml").exists():
        status['tools'] = "pass"
    else:
        status['tools'] = "TBD"
    
    # Check for 4_analysis.yaml
    if (rq_dir / "docs" / "4_analysis.yaml").exists():
        status['analysis'] = "Y"
    else:
        status['analysis'] = "N"
    
    return status

# Known validation scores from archives
KNOWN_SCORES = {
    "7.1.1": {"scholar": 9.6, "stats": 8.2},
    "7.1.2": {"scholar": 9.2, "stats": 9.0},
    "7.1.3": {"scholar": 9.0, "stats": 9.2},
    "7.1.4": {"scholar": 9.1, "stats": 9.4},
    "7.2.1": {"scholar": 9.5, "stats": 9.1},
    "7.2.2": {"scholar": 9.3, "stats": 9.2},
    "7.2.3": {"scholar": 9.0, "stats": 8.5},
    "7.2.4": {"scholar": 9.4, "stats": 9.3},
    "7.3.1": {"scholar": 9.8, "stats": 9.4},
    "7.3.2": {"scholar": 9.2, "stats": 9.4},
    "7.3.3": {"scholar": 9.5, "stats": 9.0},
    "7.3.4": {"scholar": 9.1, "stats": 9.2},
    "7.3.5": {"scholar": 9.0, "stats": 9.3},
    "7.4.1": {"scholar": 9.6, "stats": 9.4},
    "7.4.2": {"scholar": 9.2, "stats": 9.3},
    "7.4.3": {"scholar": 9.0, "stats": 9.1},
    "7.5.1": {"scholar": 9.3, "stats": 9.4},
    "7.5.2": {"scholar": 9.5, "stats": 9.2},
    "7.5.3": {"scholar": 9.1, "stats": 9.0},
    "7.5.4": {"scholar": 9.4, "stats": 9.3},
    "7.6.1": {"scholar": 9.2, "stats": 9.1},
    "7.6.2": {"scholar": 9.0, "stats": 8.8},
    "7.6.3": {"scholar": 9.6, "stats": 9.4},
    "7.6.4": {"scholar": 9.3, "stats": 9.2},
    "7.7.1": {"scholar": "N/A", "stats": "N/A"},
    "7.7.2": {"scholar": 9.1, "stats": 8.2},
    "7.7.3": {"scholar": 9.4, "stats": 9.3},
    "7.7.4": {"scholar": 9.5, "stats": 9.2},
    "7.8.1": {"scholar": 9.3, "stats": 9.0},
    "7.8.2": {"scholar": 9.0, "stats": 9.1},
    "7.8.3": {"scholar": 9.2, "stats": 9.4},
    "7.8.4": {"scholar": 9.4, "stats": 9.3},
}

# Research questions from concept files
RQ_QUESTIONS = {
    "7.1.1": "Do cognitive tests predict overall REMEMVR ability?",
    "7.1.2": "Do cognitive tests predict baseline ability more than forgetting rate?",
    "7.1.3": "Do verbal tests predict What, visuospatial predict Where?",
    "7.1.4": "What proportion of REMEMVR variance remains unexplained?",
    "7.2.1": "Does age explain variance beyond cognitive tests?",
    "7.2.2": "What proportion of age variance is attenuated by cognitive tests?",
    "7.2.3": "Do cognitive tests predict differently for younger vs older?",
    "7.2.4": "Does REMEMVR show age-invariance while RAVLT shows decline?",
    "7.3.1": "Do cognitive tests predict confidence as they predict accuracy?",
    "7.3.2": "Do cognitive tests predict calibration vs overconfidence?",
    "7.3.3": "Do cognitive tests predict high-confidence errors?",
    "7.3.4": "Does anxiety/depression predict metacognitive accuracy?",
    "7.3.5": "Do well-calibrated high performers show cognitive reserve?",
    "7.4.1": "Does RAVLT predict Free Recall more than Recognition?",
    "7.4.2": "Does BVMT predict Where more than What?",
    "7.4.3": "Does RPM predict integrated What+Where+When performance?",
    "7.5.1": "Do self-reported factors predict REMEMVR performance?",
    "7.5.2": "Do DASS subscales predict episodic memory accuracy?",
    "7.5.3": "Do memory strategies predict REMEMVR performance?",
    "7.5.4": "Does sleep quality before test predict that test's performance?",
    "7.6.1": "Do cognitive tests predict forgetting slope or just intercept?",
    "7.6.2": "Does RAVLT forgetting predict REMEMVR forgetting rate?",
    "7.6.3": "Does ICC_slope pattern replicate across domains?",
    "7.6.4": "Do slope predictors change after IRT purification?",
    "7.7.1": "Can REMEMVR predict traditional test performance?",
    "7.7.2": "Who shows RAVLT-REMEMVR divergence?",
    "7.7.3": "Does RAVLT Learning Slope predict better than Total?",
    "7.7.4": "Can we identify false negatives (low RAVLT, normal REMEMVR)?",
    "7.8.1": "Are there distinct latent profiles of REMEMVR performance?",
    "7.8.2": "Do cognitive profiles correspond to REMEMVR profiles?",
    "7.8.3": "What is the most parsimonious model to predict REMEMVR?",
    "7.8.4": "Does multivariate prediction outperform separate domains?",
}

def main():
    ch7_dir = Path("/home/etai/projects/REMEMVR/results/ch7")
    
    # Get all RQ directories
    rq_dirs = sorted([d for d in ch7_dir.iterdir() if d.is_dir() and d.name.startswith("7.")])
    
    rows = []
    
    for rq_dir in rq_dirs:
        rq = rq_dir.name
        
        # Get question
        question = RQ_QUESTIONS.get(rq, "UNKNOWN")
        
        # Get validation scores
        if rq in KNOWN_SCORES:
            scholar_score = KNOWN_SCORES[rq]["scholar"]
            stats_score = KNOWN_SCORES[rq]["stats"]
        else:
            scholar_score = "N/A"
            stats_score = "N/A"
        
        # Check actual file existence
        file_status = check_files(rq_dir)
        
        rows.append({
            "rq": rq,
            "question": question,
            "rq_scholar": scholar_score,
            "rq_stats": stats_score,
            "rq_plan": file_status['plan'],
            "rq_tools": file_status['tools'],
            "rq_analysis": file_status['analysis']
        })
    
    # Write TSV file
    output_file = ch7_dir / "rq_status.tsv"
    with open(output_file, 'w', newline='') as f:
        fieldnames = ["rq", "question", "rq_scholar", "rq_stats", "rq_plan", "rq_tools", "rq_analysis"]
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"Updated status file: {output_file}")
    
    # Print summary statistics
    total = len(rows)
    scholar_approved = sum(1 for r in rows if isinstance(r["rq_scholar"], (int, float)) and r["rq_scholar"] >= 9.0)
    stats_approved = sum(1 for r in rows if isinstance(r["rq_stats"], (int, float)) and r["rq_stats"] >= 9.0)
    plans_exist = sum(1 for r in rows if r["rq_plan"] == "Y")
    tools_pass = sum(1 for r in rows if r["rq_tools"] == "pass")
    analysis_done = sum(1 for r in rows if r["rq_analysis"] == "Y")
    
    print(f"\nActual Status Summary:")
    print(f"Total RQs: {total}")
    print(f"Scholar approved (≥9.0): {scholar_approved}/{total} ({100*scholar_approved/total:.1f}%)")
    print(f"Stats approved (≥9.0): {stats_approved}/{total} ({100*stats_approved/total:.1f}%)")
    print(f"Plans exist: {plans_exist}/{total} ({100*plans_exist/total:.1f}%)")
    print(f"Tools passed: {tools_pass}/{total} ({100*tools_pass/total:.1f}%)")
    print(f"Analysis done: {analysis_done}/{total} ({100*analysis_done/total:.1f}%)")
    
    # List any missing pieces
    print("\nMissing Components:")
    missing_found = False
    for r in rows:
        missing = []
        if r["rq_plan"] != "Y":
            missing.append("plan")
        if r["rq_tools"] != "pass":
            missing.append("tools")
        if missing:
            print(f"  {r['rq']}: Missing {', '.join(missing)}")
            missing_found = True
    
    if not missing_found:
        print("  None - All RQs have plans and tools!")

if __name__ == "__main__":
    main()