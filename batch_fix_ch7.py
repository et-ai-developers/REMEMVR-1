#!/usr/bin/env python3
"""
Batch fix Ch7 RQs with stats scores < 9.0
Parallel processing approach for efficiency
"""
import os
import re
import subprocess
from pathlib import Path

ch7_dir = Path("/home/etai/projects/REMEMVR/results/ch7")

def get_stats_score(rq_dir):
    """Extract stats score from status.yaml"""
    status_file = rq_dir / "status.yaml"
    if status_file.exists():
        content = status_file.read_text()
        match = re.search(r'rq_stats:.*?context_dump:.*?"([^"]+)"', content, re.DOTALL)
        if match:
            score_match = re.search(r'(\d+\.\d+)/10', match.group(1))
            if score_match:
                return float(score_match.group(1))
    return None

def get_failed_rqs():
    """Get all RQs with stats score < 9.0"""
    failed_rqs = []
    for rq_dir in sorted(ch7_dir.iterdir()):
        if rq_dir.is_dir():
            score = get_stats_score(rq_dir)
            if score and score < 9.0:
                # Check if plan exists
                plan_file = rq_dir / "docs" / "2_plan.md"
                has_plan = plan_file.exists()
                failed_rqs.append({
                    'rq': rq_dir.name,
                    'score': score,
                    'path': rq_dir,
                    'has_plan': has_plan
                })
    return sorted(failed_rqs, key=lambda x: x['score'])

def categorize_issues(failed_rqs):
    """Group RQs by score severity"""
    critical = []  # < 7.0
    severe = []    # 7.0-7.9
    moderate = []  # 8.0-8.5
    minor = []     # 8.5-8.9
    
    for rq in failed_rqs:
        if rq['score'] < 7.0:
            critical.append(rq)
        elif rq['score'] < 8.0:
            severe.append(rq)
        elif rq['score'] <= 8.5:
            moderate.append(rq)
        else:
            minor.append(rq)
    
    return {
        'critical': critical,
        'severe': severe,
        'moderate': moderate,
        'minor': minor
    }

def generate_batch_commands():
    """Generate commands to process multiple RQs in parallel"""
    failed_rqs = get_failed_rqs()
    categories = categorize_issues(failed_rqs)
    
    print("=" * 60)
    print("CH7 BATCH PROCESSING PLAN")
    print("=" * 60)
    print(f"Total failed RQs: {len(failed_rqs)}")
    print(f"Critical (<7.0): {len(categories['critical'])}")
    print(f"Severe (7.0-7.9): {len(categories['severe'])}")
    print(f"Moderate (8.0-8.5): {len(categories['moderate'])}")
    print(f"Minor (8.5-8.9): {len(categories['minor'])}")
    print()
    
    # First, delete all plans for failed RQs
    print("STEP 1: Delete plans for failed RQs")
    print("-" * 40)
    delete_commands = []
    for rq in failed_rqs:
        if rq['has_plan']:
            plan_path = rq['path'] / "docs" / "2_plan.md"
            delete_commands.append(f"rm {plan_path}")
            print(f"  rm {rq['rq']}/docs/2_plan.md (score: {rq['score']})")
    
    print()
    print("STEP 2: Update status.yaml files")
    print("-" * 40)
    for rq in failed_rqs:
        if rq['has_plan']:
            print(f"  Update {rq['rq']}/status.yaml - mark planner as pending")
    
    print()
    print("STEP 3: Process by severity (parallel batches)")
    print("-" * 40)
    
    # Process critical and severe first (they need most work)
    priority_rqs = categories['critical'] + categories['severe']
    if priority_rqs:
        print(f"BATCH 1 (Critical+Severe): {len(priority_rqs)} RQs")
        for rq in priority_rqs:
            print(f"  - {rq['rq']}: {rq['score']}/10")
    
    # Then moderate
    if categories['moderate']:
        print(f"BATCH 2 (Moderate): {len(categories['moderate'])} RQs")
        for rq in categories['moderate']:
            print(f"  - {rq['rq']}: {rq['score']}/10")
    
    # Finally minor (might pass with small fixes)
    if categories['minor']:
        print(f"BATCH 3 (Minor): {len(categories['minor'])} RQs")
        for rq in categories['minor']:
            print(f"  - {rq['rq']}: {rq['score']}/10")
    
    print()
    print("COMMON FIXES TO APPLY:")
    print("-" * 40)
    print("1. Add power analysis for sample size justification")
    print("2. Add cross-validation strategy (5-fold, seed=42)")
    print("3. Add remedial actions for assumption violations")
    print("4. Fix Bonferroni corrections where needed")
    print("5. Add bootstrap specifications (1000 reps, seed=42)")
    print("6. Document tool limitations but note as implementation issue")
    print("7. Add simultaneous modeling for two-stage analyses")
    print("8. Specify linearity testing procedures")
    
    return failed_rqs, categories

if __name__ == "__main__":
    failed_rqs, categories = generate_batch_commands()
    
    print()
    print("EXECUTION STRATEGY:")
    print("-" * 40)
    print("1. Delete all plans first (batch operation)")
    print("2. Fix concepts in parallel batches by severity")
    print("3. Re-run rq_stats validation in parallel")
    print("4. Run rq_planner only for RQs that pass (≥9.0)")
    print()
    print(f"Estimated time: ~2-3 hours for all {len(failed_rqs)} RQs")
    print("(vs ~8-10 hours sequential)")